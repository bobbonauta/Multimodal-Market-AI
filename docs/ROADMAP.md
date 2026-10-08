# Roadmap

This roadmap is intentionally modular. Contributions do not have to follow the order exactly, but the causal core should remain stable while higher-level components evolve.

A checked documentation/design item means the public contract is written; it does **not** imply that the corresponding reference implementation is complete unless explicitly stated.

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
- [x] Experiment/AI-agent governance
- [x] Public/private synchronization rule: open workflow, closed strategy

## Phase 1 — Data and deterministic core

- [ ] Public-data connector examples
- [ ] Timeframe-ladder configuration
- [ ] Deterministic feature plugin interface
- [ ] Event-gate interface
- [x] Public specification for causal candidate manifests
- [x] Reproducible synthetic candidate example with committed source, manifest and seal
- [ ] Candidate-manifest reference implementation
- [x] Strategy-agnostic artifact provenance and sealing helper
- [x] Purged train/validation/test temporal split helper
- [x] Feature-level causal input audit
- [ ] Automated leakage/candidate audit report
- [ ] Reusable inference/cache keys

The candidate-manifest implementation should verify real timestamps, target-column exclusion, duplicates, source provenance and content hashes before expensive model work begins.

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
- frozen-feature extraction behavior when supported;
- checkpoint/resume support;
- license constraints.

## Phase 4 — Frozen representations and fine-tuning recipes

- [x] Public workflow specification for frozen VLM feature caches
- [x] Generic resumable artifact chunk-cache primitives
- [ ] Resumable frozen-feature cache helper
- [ ] Hash/manifest validation for cached feature chunks
- [ ] LoRA/PEFT reference recipe
- [ ] frozen-vision / trainable-projector variants
- [ ] consumer-GPU profile targets
- [ ] checkpoint/resume validation
- [ ] deterministic seeds and manifests
- [ ] benchmark scripts for time/VRAM/RAM

The frozen-feature path should remain usable independently from fine-tuning: a researcher may cache a base model representation once and compare multiple cheap downstream heads without repeatedly running the VLM.

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
- [ ] explicit lineage between candidate manifest, labels and evaluation outputs

A model should not need to be retrained just because a researcher wants to test a different economic policy against already-frozen predictions.

## Phase 7 — Read-only forward validation

- [x] Public read-only forward-validation design
- [ ] Generic append-only observation-journal implementation
- [ ] Raw-observation vs derived-decision schema
- [ ] Closed-bar eligibility tests around pauses/weekends/holidays
- [ ] Polling deduplication and restart-recovery tests
- [ ] History-revision detector / provenance policy
- [ ] Sanitized forward-audit export

This phase validates causal behavior on a live/provider-specific feed without enabling order execution.

## Phase 8 — Community hardware matrix

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
3. Add a generic candidate-manifest helper using synthetic/public data.
4. Add a simple chart renderer.
5. Add a resumable frozen-VLM feature-cache example.
6. Add a benchmark result from a consumer GPU.
7. Add a deterministic moving-average trend/pullback example.
8. Add a breakout/retest baseline.
9. Improve causality tests around market-session boundaries.
10. Add a read-only append-only journal using synthetic feed fixtures.
11. Add Linux/Windows setup notes.
12. Add model-license documentation for one multimodal family.

See [Public workflow synchronization](PUBLIC_WORKFLOW_SYNC.md) for the design behind the candidate, frozen-feature and forward-validation milestones.
