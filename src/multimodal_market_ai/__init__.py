"""Multimodal Market AI public core."""

from .audit import CausalityError, assert_causal_alignment
from .metrics import evaluate_r_multiples
from .state import MarketState
from .timeframes import align_closed_higher_timeframe, resample_ohlcv_close_indexed

__all__ = [
    "CausalityError",
    "MarketState",
    "align_closed_higher_timeframe",
    "assert_causal_alignment",
    "evaluate_r_multiples",
    "resample_ohlcv_close_indexed",
]

__version__ = "0.1.0a0"
