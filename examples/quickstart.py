from __future__ import annotations

import pandas as pd

from multimodal_market_ai.metrics import evaluate_r_multiples
from multimodal_market_ai.timeframes import (
    align_closed_higher_timeframe,
    resample_ohlcv_close_indexed,
)


index = pd.date_range("2026-01-01 00:05", periods=24, freq="5min", tz="UTC")
base = pd.DataFrame(
    {
        "open": [1.1000 + i * 0.0001 for i in range(len(index))],
        "high": [1.1008 + i * 0.0001 for i in range(len(index))],
        "low": [1.0995 + i * 0.0001 for i in range(len(index))],
        "close": [1.1003 + i * 0.0001 for i in range(len(index))],
        "volume": [100 + i for i in range(len(index))],
    },
    index=index,
)

higher = resample_ohlcv_close_indexed(base, "15min")
aligned = align_closed_higher_timeframe(base, higher, prefix="m15_")

print("Causal M5 -> M15 alignment")
print(aligned[["close", "m15_close_ts", "m15_close"]].tail(8))

print("\nExample asymmetric R distribution")
metrics = evaluate_r_multiples([2.0] * 49 + [-1.0] * 51)
for key, value in metrics.items():
    print(f"{key}: {value}")
