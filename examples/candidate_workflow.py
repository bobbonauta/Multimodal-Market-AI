"""Reproduce an auditable candidate manifest from explicitly synthetic observations."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path

import pandas as pd

from multimodal_market_ai.audit import audit_causal_features
from multimodal_market_ai.cache import atomic_write_bytes
from multimodal_market_ai.provenance import (
    require_exact_record_ids,
    seal_artifact,
    verify_artifact_seal,
)

SELECTOR_REVISION = "synthetic-increase/v1"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "synthetic_candidates"


def synthetic_source_bytes() -> bytes:
    """Return a fixed, invented observation sequence with no external data dependency."""
    measurements = [10, 12, 11, 14, 14, 13, 15, 16, 12, 17, 15, 18]
    timestamps = pd.date_range("2000-01-01", periods=len(measurements), freq="D", tz="UTC")
    lines = ["record_id,decision_ts,measurement"]
    for position, (timestamp, measurement) in enumerate(zip(timestamps, measurements, strict=True)):
        lines.append(f"synthetic-{position:03d},{timestamp.isoformat()},{measurement}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def build_manifest(source: bytes) -> dict[str, object]:
    """Select rows where the current measurement exceeds the preceding observation."""
    frame = pd.read_csv(io.BytesIO(source))
    require_exact_record_ids(frame["record_id"].tolist(), frame["record_id"].tolist())
    decision = pd.to_datetime(frame["decision_ts"], utc=True, errors="raise")
    if decision.isna().any() or not decision.is_monotonic_increasing or decision.duplicated().any():
        raise ValueError("observation timestamps must be unique, valid, and increasing")
    measurement = pd.to_numeric(frame["measurement"], errors="raise")
    if measurement.isna().any() or not measurement.map(
        lambda value: float("-inf") < value < float("inf")
    ).all():
        raise ValueError("measurements must be finite")

    frame["measurement"] = measurement
    frame["decision_ts"] = decision
    frame["previous_measurement"] = measurement.shift(1)
    frame["previous_available_ts"] = decision.shift(1)
    frame["delta"] = measurement - frame["previous_measurement"]
    frame["current_available_ts"] = decision
    eligible = frame.iloc[1:].copy()
    report = audit_causal_features(
        eligible,
        decision_ts_column="decision_ts",
        feature_columns=["measurement", "previous_measurement", "delta"],
        allowed_features=["measurement", "previous_measurement", "delta"],
        availability_columns={
            "measurement": "current_available_ts",
            "previous_measurement": "previous_available_ts",
            "delta": "current_available_ts",
        },
        forbidden_columns=["future_measurement", "outcome_value"],
    )
    selected = eligible.loc[eligible["delta"] > 0].copy()
    selected["decision_ts"] = selected["decision_ts"].map(lambda value: value.isoformat())
    records = selected[
        ["record_id", "decision_ts", "measurement", "previous_measurement", "delta"]
    ].to_dict(orient="records")
    # Normalize newlines so the selector digest is portable across operating systems.
    selector_bytes = Path(__file__).read_text(encoding="utf-8").encode("utf-8")
    return {
        "schema": "synthetic-candidate-manifest/v1",
        "data_origin": "entirely synthetic",
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "selector_revision": SELECTOR_REVISION,
        "selector_sha256": hashlib.sha256(selector_bytes).hexdigest(),
        "selection_rule": "measurement > previous_measurement; first observation excluded",
        "causal_audit": {
            "result": "pass",
            "rows_checked": report.rows_checked,
            "checked_features": list(report.checked_features),
        },
        "records": records,
    }


def manifest_bytes(manifest: dict[str, object]) -> bytes:
    """Serialize the manifest reproducibly without machine-specific metadata."""
    return (json.dumps(manifest, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def run(output_dir: Path, *, check: bool = False) -> dict[str, object]:
    """Generate the public fixture or verify its bytes, lineage, and exact record IDs."""
    source = synthetic_source_bytes()
    manifest = build_manifest(source)
    expected = manifest_bytes(manifest)
    source_path = output_dir / "observations.csv"
    manifest_path = output_dir / "candidates.json"
    dependencies = {
        "source": manifest["source_sha256"],
        "selector": manifest["selector_sha256"],
        "selector_revision": SELECTOR_REVISION,
    }
    record_ids = [record["record_id"] for record in manifest["records"]]
    if check:
        if source_path.read_bytes() != source:
            raise ValueError("source fixture differs from the declared synthetic observations")
        if manifest_path.read_bytes() != expected:
            raise ValueError("candidate manifest differs from the regenerated selection")
        verify_artifact_seal(manifest_path, dependencies=dependencies, record_ids=record_ids)
    else:
        atomic_write_bytes(source_path, source)
        atomic_write_bytes(manifest_path, expected)
        seal_artifact(manifest_path, dependencies=dependencies, record_ids=record_ids)
    return manifest


def main() -> None:
    """Run the example from the repository root after installing the public package."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Verify committed artifacts without writing")
    args = parser.parse_args()
    manifest = run(args.output_dir, check=args.check)
    action = "Verified" if args.check else "Generated"
    print(f"{action} synthetic candidate manifest: {len(manifest['records'])} records")


if __name__ == "__main__":
    main()
