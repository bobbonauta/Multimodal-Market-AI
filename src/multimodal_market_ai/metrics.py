"""Economic metrics for return series expressed in risk units (R)."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np


def evaluate_r_multiples(values: Iterable[float]) -> dict[str, float | int]:
    """Evaluate a sequence of trade outcomes expressed in R multiples.

    ``+2`` means a gain of twice the initial risk unit and ``-1`` means a full
    one-risk-unit loss. No assumption is made that wins and losses are
    symmetric.
    """
    r = np.asarray(list(values), dtype=float)
    if r.size == 0:
        raise ValueError("at least one R-multiple is required")
    if not np.isfinite(r).all():
        raise ValueError("R-multiples must all be finite")

    wins = r[r > 0]
    losses = r[r < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(-losses.sum())
    profit_factor = float("inf") if gross_loss == 0 else gross_profit / gross_loss

    equity = np.cumsum(r)
    running_peak = np.maximum.accumulate(np.concatenate(([0.0], equity)))
    equity_with_origin = np.concatenate(([0.0], equity))
    drawdown = running_peak - equity_with_origin

    return {
        "n": int(r.size),
        "win_rate": float((r > 0).mean()),
        "loss_rate": float((r < 0).mean()),
        "expectancy_r": float(r.mean()),
        "avg_win_r": float(wins.mean()) if wins.size else 0.0,
        "avg_loss_r": float(losses.mean()) if losses.size else 0.0,
        "gross_profit_r": gross_profit,
        "gross_loss_r": gross_loss,
        "profit_factor": profit_factor,
        "sum_r": float(r.sum()),
        "max_drawdown_r": float(drawdown.max()),
    }
