from __future__ import annotations

import pandas as pd
import pytest

from multimodal_market_ai.integration import (
    IntegrationError,
    attach_causal_market_context,
    validate_bot_events,
)


def _bars() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100.0, 101.0, 102.0],
            "high": [102.0, 103.0, 104.0],
            "low": [99.0, 100.0, 101.0],
            "close": [101.0, 102.0, 103.0],
        },
        index=pd.to_datetime(
            [
                "2026-01-01T10:05:00Z",
                "2026-01-01T10:10:00Z",
                "2026-01-01T10:15:00Z",
            ]
        ),
    )


def test_attach_causal_market_context_uses_latest_closed_bar() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["a", "b"],
            "decision_ts": ["2026-01-01T10:07:00Z", "2026-01-01T10:10:00Z"],
            "private_state": [7, 9],
        }
    )

    joined = attach_causal_market_context(events, _bars())

    assert joined["market_close_ts"].tolist() == [
        pd.Timestamp("2026-01-01T10:05:00Z"),
        pd.Timestamp("2026-01-01T10:10:00Z"),
    ]
    assert joined["market_close"].tolist() == [101.0, 102.0]
    assert joined["private_state"].tolist() == [7, 9]


def test_future_bar_is_never_attached() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["a"],
            "decision_ts": ["2026-01-01T10:14:59Z"],
        }
    )

    joined = attach_causal_market_context(events, _bars())
    assert joined.loc[0, "market_close_ts"] == pd.Timestamp("2026-01-01T10:10:00Z")
    assert joined.loc[0, "market_close"] == 102.0


def test_event_before_first_bar_keeps_event_and_has_no_context() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["a"],
            "decision_ts": ["2026-01-01T10:01:00Z"],
            "private_state": [3.5],
        }
    )

    joined = attach_causal_market_context(events, _bars())
    assert len(joined) == 1
    assert joined.loc[0, "private_state"] == 3.5
    assert pd.isna(joined.loc[0, "market_close_ts"])


def test_duplicate_event_ids_are_rejected() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["a", "a"],
            "decision_ts": ["2026-01-01T10:01:00Z", "2026-01-01T10:02:00Z"],
        }
    )

    with pytest.raises(IntegrationError, match="unique"):
        validate_bot_events(events)


def test_required_private_state_is_validated_but_not_interpreted() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["a"],
            "decision_ts": ["2026-01-01T10:07:00Z"],
            "opaque_strategy_value": [123.456],
        }
    )

    joined = attach_causal_market_context(
        events,
        _bars(),
        required_state_columns=["opaque_strategy_value"],
    )
    assert joined.loc[0, "opaque_strategy_value"] == 123.456


def test_context_column_collision_fails_closed() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["a"],
            "decision_ts": ["2026-01-01T10:07:00Z"],
            "market_close": [999.0],
        }
    )

    with pytest.raises(IntegrationError, match="collide"):
        attach_causal_market_context(events, _bars())
