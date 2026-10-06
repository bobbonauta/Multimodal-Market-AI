"""Causality checks used across the project."""

from __future__ import annotations

import pandas as pd


class CausalityError(ValueError):
    """Raised when an input contains information unavailable at decision time."""


def assert_causal_alignment(decision_ts: pd.Series, context_ts: pd.Series) -> None:
    """Ensure every non-null context timestamp is <= its decision timestamp."""
    decision = pd.to_datetime(decision_ts, utc=True)
    context = pd.to_datetime(context_ts, utc=True)
    invalid = context.notna() & (context > decision)
    if invalid.any():
        first = int(invalid.to_numpy().nonzero()[0][0])
        raise CausalityError(
            f"future context detected at row {first}: "
            f"context={context.iloc[first]!s} decision={decision.iloc[first]!s}"
        )
