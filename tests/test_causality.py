import pandas as pd
import pytest

from multimodal_market_ai.audit import CausalityError, assert_causal_alignment
from multimodal_market_ai.timeframes import (
    align_closed_higher_timeframe,
    resample_ohlcv_close_indexed,
)


def _m5_frame() -> pd.DataFrame:
    index = pd.date_range("2026-01-01 00:05", periods=12, freq="5min", tz="UTC")
    values = list(range(12))
    return pd.DataFrame(
        {
            "open": [1.00 + i * 0.001 for i in values],
            "high": [1.01 + i * 0.001 for i in values],
            "low": [0.99 + i * 0.001 for i in values],
            "close": [1.005 + i * 0.001 for i in values],
            "volume": [10 + i for i in values],
        },
        index=index,
    )


def test_backward_alignment_never_uses_future_htf_bar() -> None:
    base = _m5_frame()
    higher = resample_ohlcv_close_indexed(base, "15min")
    aligned = align_closed_higher_timeframe(base, higher)

    visible = aligned["htf_close_ts"].dropna()
    decisions = aligned.loc[visible.index].index
    assert (visible.to_numpy() <= decisions.to_numpy()).all()


def test_exact_close_can_see_exact_higher_timeframe_close() -> None:
    base = _m5_frame()
    higher = resample_ohlcv_close_indexed(base, "15min")
    aligned = align_closed_higher_timeframe(base, higher)

    decision = pd.Timestamp("2026-01-01 00:15", tz="UTC")
    assert aligned.loc[decision, "htf_close_ts"] == decision


def test_future_context_is_rejected() -> None:
    decision = pd.Series(pd.to_datetime(["2026-01-01 10:00Z"]))
    context = pd.Series(pd.to_datetime(["2026-01-01 10:05Z"]))
    with pytest.raises(CausalityError):
        assert_causal_alignment(decision, context)
