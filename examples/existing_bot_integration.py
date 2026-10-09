"""Small example: attach causal market context to events from an existing bot."""

from __future__ import annotations

import pandas as pd

from multimodal_market_ai.integration import attach_causal_market_context


def main() -> None:
    events = pd.DataFrame(
        {
            "event_id": ["evt-001", "evt-002", "evt-003"],
            "decision_ts": [
                "2026-01-01T10:07:00Z",
                "2026-01-01T10:10:00Z",
                "2026-01-01T10:14:00Z",
            ],
            "symbol": ["SYNTH", "SYNTH", "SYNTH"],
            "system_score": [0.25, 0.62, 0.41],
            "private_state_example": [1.2, 1.7, 1.4],
        }
    )

    bars = pd.DataFrame(
        {
            "open": [100.0, 101.0, 102.0],
            "high": [102.0, 103.0, 104.0],
            "low": [99.0, 100.0, 101.0],
            "close": [101.0, 102.0, 103.0],
            "volume": [10.0, 12.0, 11.0],
        },
        index=pd.to_datetime(
            [
                "2026-01-01T10:05:00Z",
                "2026-01-01T10:10:00Z",
                "2026-01-01T10:15:00Z",
            ]
        ),
    )

    joined = attach_causal_market_context(events, bars)
    columns = [
        "event_id",
        "decision_ts",
        "system_score",
        "market_close_ts",
        "market_close",
    ]
    print(joined[columns].to_string(index=False))


if __name__ == "__main__":
    main()
