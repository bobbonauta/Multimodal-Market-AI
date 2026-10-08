import hashlib

import pytest

from multimodal_market_ai.cache import CacheIntegrityError, ResumableChunkCache


def test_interrupted_and_stale_chunks_are_invalidated_and_resumed(tmp_path) -> None:
    interrupted = ResumableChunkCache(
        tmp_path / "interrupted",
        dependencies={"source": "v1"},
        expected_chunk_ids=["chunk-a"],
    )
    interrupted.root.mkdir(parents=True)
    token = hashlib.sha256(b"chunk-a").hexdigest()
    (interrupted.root / f"{token}.chunk").write_bytes(b"partial")

    assert interrupted.resume() == ("chunk-a",)
    assert not (interrupted.root / f"{token}.chunk").exists()

    stale_path = tmp_path / "stale"
    old_cache = ResumableChunkCache(
        stale_path,
        dependencies={"source": "v1"},
        expected_chunk_ids=["chunk-a"],
    )
    old_cache.write_chunk("chunk-a", b"complete")
    new_cache = ResumableChunkCache(
        stale_path,
        dependencies={"source": "v2"},
        expected_chunk_ids=["chunk-a"],
    )

    assert new_cache.resume() == ("chunk-a",)
    assert new_cache.read_chunk("chunk-a") is None


def test_cache_requires_exact_chunk_ids_and_supports_deterministic_rerun(tmp_path) -> None:
    expected = ["part-1", "part-2"]
    first_run = ResumableChunkCache(
        tmp_path / "cache",
        dependencies={"processor": "revision-1"},
        expected_chunk_ids=expected,
    )
    first_run.write_chunk("part-1", b"output-1")
    with pytest.raises(CacheIntegrityError):
        first_run.verify_complete()

    first_run.write_chunk("part-2", b"output-2")
    assert first_run.verify_complete()

    rerun = ResumableChunkCache(
        tmp_path / "cache",
        dependencies={"processor": "revision-1"},
        expected_chunk_ids=expected,
    )
    assert rerun.resume() == ()
    assert rerun.read_chunk("part-1") == b"output-1"
    assert rerun.read_chunk("part-2") == b"output-2"


def test_unexpected_chunk_id_cannot_be_written(tmp_path) -> None:
    cache = ResumableChunkCache(
        tmp_path / "cache", dependencies={"source": "v1"}, expected_chunk_ids=["expected"]
    )
    with pytest.raises(CacheIntegrityError):
        cache.write_chunk("extra", b"unexpected")


def test_completeness_check_rejects_orphan_extra_chunk_file(tmp_path) -> None:
    cache = ResumableChunkCache(
        tmp_path / "cache", dependencies={"source": "v1"}, expected_chunk_ids=["expected"]
    )
    cache.write_chunk("expected", b"complete")
    token = hashlib.sha256(b"extra").hexdigest()
    (cache.root / f"{token}.chunk").write_bytes(b"orphan")

    with pytest.raises(CacheIntegrityError):
        cache.verify_complete()
