"""Typed intermediate state shared by numerical and multimodal components."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class MarketState:
    """Strategy-agnostic market state at one causal decision timestamp."""

    symbol: str
    decision_ts: datetime
    lane: str
    numerical: dict[str, Any] = field(default_factory=dict)
    visual: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("symbol cannot be empty")
        if not self.lane.strip():
            raise ValueError("lane cannot be empty")
        if self.decision_ts.tzinfo is None or self.decision_ts.utcoffset() is None:
            raise ValueError("decision_ts must be timezone-aware")

    def as_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "decision_ts": self.decision_ts.isoformat(),
            "lane": self.lane,
            "numerical": self.numerical,
            "visual": self.visual,
            "metadata": self.metadata,
        }
