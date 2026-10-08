import io
import runpy
from pathlib import Path

import pandas as pd
import pytest

from multimodal_market_ai.provenance import ArtifactSealError

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "candidate_workflow.py"
workflow = runpy.run_path(str(EXAMPLE))


def test_committed_candidates_match_declared_public_rule() -> None:
    manifest = workflow["run"](EXAMPLE.parent / "synthetic_candidates", check=True)
    assert [record["record_id"] for record in manifest["records"]] == [
        "synthetic-001",
        "synthetic-003",
        "synthetic-006",
        "synthetic-007",
        "synthetic-009",
        "synthetic-011",
    ]
    assert all(record["delta"] > 0 for record in manifest["records"])


def test_future_observation_mutation_leaves_earlier_candidates_unchanged() -> None:
    source = workflow["synthetic_source_bytes"]()
    original = workflow["build_manifest"](source)
    frame = pd.read_csv(io.BytesIO(source))
    frame.loc[frame.index[-1], "measurement"] = -999
    changed = workflow["build_manifest"](frame.to_csv(index=False, lineterminator="\n").encode())
    assert changed["records"] == original["records"][:-1]


def test_regeneration_is_deterministic_and_corrupt_sidecar_fails_closed(tmp_path) -> None:
    workflow["run"](tmp_path)
    first = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    workflow["run"](tmp_path)
    assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == first
    workflow["run"](tmp_path, check=True)
    (tmp_path / "candidates.json.seal.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(ArtifactSealError):
        workflow["run"](tmp_path, check=True)


def test_missing_candidate_is_rejected_even_with_existing_seal(tmp_path) -> None:
    workflow["run"](tmp_path)
    artifact = tmp_path / "candidates.json"
    artifact.write_text('{"records": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="regenerated selection"):
        workflow["run"](tmp_path, check=True)
