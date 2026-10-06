"""Causal helpers for close-timestamped OHLCV data."""

from __future__ import annotations

import pandas as pd

from .audit import assert_causal_alignment

_REQUIRED = ("open", "high", "low", "close")


def _validate_close_indexed(frame: pd.DataFrame, name: str) -> None:
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise TypeError(f"{name} must use a pandas DatetimeIndex")
    if frame.index.tz is None:
        raise ValueError(f"{name} timestamps must be timezone-aware")
    if not frame.index.is_monotonic_increasing:
        raise ValueError(f"{name} timestamps must be sorted ascending")
    if frame.index.has_duplicates:
        raise ValueError(f"{name} timestamps must be unique")
    missing = [column for column in _REQUIRED if column not in frame.columns]
    if missing:
        raise ValueError(f"{name} is missing OHLC columns: {missing}")


def resample_ohlcv_close_indexed(frame: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Aggregate close-timestamped bars to a higher timeframe.

    Resampled rows are labelled with the higher-timeframe close timestamp.
    Consumers must still align them causally: a row labelled 10:00 cannot be
    used by a decision made at 09:59.
    """
    _validate_close_indexed(frame, "frame")

    agg: dict[str, str] = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
    }
    if "volume" in frame.columns:
        agg["volume"] = "sum"

    out = frame.resample(rule, label="right", closed="right").agg(agg)
    out = out.dropna(subset=list(_REQUIRED))
    out.index.name = frame.index.name or "close_ts"
    return out


def align_closed_higher_timeframe(
    base: pd.DataFrame,
    higher: pd.DataFrame,
    *,
    prefix: str = "htf_",
) -> pd.DataFrame:
    """Attach the most recent *closed* higher-timeframe row to each base row.

    Alignment is backward-only and exact timestamp matches are allowed. The
    resulting ``<prefix>close_ts`` column records which higher-timeframe close
    was visible at each base decision timestamp.
    """
    _validate_close_indexed(base, "base")
    _validate_close_indexed(higher, "higher")

    base_name = base.index.name or "decision_ts"
    left = base.copy().reset_index()
    left = left.rename(columns={left.columns[0]: "decision_ts"})

    right = higher.copy().reset_index()
    right = right.rename(columns={right.columns[0]: f"{prefix}close_ts"})
    rename = {
        column: f"{prefix}{column}"
        for column in higher.columns
        if column != f"{prefix}close_ts"
    }
    right = right.rename(columns=rename)

    merged = pd.merge_asof(
        left.sort_values("decision_ts"),
        right.sort_values(f"{prefix}close_ts"),
        left_on="decision_ts",
        right_on=f"{prefix}close_ts",
        direction="backward",
        allow_exact_matches=True,
    )

    assert_causal_alignment(merged["decision_ts"], merged[f"{prefix}close_ts"])
    merged = merged.set_index("decision_ts")
    merged.index.name = base_name
    return merged
