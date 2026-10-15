# Project status — simple version

Multimodal Market AI is **early alpha**, but the public project can now be understood and executed
without private data or a GPU.

## Operational pipeline

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

This is the main operational path.

Training, VLM experiments, model arenas, caches and audits are supporting research tools around
that path. They are not separate mandatory pipelines.

## Public building blocks that exist now

- causal market-data alignment;
- higher-timeframe construction without using future bars;
- feature-availability checks;
- deterministic multi-signal combiner;
- existing-bot event adapter;
- train/validation/test split helpers;
- hashes, seals and exact record-ID checks;
- resumable-cache primitives;
- deterministic freeze/replay documentation;
- CPU-only synthetic multimodal demo;
- three generated synthetic chart images;
- deterministic + mock-visual fusion table;
- `LONG / WAIT / SHORT` teaching decisions;
- published aggregate results from adapter-training and large-sample visual arenas;
- Hugging Face dataset/Space export package.

## What the synthetic demo proves

A new user can clone the repository and run:

```bash
python examples/synthetic_multimodal/run_demo.py
```

without:

- broker credentials;
- real market data;
- CUDA;
- a large VLM;
- private strategy rules.

The demo generates fake OHLCV, renders charts, calculates replaceable deterministic signals,
adds a mock visual feature and creates one fusion table.

It is a wiring/contract example, not a trading strategy.

## Model-research status

The public repository now includes aggregate, public-safe results from two distinct multimodal
experiments.

### Adapter-training arena

The controlled fine-tuning arena reports final holdout macro-F1 after validation-only checkpoint
selection. It showed that:

- model size did not rank model quality;
- some adapters improved strongly;
- some adapters made the model worse;
- a good mean can hide a failed subtask;
- real job time matters when choosing GPU hardware;
- negative results are useful engineering evidence.

See [MODEL_ARENA_RESULTS.md](MODEL_ARENA_RESULTS.md).

### Large-sample visual arena — October 2026

A second experiment evaluated **5 open VLM configurations × 1,000 frozen cases**, producing
**5,000/5,000 valid outputs** across two 500-case tranches per model.

The public report shows aggregate agreement, 95% confidence intervals, internal consistency and
measured throughput. The deterministic comparison is explicitly treated as a reference anchor,
not ground truth. Private task meanings, cases, strategy rules and model artifacts remain closed.

The two tranches produced closely aligned aggregate behaviour and an independent recomputation of
all 5,000 outputs found zero discrepancies in the published aggregate statistics.

See [LARGE_SAMPLE_VISUAL_ARENA_2026_10.md](LARGE_SAMPLE_VISUAL_ARENA_2026_10.md).

The metrics from these two arenas are not directly interchangeable: adapted holdout macro-F1 and
large-sample reference agreement answer different research questions.

## Hugging Face status

The repository contains:

```text
huggingface/dataset/
huggingface/space_static/
huggingface/space/
huggingface/export_to_hub.py
```

The static Space is the default public demo; the Gradio version remains optional.

GitHub is the canonical source. A real Hugging Face export is allowed only from `main`; the export
script refuses publication from another Git branch. The export package deliberately contains only
public-safe synthetic material and public aggregate research summaries.

See [HUGGING_FACE.md](HUGGING_FACE.md).

## Deterministic freeze remains central

A deterministic core should not be called stable because it ran once.

The public protocol requires ideas such as:

- future-appended data must not rewrite old canonical records;
- isolated execution should reproduce sequential execution;
- source/input fingerprints should match before outputs are compared;
- record IDs and required schema should remain stable;
- value differences should be separated from dtype/schema differences;
- unavailable information must not be invented.

## What we do NOT claim

This repository does not claim that:

- the framework is profitable;
- the synthetic decisions are useful trading signals;
- a model-arena winner is automatically a deployment choice;
- agreement with a deterministic reference is ground-truth accuracy;
- visual AI always beats numerical models;
- one model family is best for every market;
- every private research result reproduces on public synthetic data.

## Important next steps

1. reusable deterministic prefix/freeze audit helpers;
2. MT4/MT5 read-only bridge example;
3. append-only forward journal and restart tests;
4. deterministic feature plugin interface;
5. simple public statistical baselines;
6. production-grade chart renderer;
7. real open VLM adapters;
8. automatic GitHub -> Hugging Face sync after explicit release approval.

See the [roadmap](ROADMAP.md).
