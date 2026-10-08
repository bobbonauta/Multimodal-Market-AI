
import pandas as pd
import pytest

from multimodal_market_ai.provenance import (
    ArtifactSealError,
    RecordIDMismatchError,
    compare_record_ids,
    exact_one_to_one_join,
    seal_artifact,
    verify_artifact_seal,
)


def test_seal_binds_dependencies_and_exact_record_ids(tmp_path) -> None:
    artifact = tmp_path / "artifact.bin"
    artifact.write_bytes(b"synthetic artifact")
    dependencies = {"source": "sha256:abc", "transform": "v1"}
    record_ids = ["row-1", "row-2"]

    seal_artifact(artifact, dependencies=dependencies, record_ids=record_ids)
    assert verify_artifact_seal(artifact, dependencies=dependencies, record_ids=record_ids)

    with pytest.raises(ArtifactSealError):
        verify_artifact_seal(
            artifact,
            dependencies={**dependencies, "transform": "v2"},
            record_ids=record_ids,
        )


def test_record_id_comparison_reports_missing_extra_and_duplicates() -> None:
    report = compare_record_ids(["a", "b", "b"], ["b", "c", "c"])

    assert report.missing_ids == ("a",)
    assert report.extra_ids == ("c",)
    assert report.duplicate_expected_ids == ("b",)
    assert report.duplicate_actual_ids == ("c",)
    with pytest.raises(RecordIDMismatchError):
        exact_one_to_one_join(
            pd.DataFrame({"record_id": ["a", "b"]}),
            pd.DataFrame({"record_id": ["a", "c"]}),
            on="record_id",
        )


def test_exact_one_to_one_join_preserves_left_order() -> None:
    left = pd.DataFrame({"record_id": ["b", "a"], "value": [2, 1]})
    right = pd.DataFrame({"record_id": ["a", "b"], "feature": [10, 20]})

    joined = exact_one_to_one_join(left, right, on="record_id")

    assert joined["record_id"].tolist() == ["b", "a"]
    assert joined["feature"].tolist() == [20, 10]


def test_exact_one_to_one_join_accepts_integer_record_ids() -> None:
    left = pd.DataFrame({"record_id": [2, 1], "value": [20, 10]})
    right = pd.DataFrame({"record_id": [1, 2], "feature": [100, 200]})

    joined = exact_one_to_one_join(left, right, on="record_id")

    assert joined["record_id"].tolist() == [2, 1]
    assert joined["feature"].tolist() == [200, 100]


def test_corrupt_seal_fails_closed(tmp_path) -> None:
    artifact = tmp_path / "artifact.bin"
    artifact.write_bytes(b"synthetic artifact")
    seal_artifact(artifact, dependencies={"source": "v1"}, record_ids=["row-1"])
    sidecar = tmp_path / "artifact.bin.seal.json"
    sidecar.write_text("{broken", encoding="utf-8")

    with pytest.raises(ArtifactSealError):
        verify_artifact_seal(artifact, dependencies={"source": "v1"}, record_ids=["row-1"])


def test_artifact_content_change_invalidates_seal(tmp_path) -> None:
    artifact = tmp_path / "artifact.bin"
    artifact.write_bytes(b"first")
    seal_artifact(artifact, dependencies={"source": "v1"}, record_ids=["row-1"])
    artifact.write_bytes(b"changed")

    with pytest.raises(ArtifactSealError):
        verify_artifact_seal(artifact, dependencies={"source": "v1"}, record_ids=["row-1"])
