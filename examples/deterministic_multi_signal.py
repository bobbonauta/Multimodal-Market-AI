"""Small example: build a deterministic multi-signal model from invented prices."""

from __future__ import annotations

import numpy as np
import pandas as pd

from multimodal_market_ai.deterministic import combine_directional_signals


# 1. Invent a tiny price series. These are not real market prices.
frame = pd.DataFrame(
    {
        "close": [100.0, 101.0, 102.0, 101.5, 103.0, 104.0, 103.5, 105.0],
    }
)

# 2. Create three simple, replaceable rules.
# Rule A: price above its recent 3-row average points up, otherwise down.
recent_average = frame["close"].rolling(3, min_periods=1).mean()
frame["trend_signal"] = np.where(frame["close"] >= recent_average, 1, -1)

# Rule B: rising from the previous row points up, falling points down.
change = frame["close"].diff()
frame["momentum_signal"] = np.select(
    [change > 0, change < 0],
    [1, -1],
    default=0,
)

# Rule C: price above the recent 4-row midpoint points up, otherwise down.
recent_high = frame["close"].rolling(4, min_periods=1).max()
recent_low = frame["close"].rolling(4, min_periods=1).min()
midpoint = (recent_high + recent_low) / 2
frame["structure_signal"] = np.where(frame["close"] >= midpoint, 1, -1)

# 3. Let the majority decide. You can replace any of the three rules above.
result = combine_directional_signals(
    frame,
    ["trend_signal", "momentum_signal", "structure_signal"],
    policy="majority",
)

print(
    result[
        [
            "close",
            "trend_signal",
            "momentum_signal",
            "structure_signal",
            "det_score",
            "det_active_signals",
            "det_signal",
        ]
    ]
)
