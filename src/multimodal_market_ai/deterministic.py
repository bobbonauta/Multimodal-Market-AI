"""Simple building blocks for a public deterministic multi-signal model."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd


class DeterministicModelError(ValueError):
    """Raised when deterministic signal inputs are invalid."""


def combine_directional_signals(
    frame: pd.DataFrame,
    signal_columns: Sequence[str],
    *,
    policy: str = "majority",
    weights: Mapping[str, float] | None = None,
    minimum_active: int = 1,
    weighted_threshold: float = 0.5,
    prefix: str = "det_",
) -> pd.DataFrame:
    """Combine simple directional signals into one deterministic decision.

    Each input signal must contain only:

    - ``+1``: this rule points up / positive;
    - ``-1``: this rule points down / negative;
    - ``0``: this rule has no opinion for this row.

    The ``0`` value is only a public helper convention meaning "no opinion from
    this rule". It does not define a market regime or a private trading state.

    Supported policies:

    - ``majority``: the side with more active votes wins;
    - ``unanimous``: all active votes must point the same way;
    - ``weighted``: stronger rules can receive larger weights.

    The original frame is never changed. The returned copy adds three columns:
    ``<prefix>score``, ``<prefix>active_signals`` and ``<prefix>signal``.
    """
    if not isinstance(frame, pd.DataFrame):
        raise DeterministicModelError("frame must be a pandas DataFrame")
    if not signal_columns:
        raise DeterministicModelError("at least one signal column is required")
    if len(signal_columns) != len(set(signal_columns)):
        raise DeterministicModelError("signal columns must be unique")
    if minimum_active < 1:
        raise DeterministicModelError("minimum_active must be at least 1")
    if policy not in {"majority", "unanimous", "weighted"}:
        raise DeterministicModelError(
            "policy must be one of: majority, unanimous, weighted"
        )
    if not 0 <= weighted_threshold <= 1:
        raise DeterministicModelError("weighted_threshold must be between 0 and 1")

    missing = [column for column in signal_columns if column not in frame.columns]
    if missing:
        raise DeterministicModelError(f"signal columns are missing: {missing}")

    numeric = frame.loc[:, list(signal_columns)].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        raise DeterministicModelError("signal columns must contain numeric values")

    allowed = numeric.isin([-1, 0, 1])
    if not allowed.all().all():
        raise DeterministicModelError("signals must contain only -1, 0 or +1")

    resolved_weights = {column: 1.0 for column in signal_columns}
    if weights is not None:
        unknown = [column for column in weights if column not in signal_columns]
        if unknown:
            raise DeterministicModelError(f"weights reference unknown signals: {unknown}")
        for column, weight in weights.items():
            value = float(weight)
            if not np.isfinite(value) or value <= 0:
                raise DeterministicModelError("signal weights must be finite and positive")
            resolved_weights[column] = value

    weight_series = pd.Series(resolved_weights, dtype=float)
    active = numeric.ne(0)
    active_count = active.sum(axis=1).astype(int)

    weighted_sum = numeric.mul(weight_series, axis=1).sum(axis=1)
    active_weight = active.mul(weight_series, axis=1).sum(axis=1)
    score = weighted_sum.div(active_weight.where(active_weight.ne(0), 1.0))
    score = score.where(active_weight.ne(0), 0.0)

    decision = pd.Series(0, index=frame.index, dtype=int)
    enough = active_count.ge(minimum_active)

    if policy == "majority":
        vote_sum = numeric.sum(axis=1)
        decision.loc[enough & vote_sum.gt(0)] = 1
        decision.loc[enough & vote_sum.lt(0)] = -1
    elif policy == "unanimous":
        positive = numeric.eq(1).sum(axis=1)
        negative = numeric.eq(-1).sum(axis=1)
        decision.loc[enough & positive.eq(active_count)] = 1
        decision.loc[enough & negative.eq(active_count)] = -1
    else:
        decision.loc[enough & score.ge(weighted_threshold)] = 1
        decision.loc[enough & score.le(-weighted_threshold)] = -1

    out = frame.copy()
    out[f"{prefix}score"] = score.astype(float)
    out[f"{prefix}active_signals"] = active_count
    out[f"{prefix}signal"] = decision
    return out
