# Roadmap

This roadmap is intentionally modular. Contributions do not have to follow the order exactly, but the causal core should remain stable while higher-level components evolve.

## Phase 0 — Public foundation

- [x] Project scope and architecture
- [x] Apache-2.0 license
- [x] Causal multi-timeframe alignment primitive
- [x] Basic leakage checks
- [x] Typed `MarketState`
- [x] R-multiple evaluation metrics
- [x] Quickstart and tests
- [x] Hardware/research-environment documentation
- [x] Benchmarking guidelines
- [x] Generic trading-system research patterns

## Phase 1 — Data and deterministic core

- [ ] Public-data connector examples
- [ ] Timeframe-ladder configuration
- [ ] Deterministic feature plugin interface
- [ ] Event-gate interface
- [ ] Dataset manifests and provenance
- [ ] Train/validation/test temporal split helpers
- [ ] Automated leakage audit report
- [ ] Reusable inference/cache keys

## Phase 2 — Rendering and multimodal input

- [ ] Strategy-agnostic chart renderer
- [ ] Multi-image / multi-timeframe sample format
- [ ] Renderer manifest + hash
- [ ] Visual input masking rules
- [ ] Public synthetic benchmark set

## Phase 3 — Model adapters

Candidate families include:

- [ ] InternVL
- [ ] Qwen multimodal/VL families
- [ ] Gemma multimodal families where licensing permits
- [ ] other open multimodal models proposed by contributors

Each adapter should document:

- exact model/revision;
- VRAM requirements;
- precision/quantization;
- expected input format;
- structured-output behavior;
- checkpoint/resume support;
- license constraints.

## Phase 4 — Fine-tuning recipes

- [ ] LoRA/PEFT reference recipe
- [ ] frozen-vision / trainable-projector variants
- [ ] consumer-GPU profile targets
- [ ] checkpoint/resume validation
- [ ] deterministic seeds and manifests
- [ ] benchmark scripts for time/VRAM/RAM

## Phase 5 — Structured state and decision heads

- [ ] Extended typed `MarketState`
- [ ] visual + numerical fusion interface
- [ ] logistic-regression baseline
- [ ] gradient-boosting baseline
- [ ] small MLP baseline
- [ ] optional compact reasoning/decision-model interface

The goal is to compare sophisticated perception models while keeping downstream decisions cheap and auditable.

## Phase 6 — Evaluation

- [ ] Classification/regression metrics
- [ ] R-multiple distribution reports
- [ ] expectancy / PF / drawdown
- [ ] asymmetric payoff analysis
- [ ] per-symbol and per-regime breakdowns
- [ ] transaction-cost hooks
- [ ] frozen-output re-evaluation under alternative exit policies

A model should not need to be retrained just because a researcher wants to test a different economic policy against already-frozen predictions.

## Phase 7 — Community hardware matrix

- [ ] CPU-only reference benchmark
- [ ] NVIDIA 8–12 GB class
- [ ] NVIDIA 16–24 GB class
- [ ] NVIDIA workstation/datacenter class
- [ ] AMD ROCm
- [ ] Intel GPU where practical
- [ ] Windows vs Linux comparisons

## Good first issues

Potential starter tasks:

1. Add a CSV/Parquet public-data example.
2. Add a configurable multi-timeframe ladder.
3. Add CI for Python 3.10–3.12.
4. Add a simple chart renderer.
5. Add a benchmark result from a consumer GPU.
6. Add a deterministic moving-average trend/pullback example.
7. Add a breakout/retest baseline.
8. Improve causality tests around market-session boundaries.
9. Add Linux/Windows setup notes.
10. Add model-license documentation for one multimodal family.
