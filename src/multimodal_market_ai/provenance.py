"""Artifact integrity, dependency lineage, and exact record matching helpers."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from numbers import Integral
from pathlib import Path

import pandas as pd


class ArtifactSealError(ValueError):
    """Raised when an artifact seal is missing, corrupt, stale, or inconsistent."""


class RecordIDMismatchError(ValueError):
    """Raised when record identifiers are not an exact one-to-one match."""

    def __init__(
        self,
        *,
        missing_ids: Sequence[str | int] = (),
        extra_ids: Sequence[str | int] = (),
        duplicate_expected_ids: Sequence[str | int] = (),
        duplicate_actual_ids: Sequence[str | int] = (),
    ) -> None:
        self.missing_ids = tuple(missing_ids)
        self.extra_ids = tuple(extra_ids)
        self.duplicate_expected_ids = tuple(duplicate_expected_ids)
        self.duplicate_actual_ids = tuple(duplicate_actual_ids)
        parts = []
        if self.missing_ids:
            parts.append(f"missing IDs: {list(self.missing_ids)}")
        if self.extra_ids:
            parts.append(f"extra IDs: {list(self.extra_ids)}")
        if self.duplicate_expected_ids:
            parts.append(f"duplicate expected IDs: {list(self.duplicate_expected_ids)}")
        if self.duplicate_actual_ids:
            parts.append(f"duplicate actual IDs: {list(self.duplicate_actual_ids)}")
        super().__init__("record IDs are not an exact one-to-one match (" + "; ".join(parts) + ")")


@dataclass(frozen=True)
class RecordIDReport:
    """Exact-set comparison result for two record ID sequences."""

    missing_ids: tuple[str | int, ...]
    extra_ids: tuple[str | int, ...]
    duplicate_expected_ids: tuple[str | int, ...]
    duplicate_actual_ids: tuple[str | int, ...]

    @property
    def is_exact(self) -> bool:
        """Return whether both sequences contain the same unique identifiers."""
        return not (
            self.missing_ids
            or self.extra_ids
            or self.duplicate_expected_ids
            or self.duplicate_actual_ids
        )


def _validated_ids(ids: Sequence[str | int], label: str) -> tuple[str | int, ...]:
    values = tuple(ids)
    normalized: list[str | int] = []
    for value in values:
        if isinstance(value, str) and value:
            normalized.append(value)
        elif isinstance(value, Integral) and not isinstance(value, bool):
            normalized.append(int(value))
        else:
            raise ValueError(f"{label} must contain non-empty string or integer IDs")
    return tuple(normalized)


def compare_record_ids(
    expected_ids: Sequence[str | int], actual_ids: Sequence[str | int]
) -> RecordIDReport:
    """Detect missing, extra, and duplicate IDs without silently dropping records."""
    expected = _validated_ids(expected_ids, "expected_ids")
    actual = _validated_ids(actual_ids, "actual_ids")
    expected_counts = Counter(expected)
    actual_counts = Counter(actual)
    return RecordIDReport(
        missing_ids=tuple(value for value in expected if value not in actual_counts),
        extra_ids=tuple(dict.fromkeys(value for value in actual if value not in expected_counts)),
        duplicate_expected_ids=tuple(value for value, count in expected_counts.items() if count > 1),
        duplicate_actual_ids=tuple(value for value, count in actual_counts.items() if count > 1),
    )


def require_exact_record_ids(
    expected_ids: Sequence[str | int], actual_ids: Sequence[str | int]
) -> None:
    """Raise when IDs are missing, unexpected, duplicated, or otherwise mismatched."""
    report = compare_record_ids(expected_ids, actual_ids)
    if not report.is_exact:
        raise RecordIDMismatchError(
            missing_ids=report.missing_ids,
            extra_ids=report.extra_ids,
            duplicate_expected_ids=report.duplicate_expected_ids,
            duplicate_actual_ids=report.duplicate_actual_ids,
        )


def exact_one_to_one_join(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    on: str,
) -> pd.DataFrame:
    """Join two frames only when their non-null record IDs match exactly once."""
    for label, frame in (("left", left), ("right", right)):
        if on not in frame.columns:
            raise RecordIDMismatchError(extra_ids=(f"{label} is missing key column {on}",))
        if frame[on].isna().any():
            raise RecordIDMismatchError(missing_ids=(f"{label} contains null record IDs",))

    left_ids = _validated_ids(left[on].tolist(), "left record IDs")
    right_ids = _validated_ids(right[on].tolist(), "right record IDs")
    require_exact_record_ids(left_ids, right_ids)

    order_column = "__exact_join_order__"
    while order_column in left.columns or order_column in right.columns:
        order_column += "_"
    ordered_left = left.copy()
    ordered_left[order_column] = range(len(ordered_left))
    merged = ordered_left.merge(right, on=on, how="inner", validate="one_to_one", sort=False)
    return merged.sort_values(order_column, kind="stable").drop(columns=order_column).reset_index(drop=True)


def dependency_fingerprint(dependencies: Mapping[str, str]) -> str:
    """Return a stable SHA-256 fingerprint for named dependency digests or revisions."""
    normalized = dict(dependencies)
    if any(not isinstance(key, str) or not key for key in normalized):
        raise ValueError("dependency names must be non-empty strings")
    if any(not isinstance(value, str) or not value for value in normalized.values()):
        raise ValueError("dependency values must be non-empty strings")
    canonical = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Compute the SHA-256 digest of a file without loading it all into memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _ids_fingerprint(ids: Sequence[str | int]) -> str:
    payload = json.dumps(list(ids), ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _sidecar_path(artifact_path: Path, sidecar_path: str | Path | None) -> Path:
    return Path(sidecar_path) if sidecar_path is not None else Path(str(artifact_path) + ".seal.json")


def _atomic_write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def seal_artifact(
    artifact_path: str | Path,
    *,
    dependencies: Mapping[str, str],
    record_ids: Sequence[str | int],
    sidecar_path: str | Path | None = None,
) -> dict[str, object]:
    """Write an atomic sidecar binding artifact bytes, dependencies, and exact record IDs."""
    artifact = Path(artifact_path)
    if not artifact.is_file():
        raise ArtifactSealError(f"artifact does not exist or is not a file: {artifact}")
    ids = _validated_ids(record_ids, "record_ids")
    if len(ids) != len(set(ids)):
        duplicates = tuple(value for value, count in Counter(ids).items() if count > 1)
        raise RecordIDMismatchError(duplicate_expected_ids=duplicates)
    normalized_dependencies = dict(dependencies)
    dependency_hash = dependency_fingerprint(normalized_dependencies)
    payload: dict[str, object] = {
        "schema": "artifact-seal/v1",
        "artifact_sha256": sha256_file(artifact),
        "dependencies": normalized_dependencies,
        "dependency_fingerprint": dependency_hash,
        "record_ids": list(ids),
        "record_ids_sha256": _ids_fingerprint(ids),
    }
    _atomic_write_json(_sidecar_path(artifact, sidecar_path), payload)
    return payload


def verify_artifact_seal(
    artifact_path: str | Path,
    *,
    dependencies: Mapping[str, str],
    record_ids: Sequence[str | int],
    sidecar_path: str | Path | None = None,
) -> bool:
    """Verify a seal or raise; malformed and stale sidecars always fail closed."""
    artifact = Path(artifact_path)
    sidecar = _sidecar_path(artifact, sidecar_path)
    try:
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema") != "artifact-seal/v1":
            raise ValueError("unsupported or missing schema")
        raw_ids = payload["record_ids"]
        if not isinstance(raw_ids, list):
            raise TypeError("sealed record IDs must be a list")
        stored_ids = _validated_ids(raw_ids, "sealed record_ids")
        if len(stored_ids) != len(set(stored_ids)):
            raise ValueError("sealed record IDs contain duplicates")
        current_ids = _validated_ids(record_ids, "record_ids")
        if stored_ids != current_ids:
            raise ValueError("record IDs or their order changed")
        if payload.get("record_ids_sha256") != _ids_fingerprint(stored_ids):
            raise ValueError("record ID fingerprint mismatch")
        stored_dependencies = payload["dependencies"]
        if not isinstance(stored_dependencies, dict):
            raise TypeError("sealed dependencies must be an object")
        current_dependencies = dict(dependencies)
        if stored_dependencies != current_dependencies:
            raise ValueError("dependency values changed")
        current_dependency_hash = dependency_fingerprint(current_dependencies)
        if payload.get("dependency_fingerprint") != current_dependency_hash:
            raise ValueError("dependency fingerprint mismatch")
        if not artifact.is_file() or payload.get("artifact_sha256") != sha256_file(artifact):
            raise ValueError("artifact is missing or its content changed")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ArtifactSealError(f"artifact is not reusable: {exc}") from exc
    return True
