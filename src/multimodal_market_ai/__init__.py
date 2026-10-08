"""Multimodal Market AI public core."""

from .audit import CausalityError, assert_causal_alignment, audit_causal_features
from .cache import CacheIntegrityError, ResumableChunkCache, atomic_write_bytes
from .metrics import evaluate_r_multiples
from .provenance import (
    ArtifactSealError,
    RecordIDMismatchError,
    compare_record_ids,
    dependency_fingerprint,
    exact_one_to_one_join,
    seal_artifact,
    verify_artifact_seal,
)
from .splits import (
    TemporalSplit,
    TemporalSplitError,
    apply_numeric_statistics,
    fit_numeric_statistics,
    purged_temporal_split,
)
from .state import MarketState
from .timeframes import align_closed_higher_timeframe, resample_ohlcv_close_indexed

__all__ = [
    "ArtifactSealError",
    "CacheIntegrityError",
    "CausalityError",
    "MarketState",
    "RecordIDMismatchError",
    "ResumableChunkCache",
    "TemporalSplit",
    "TemporalSplitError",
    "align_closed_higher_timeframe",
    "apply_numeric_statistics",
    "assert_causal_alignment",
    "atomic_write_bytes",
    "audit_causal_features",
    "compare_record_ids",
    "dependency_fingerprint",
    "evaluate_r_multiples",
    "exact_one_to_one_join",
    "fit_numeric_statistics",
    "purged_temporal_split",
    "resample_ohlcv_close_indexed",
    "seal_artifact",
    "verify_artifact_seal",
]

__version__ = "0.1.0a0"
