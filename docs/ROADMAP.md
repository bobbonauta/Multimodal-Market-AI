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
- [x] CPU-only synthetic multimodal demo
- [x] Public model-arena metrics
- [x] Hugging Face export layout
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

## Phase 2 — Candidate research and experiment provenance

- [x] Public specification for causal candidate manifests
- [x] Reproducible synthetic candidate example with source, manifest and seal
- [ ] Candidate-manifest reference implementation
- [ ] Automated leakage/candidate audit report
- [ ] Reusable inference/cache keys

## Phase 3 — External-system integration

- [x] Generic Python/DataFrame event adapter
- [x] Example that connects an existing bot to causal market context
- [ ] MT4/MT5 CSV/JSON read-only bridge example
- [ ] SQLite/IPC bridge example
- [ ] Generic read-only model-output return channel
- [ ] Multi-symbol integration helper
- [ ] Bridge test proving transport without strategy duplication

## Phase 4 — Rendering and multimodal input

- [x] Lightweight strategy-agnostic SVG renderer for the synthetic demo
- [x] Public synthetic image + fusion-table demo set
- [ ] Production chart-renderer interface
- [ ] Multi-image / multi-timeframe sample format
- [ ] Renderer manifest + hash
- [ ] Visual input masking rules
- [ ] Larger public synthetic benchmark set

## Phase 5 — Model adapters

Planned model families include:

- [ ] InternVL
- [ ] Qwen multimodal/VL families
- [ ] Gemma multimodal families where licensing permits
- [ ] other open multimodal models proposed by contributors

Each adapter should document model revision, memory needs, input/output contracts,
checkpoint/resume behaviour and license limits.

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

- [x] Generic `LONG / SHORT / WAIT` teaching interface
- [x] Deterministic + visual fusion-table teaching example
- [ ] Extended typed `MarketState`
- [ ] Production visual + numerical fusion interface
- [ ] logistic-regression baseline
- [ ] gradient-boosting baseline
- [ ] small MLP baseline
- [ ] optional compact reasoning-model interface

## Phase 8 — Evaluation

- [ ] General classification/regression report helpers
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

## Phase 10 — Community and distribution

- [x] Hugging Face dataset card/export package
- [x] Hugging Face CPU Space package
- [ ] Automated GitHub -> Hugging Face release sync
- [ ] CPU-only benchmark
- [ ] NVIDIA 8–12 GB class
- [ ] NVIDIA 16–24 GB class
- [ ] NVIDIA workstation/datacenter class
- [ ] AMD ROCm
- [ ] Intel GPU where practical
- [ ] Windows vs Linux comparisons

## Good first tasks

1. Run the synthetic multimodal demo and replace one example signal.
2. Add a prefix-invariance audit helper.
3. Add a public CSV/Parquet market-data example.
4. Add an MT4/MT5 read-only bridge that transports a decision without rebuilding the strategy.
5. Add a simple statistical baseline.
6. Replace the mock visual adapter with a real public VLM adapter.
7. Add a frozen-VLM cache example.
8. Add a read-only append-only journal.
9. Improve tests around market-session boundaries and history revisions.
10. Add community hardware measurements.

Start with the repository README and the
[Synthetic multimodal demo](../examples/synthetic_multimodal/README.md).
