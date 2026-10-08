"""Atomic, dependency-aware storage primitives for resumable chunked work."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path

from .provenance import dependency_fingerprint, sha256_file


class CacheIntegrityError(ValueError):
    """Raised when cached data cannot be safely reused or is incomplete."""


def atomic_write_bytes(path: str | Path, content: bytes) -> None:
    """Write bytes through a temporary sibling file and atomically replace the destination."""
    destination = Path(path)
    if not isinstance(content, bytes):
        raise TypeError("content must be bytes")
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _atomic_write_json(path: Path, payload: Mapping[str, object]) -> None:
    encoded = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    atomic_write_bytes(path, encoded)


def _validate_chunk_ids(chunk_ids: Sequence[str]) -> tuple[str, ...]:
    values = tuple(chunk_ids)
    if any(not isinstance(value, str) or not value for value in values):
        raise ValueError("chunk IDs must be non-empty strings")
    if len(values) != len(set(values)):
        raise ValueError("chunk IDs must be unique")
    return values


class ResumableChunkCache:
    """Persist exact, dependency-bound chunks and verify completeness before reuse."""

    def __init__(
        self,
        root: str | Path,
        *,
        dependencies: Mapping[str, str],
        expected_chunk_ids: Sequence[str],
    ) -> None:
        self.root = Path(root)
        self.dependencies = dict(dependencies)
        self.dependency_fingerprint = dependency_fingerprint(self.dependencies)
        self.expected_chunk_ids = _validate_chunk_ids(expected_chunk_ids)

    def _token(self, chunk_id: str) -> str:
        return hashlib.sha256(chunk_id.encode("utf-8")).hexdigest()

    def _chunk_path(self, chunk_id: str) -> Path:
        return self.root / f"{self._token(chunk_id)}.chunk"

    def _metadata_path(self, chunk_id: str) -> Path:
        return self.root / f"{self._token(chunk_id)}.meta.json"

    def _check_id(self, chunk_id: str) -> None:
        if chunk_id not in self.expected_chunk_ids:
            raise CacheIntegrityError(f"unexpected chunk ID: {chunk_id}")

    def invalidate_chunk(self, chunk_id: str) -> None:
        """Remove a chunk's completion record before removing its data file."""
        self._check_id(chunk_id)
        self._metadata_path(chunk_id).unlink(missing_ok=True)
        self._chunk_path(chunk_id).unlink(missing_ok=True)

    def _is_reusable(self, chunk_id: str) -> bool:
        self._check_id(chunk_id)
        data_path = self._chunk_path(chunk_id)
        metadata_path = self._metadata_path(chunk_id)
        if not data_path.is_file() or not metadata_path.is_file():
            self.invalidate_chunk(chunk_id)
            return False
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if not isinstance(metadata, dict):
                raise TypeError("metadata must be an object")
            valid = (
                metadata.get("schema") == "chunk-cache/v1"
                and metadata.get("complete") is True
                and metadata.get("chunk_id") == chunk_id
                and metadata.get("dependency_fingerprint") == self.dependency_fingerprint
                and metadata.get("sha256") == sha256_file(data_path)
            )
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError):
            valid = False
        if not valid:
            self.invalidate_chunk(chunk_id)
        return valid

    def is_chunk_reusable(self, chunk_id: str) -> bool:
        """Return whether a chunk has valid data and matching completion metadata."""
        return self._is_reusable(chunk_id)

    def read_chunk(self, chunk_id: str) -> bytes | None:
        """Read a verified chunk, returning None when it must be recomputed."""
        if not self._is_reusable(chunk_id):
            return None
        try:
            content = self._chunk_path(chunk_id).read_bytes()
            metadata = json.loads(self._metadata_path(chunk_id).read_text(encoding="utf-8"))
            if not isinstance(metadata, dict) or hashlib.sha256(content).hexdigest() != metadata.get(
                "sha256"
            ):
                raise ValueError("chunk content changed during verification")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError):
            self.invalidate_chunk(chunk_id)
            return None
        return content

    def write_chunk(self, chunk_id: str, content: bytes) -> None:
        """Atomically write a chunk and then its completion metadata."""
        self._check_id(chunk_id)
        if not isinstance(content, bytes):
            raise TypeError("content must be bytes")
        data_path = self._chunk_path(chunk_id)
        metadata_path = self._metadata_path(chunk_id)
        self.root.mkdir(parents=True, exist_ok=True)
        atomic_write_bytes(data_path, content)
        metadata = {
            "schema": "chunk-cache/v1",
            "chunk_id": chunk_id,
            "dependency_fingerprint": self.dependency_fingerprint,
            "sha256": sha256_file(data_path),
            "complete": True,
        }
        _atomic_write_json(metadata_path, metadata)

    def resume(self) -> tuple[str, ...]:
        """Return missing or stale chunk IDs and invalidate any unsafe cached copies."""
        return tuple(chunk_id for chunk_id in self.expected_chunk_ids if not self._is_reusable(chunk_id))

    def verify_complete(self) -> bool:
        """Require every expected chunk exactly once and reject unexpected sidecars."""
        missing = self.resume()
        if missing:
            raise CacheIntegrityError(f"cache is incomplete; chunks need recomputation: {list(missing)}")

        expected_metadata_paths = {self._metadata_path(chunk_id).resolve() for chunk_id in self.expected_chunk_ids}
        expected_chunk_paths = {self._chunk_path(chunk_id).resolve() for chunk_id in self.expected_chunk_ids}
        observed_chunk_paths = {path.resolve() for path in self.root.glob("*.chunk")}
        if observed_chunk_paths != expected_chunk_paths:
            raise CacheIntegrityError("cache data files do not match the exact expected chunk IDs")
        observed_ids: list[str] = []
        for metadata_path in self.root.glob("*.meta.json"):
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                if not isinstance(metadata, dict) or not isinstance(metadata.get("chunk_id"), str):
                    raise TypeError("invalid chunk metadata")
                chunk_id = metadata["chunk_id"]
                observed_ids.append(chunk_id)
                if chunk_id not in self.expected_chunk_ids or metadata_path.resolve() not in expected_metadata_paths:
                    raise ValueError(f"unexpected chunk metadata for ID {chunk_id!r}")
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
                raise CacheIntegrityError(f"cache contains invalid or unexpected metadata: {exc}") from exc

        if len(observed_ids) != len(set(observed_ids)):
            raise CacheIntegrityError("cache contains duplicate chunk metadata")
        if set(observed_ids) != set(self.expected_chunk_ids):
            raise CacheIntegrityError("cache metadata does not match the exact expected chunk IDs")
        return True

    def invalidate_all(self) -> None:
        """Invalidate all known chunk completion records before removing their data."""
        for chunk_id in self.expected_chunk_ids:
            self._metadata_path(chunk_id).unlink(missing_ok=True)
        for chunk_id in self.expected_chunk_ids:
            self._chunk_path(chunk_id).unlink(missing_ok=True)
