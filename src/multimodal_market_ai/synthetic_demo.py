"""CPU-only synthetic multimodal demo used by the public examples."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

from .deterministic import combine_directional_signals

CASE_ROWS = (29, 59, 89)


def generate_synthetic_market() -> pd.DataFrame:
    """Create a small deterministic OHLCV series with no external data."""
    timestamps = pd.date_range(
        "2026-01-01T00:00:00Z",
        periods=90,
        freq="h",
    )
    closes: list[float] = []
    price = 100.0

    for row in range(90):
        if row < 30:
            delta = 0.18 + 0.04 * math.sin(row / 2)
        elif row < 60:
            delta = 0.22 if row % 2 == 0 else -0.20
            if row >= 54:
                delta = -0.08 if row % 2 == 0 else 0.05
        else:
            delta = -0.17 + 0.04 * math.sin(row / 2)

        price += delta
        closes.append(round(price, 4))

    close = np.asarray(closes, dtype=float)
    open_ = np.concatenate(([100.0], close[:-1]))
    high = np.maximum(open_, close) + 0.12
    low = np.minimum(open_, close) - 0.12
    volume = 1_000 + np.arange(90) * 3

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )


def _direction(value: float, threshold: float) -> int:
    if value > threshold:
        return 1
    if value < -threshold:
        return -1
    return 0


def build_fusion_table(market: pd.DataFrame) -> pd.DataFrame:
    """Build three causal teaching cases and fuse deterministic + mock visual clues."""
    rows: list[dict[str, object]] = []

    for case_number, row_index in enumerate(CASE_ROWS, start=1):
        history = market.iloc[: row_index + 1]
        close = history["close"]
        last_close = float(close.iloc[-1])

        sma5 = float(close.tail(5).mean())
        trend_signal = _direction(last_close - sma5, 0.03)

        momentum_delta = float(last_close - close.iloc[-4])
        momentum_signal = _direction(momentum_delta, 0.05)

        recent = history.tail(10)
        midpoint = (float(recent["high"].max()) + float(recent["low"].min())) / 2
        structure_signal = _direction(last_close - midpoint, 0.05)

        visual_score = float(
            (last_close - float(close.iloc[-12])) / abs(float(close.iloc[-12]))
        )
        visual_signal = _direction(visual_score, 0.003)

        decision_ts = pd.Timestamp(history["timestamp"].iloc[-1])
        rows.append(
            {
                "case_id": f"case_{case_number:03d}",
                "decision_ts": decision_ts,
                "source_end_ts": decision_ts,
                "trend_signal": trend_signal,
                "momentum_signal": momentum_signal,
                "structure_signal": structure_signal,
                "mock_visual_score": round(visual_score, 6),
                "visual_signal": visual_signal,
                "image_path": f"images/case_{case_number:03d}.svg",
            }
        )

    frame = pd.DataFrame(rows)
    combined = combine_directional_signals(
        frame,
        ["trend_signal", "momentum_signal", "structure_signal"],
        policy="majority",
    )

    decisions: list[str] = []
    for det_signal, visual_signal in zip(
        combined["det_signal"],
        combined["visual_signal"],
        strict=True,
    ):
        if det_signal == 1 and visual_signal == 1:
            decisions.append("LONG")
        elif det_signal == -1 and visual_signal == -1:
            decisions.append("SHORT")
        else:
            decisions.append("WAIT")

    combined["decision"] = decisions
    return combined


def _svg_chart(window: pd.DataFrame, title: str) -> str:
    width = 640
    height = 320
    left = 44
    right = 18
    top = 38
    bottom = 34
    plot_width = width - left - right
    plot_height = height - top - bottom

    closes = window["close"].astype(float)
    min_price = float(window["low"].min())
    max_price = float(window["high"].max())
    span = max(max_price - min_price, 1e-9)
    step = plot_width / max(len(window) - 1, 1)

    def y(price: float) -> float:
        return top + (max_price - price) / span * plot_height

    points = " ".join(
        f"{left + position * step:.2f},{y(float(price)):.2f}"
        for position, price in enumerate(closes)
    )

    grid = "\n".join(
        (
            f'<line x1="{left}" y1="{top + plot_height * row / 4:.2f}" '
            f'x2="{width-right}" y2="{top + plot_height * row / 4:.2f}" '
            'stroke="#dddddd" stroke-width="1"/>'
        )
        for row in range(5)
    )

    return "\n".join(
        [
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                f'viewBox="0 0 {width} {height}">'
            ),
            '<rect width="100%" height="100%" fill="white"/>',
            (
                f'<text x="{left}" y="24" font-family="sans-serif" '
                f'font-size="16">{title}</text>'
            ),
            grid,
            (
                f'<polyline points="{points}" fill="none" stroke="#222222" '
                'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
            ),
            (
                f'<text x="{left}" y="{height-10}" font-family="sans-serif" '
                'font-size="11">Synthetic data — generated locally, no real market source</text>'
            ),
            "</svg>",
        ]
    )


def render_charts(
    market: pd.DataFrame,
    output_dir: str | Path,
) -> list[Path]:
    """Render three strategy-agnostic SVG chart images using only the standard library."""
    image_dir = Path(output_dir)
    image_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    for case_number, row_index in enumerate(CASE_ROWS, start=1):
        start = max(0, row_index - 19)
        window = market.iloc[start : row_index + 1]
        path = image_dir / f"case_{case_number:03d}.svg"
        path.write_text(
            _svg_chart(window, f"Synthetic case {case_number}"),
            encoding="utf-8",
        )
        paths.append(path)

    return paths


def write_demo(output_dir: str | Path) -> pd.DataFrame:
    """Generate data, images and a fusion table in one reproducible CPU-only run."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    market = generate_synthetic_market()
    fusion = build_fusion_table(market)

    market.to_csv(destination / "market.csv", index=False)
    render_charts(market, destination / "images")
    fusion.to_csv(destination / "fusion_table.csv", index=False)

    return fusion
