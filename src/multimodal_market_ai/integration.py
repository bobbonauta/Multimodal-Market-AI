"""Generic adapters for connecting timestamped events from an existing trading system."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from .audit import CausalityError, assert_causal_alignment

_REQUIRED_OHLC = ("open", "high", "low", "close")


class IntegrationError(ValueError):
    """Raised when external bot events cannot be integrated safely."""


def validate_bot_events(
    events: pd.DataFrame,
    *,
    event_id_column: str = "event_id",
    decision_ts_column: str = "decision_ts",
    required_state_columns: Sequence[str] = (),
) -> pd.DataFrame:
    """Return a normalized copy of timestamped bot events.

    The adapter intentionally does not interpret the strategy-owned columns. It only
    validates stable identity and the timestamp at which each event became available.
    """
    if not isinstance(events, pd.DataFrame):
        raise IntegrationError("events must be a pandas DataFrame")
    required = [event_id_column, decision_ts_column, *required_state_columns]
    missing = [column for column in required if column not in events.columns]
    if missing:
        raise IntegrationError(f"events are missing required columns: {missing}")

    out = events.copy()
    identifiers = out[event_id_column]
    if identifiers.isna().any():
        raise IntegrationError("event IDs must not be missing")
    if identifiers.astype(str).str.len().eq(0).any():
        raise IntegrationError("event IDs must not be empty")
    if identifiers.duplicated().any():
        raise IntegrationError("event IDs must be unique")

    decision = pd.to_datetime(out[decision_ts_column], utc=True, errors="coerce")
    if decision.isna().any():
        raise IntegrationError("decision timestamps contain missing or invalid values")
    out[decision_ts_column] = decision
    return out


def _validate_closed_bars(bars: pd.DataFrame) -> None:
    if not isinstance(bars, pd.DataFrame):
        raise IntegrationError("bars must be a pandas DataFrame")
    if not isinstance(bars.index, pd.DatetimeIndex):
        raise IntegrationError("bars must use a pandas DatetimeIndex of close timestamps")
    if bars.index.tz is None:
        raise IntegrationError("bar close timestamps must be timezone-aware")
    if not bars.index.is_monotonic_increasing:
        raise IntegrationError("bar close timestamps must be sorted ascending")
    if bars.index.has_duplicates:
        raise IntegrationError("bar close timestamps must be unique")
    missing = [column for column in _REQUIRED_OHLC if column not in bars.columns]
    if missing:
        raise IntegrationError(f"bars are missing OHLC columns: {missing}")


def attach_causal_market_context(
    events: pd.DataFrame,
    bars: pd.DataFrame,
    *,
    event_id_column: str = "event_id",
    decision_ts_column: str = "decision_ts",
    required_state_columns: Sequence[str] = (),
    prefix: str = "market_",
) -> pd.DataFrame:
    """Attach the latest closed market bar to each event emitted by an existing bot.

    `bars.index` is interpreted as bar close time. Alignment is strictly backward:
    an event can see a bar only when that bar's close timestamp is <= the event's
    decision timestamp. Strategy-owned columns are preserved without interpretation.

    This helper intentionally handles one market series per call. Multi-symbol systems
    should group their events by symbol and join each group to the corresponding bars.
    """
    normalized = validate_bot_events(
        events,
        event_id_column=event_id_column,
        decision_ts_column=decision_ts_column,
        required_state_columns=required_state_columns,
    )
    _validate_closed_bars(bars)

    context_ts_column = f"{prefix}close_ts"
    context_columns = [context_ts_column, *(f"{prefix}{column}" for column in bars.columns)]
    collisions = [column for column in context_columns if column in normalized.columns]
    if collisions:
        raise IntegrationError(f"context column names collide with event columns: {collisions}")

    left = normalized.copy()
    left["__integration_order"] = range(len(left))
    right = bars.copy().reset_index()
    right = right.rename(columns={right.columns[0]: context_ts_column})
    right = right.rename(columns={column: f"{prefix}{column}" for column in bars.columns})

    joined = pd.merge_asof(
        left.sort_values(decision_ts_column),
        right.sort_values(context_ts_column),
        left_on=decision_ts_column,
        right_on=context_ts_column,
        direction="backward",
        allow_exact_matches=True,
    )

    try:
        assert_causal_alignment(joined[decision_ts_column], joined[context_ts_column])
    except CausalityError as exc:
        raise IntegrationError(str(exc)) from exc

    if len(joined) != len(normalized):
        raise IntegrationError("integration changed the number of bot events")
    if set(joined[event_id_column]) != set(normalized[event_id_column]):
        raise IntegrationError("integration changed the event-ID set")

    joined = joined.sort_values("__integration_order").drop(columns="__integration_order")
    joined.index = normalized.index
    return joined
