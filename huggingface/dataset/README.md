---
license: apache-2.0
pretty_name: Multimodal Market AI Synthetic Demo
size_categories:
- n<1K
tags:
- finance
- synthetic
- multimodal
- time-series
- causal-inference
---

# Multimodal Market AI — synthetic demo dataset

A tiny, fully synthetic dataset for demonstrating the public Multimodal Market AI workflow.
Everything in it is fake and is regenerated from the open-source code.

No real market record, proprietary strategy rule or private feature is included.

## What it contains

| File | Rows | What it is |
|---|---|---|
| `market.csv` | 90 | fake hourly OHLCV bars |
| `fusion_table.csv` | 3 | one row per decision time: deterministic signals, a mock visual feature and the final decision |
| `images/case_001.svg`, `case_002.svg`, `case_003.svg` | 3 | the synthetic chart image of each decision |

The three decisions are teaching examples: one `LONG`, one `WAIT`, one `SHORT`.

## Schema

`market.csv`

| Column | Meaning |
|---|---|
| `timestamp` | bar time, UTC, hourly from 2026-01-01 |
| `open`, `high`, `low`, `close` | fake prices |
| `volume` | fake volume |

`fusion_table.csv`

| Column | Meaning |
|---|---|
| `case_id` | `case_001` to `case_003` |
| `decision_ts`, `source_end_ts` | decision time, and the last bar the inputs were allowed to use (the same here) |
| `trend_signal`, `momentum_signal`, `structure_signal` | three simple deterministic signals: `+1`, `-1` or `0` (no opinion) |
| `mock_visual_score`, `visual_signal` | the mock visual feature and its direction (`+1`, `-1`, `0`) |
| `image_path` | the chart image of that case, relative to the dataset root |
| `det_score`, `det_active_signals`, `det_signal` | the majority combination of the three deterministic signals |
| `decision` | `LONG`, `WAIT` or `SHORT` |

## How it is generated

`market.csv` is a fixed formula, not a random draw, so every run gives the same file. The three
decision times are fixed bars of that series. Each signal only looks at bars up to its decision
time; no future bar is used as an input. The final decision is `LONG` or `SHORT` only when the
deterministic result and the mock visual signal agree; otherwise it is `WAIT`.

To regenerate it:

```bash
git clone https://github.com/bobbonauta/Multimodal-Market-AI
cd Multimodal-Market-AI
pip install -e .
python examples/synthetic_multimodal/run_demo.py
```

## Limits

- Only 90 bars and 3 decisions: it shows the data contract, not statistics.
- The prices are invented. They say nothing about any real market.
- The visual feature is a deliberately simple mock. It does not read the chart image, and it is not
  a model.
- This is an educational engineering dataset. It is not a trading dataset and not evidence of
  profitability. Do not train or evaluate a trading system on it.

## License

Apache-2.0, the same as the code.

## Source

The canonical source, the full project description and the code that generates this dataset are on
GitHub: `https://github.com/bobbonauta/Multimodal-Market-AI`
