# Roadmap

This is the project to-do list.

A checked box `[x]` means that part exists publicly. An empty box `[ ]` means it is still planned.

## Phase 0 — Public foundation

- [x] Project scope and architecture
- [x] Apache-2.0 license
- [x] Four-stage operational pipeline: `ACQUIRE -> EXTRACT -> DECIDE -> APPLY`
- [x] Causal multi-timeframe alignment
- [x] Basic leakage checks
- [x] Typed `MarketState`
- [x] R-multiple evaluation metrics
- [x] Quickstart and tests
- [x] Existing-bot integration guide
- [x] Generic event-to-market-context adapter
- [x] Beginner-friendly multi-signal theory guide
- [x] Public deterministic multi-signal combiner
- [x] Runnable deterministic model example
- [x] Failure-modes / lessons-learned guide
- [x] Public/private rule: open workflow, closed strategy

## Phase 1 — Deterministic core and data path

- [ ] Public-data connector examples
- [ ] Configurable timeframe hierarchy
- [ ] Deterministic feature plugin interface
- [ ] Event-gate interface
- [x] Public deterministic freeze/replay protocol
- [ ] Reusable prefix-invariance audit helper
- [ ] Isolated-vs-sequential replay helper
- [ ] Generic schema/value/dtype comparison report
- [x] Artifact provenance and sealing helper
- [x] Purged temporal split helper
- [x] Feature-level causal input audit
- [ ] Automated deterministic-freeze report

The goal of this phase is simple: prove that the deterministic/data path is causal and reproducible before it becomes the base for model comparison.

## Phase 2 — Candidate research and experiment provenance

- [x] Public specification for causal candidate manifests
- [x] Reproducible synthetic candidate example with source, manifest and seal
- [ ] Candidate-manifest reference implementation
- [ ] Automated leakage/candidate audit report
- [ ] Reusable inference/cache keys

Candidate selection is a research tool around the operational pipeline. It is not a mandatory extra operational stage.

## Phase 3 — External-system integration

- [x] Generic Python/DataFrame event adapter
- [x] Example that connects an existing bot to causal market context
- [ ] MT4/MT5 CSV/JSON read-only bridge example
- [ ] SQLite/IPC bridge example
- [ ] Generic read-only model-output return channel
- [ ] Multi-symbol integration helper
- [ ] Bridge test proving transport without strategy duplication

The integration layer should let a user keep the original bot private and mostly unchanged.

## Phase 4 — Rendering and multimodal input

- [ ] Strategy-agnostic chart renderer
- [ ] Multi-image / multi-timeframe sample format
- [ ] Renderer manifest + hash
- [ ] Visual input masking rules
- [ ] Public synthetic benchmark set

Visual/multimodal processing is optional. It should be added only when it improves or validates one of the four operational stages.

## Phase 5 — Model adapters

Planned model families include:

- [ ] InternVL
- [ ] Qwen multimodal/VL families
- [ ] Gemma multimodal families where licensing permits
- [ ] other open multimodal models proposed by contributors

Each adapter should explain:

- exact model/revision;
- memory requirements;
- input format;
- output format;
- checkpoint/resume support;
- license limits.

No model family is the default final choice merely because an adapter exists.

## Phase 6 — Frozen representations and fine-tuning

- [x] Public design for frozen VLM feature caches
- [x] Generic resumable chunk-cache primitives
- [ ] Full frozen-feature cache example
- [ ] Hash/manifest validation for cached feature chunks
- [ ] LoRA/PEFT reference recipe
- [ ] consumer-GPU profiles
- [ ] checkpoint/resume validation
- [ ] benchmark scripts for time/VRAM/RAM

## Phase 7 — Decision models

- [ ] Generic `LONG / SHORT / WAIT` example decision interface
- [ ] Extended typed `MarketState`
- [ ] visual + numerical fusion interface
- [ ] logistic-regression baseline
- [ ] gradient-boosting baseline
- [ ] small MLP baseline
- [ ] optional compact reasoning-model interface

The decision layer should clearly separate:

- a signal that does not vote;
- missing/unavailable information;
- final `WAIT`;
- any longer-lived internal state used by the caller.

Candidate models should be compared only after the operational contract and deterministic core are frozen.

## Phase 8 — Evaluation

- [ ] Classification/regression metrics
- [ ] R-multiple distribution reports
- [ ] expectancy / profit factor / drawdown
- [ ] asymmetric payoff analysis
- [ ] per-symbol and per-regime breakdowns
- [ ] transaction-cost hooks
- [ ] frozen-output re-evaluation under alternative policies
- [ ] exact lineage between candidates, labels and results
- [ ] fair model-comparison harness using identical rows/splits/targets/core

## Phase 9 — Read-only forward validation

- [x] Public read-only forward-validation design
- [ ] Generic append-only observation journal
- [ ] Raw-observation vs derived-decision schema
- [ ] Tests around pauses/weekends/holidays
- [ ] Restart and duplicate handling tests
- [ ] History-revision detector
- [ ] Sanitized forward-audit export
- [ ] Frozen-core vs live-output replay comparison

This phase watches a live feed without letting the research layer place orders.

## Phase 10 — Community hardware matrix

- [ ] CPU-only benchmark
- [ ] NVIDIA 8–12 GB class
- [ ] NVIDIA 16–24 GB class
- [ ] NVIDIA workstation/datacenter class
- [ ] AMD ROCm
- [ ] Intel GPU where practical
- [ ] Windows vs Linux comparisons

## Good first tasks

1. Build three simple public signals and combine them with the deterministic helper.
2. Map the deterministic output to a simple `LONG / SHORT / WAIT` teaching example.
3. Add a prefix-invariance audit helper.
4. Add a public CSV/Parquet market-data example.
5. Add an MT4/MT5 read-only bridge that transports a decision without rebuilding the strategy.
6. Add a simple statistical baseline.
7. Add a chart renderer only after the numerical path is stable.
8. Add a frozen-VLM cache example.
9. Add a read-only append-only journal.
10. Improve tests around market-session boundaries and history revisions.

Start with [Operational pipeline](OPERATIONAL_PIPELINE.md), then [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md), then [Deterministic freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md).
