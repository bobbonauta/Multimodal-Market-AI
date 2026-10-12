# Synthetic multimodal demo

This is the fastest way to understand Multimodal Market AI.

It uses only **fake market data** and runs on a CPU. No broker, API key, GPU or model download is
needed.

## What happens

```text
1. generate 90 synthetic OHLCV bars
2. pick three decision times
3. calculate three simple deterministic signals
4. render one SVG chart for each decision time
5. calculate one mock visual signal from the visible history
6. join everything into a fusion table
7. produce LONG / WAIT / SHORT teaching decisions
```

The visual signal is deliberately a **mock adapter**. It is not called AI and it does not pretend
to interpret the SVG file. It represents the interface that a real VLM can later fill.

## Run everything

From the repository root:

```bash
python examples/synthetic_multimodal/run_demo.py
```

Expected final decisions:

```text
case_001 -> LONG
case_002 -> WAIT
case_003 -> SHORT
```

Generated files are written to `examples/synthetic_multimodal/output/`.

## Run the steps separately

```bash
python examples/synthetic_multimodal/generate_data.py
python examples/synthetic_multimodal/render_charts.py
python examples/synthetic_multimodal/build_fusion_table.py
```

## Why the demo is causal

For every case, features are calculated only from rows at or before `decision_ts`.

The fusion table contains both:

- `decision_ts`;
- `source_end_ts`.

The test suite checks that `source_end_ts <= decision_ts`.

Future bars may exist in the synthetic file, but the case builder slices the data at the decision
row before calculating the features.

## Replace the pieces

You can replace:

```text
trend_signal       -> your own deterministic rule
momentum_signal    -> another indicator or model
structure_signal   -> your own structure logic
mock_visual_score  -> output from a real VLM
decision rule      -> classifier / policy / scoring model
```

The rest of the pipeline can remain unchanged.

## Why SVG?

The demo renders line-chart SVG files with pure Python. This keeps the first run light:

- no matplotlib dependency;
- no GPU;
- images display directly on GitHub;
- the same files can be regenerated exactly.

A future public renderer can support richer charts without changing the fusion contract.
