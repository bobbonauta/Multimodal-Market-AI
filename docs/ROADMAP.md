# Roadmap

This is the project to-do list.

A checked box `[x]` means that part exists in the public repository. An empty box `[ ]` means it is still planned.

## Phase 0 — Public foundation

- [x] Project scope and architecture
- [x] Apache-2.0 license
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

## Phase 1 — Data and deterministic core

- [ ] Public-data connector examples
- [ ] Configurable timeframe hierarchy
- [ ] Deterministic feature plugin interface
- [ ] Event-gate interface
- [x] Public specification for causal candidate manifests
- [x] Reproducible synthetic candidate example with source, manifest and seal
- [ ] Candidate-manifest reference implementation
- [x] Artifact provenance and sealing helper
- [x] Purged temporal split helper
- [x] Feature-level causal input audit
- [ ] Automated leakage/candidate audit report
- [ ] Reusable inference/cache keys

The idea is simple: before expensive model work, prove which rows were selected, when their information became available, and whether the files still match the inputs that created them.

## Phase 2 — External-system integration

- [x] Generic Python/DataFrame event adapter
- [x] Example that connects an existing bot to causal market context
- [ ] MT4/MT5 CSV/JSON bridge example
- [ ] SQLite/IPC bridge example
- [ ] Generic read-only model-output return channel
- [ ] Multi-symbol integration helper

The integration layer should let a user keep the original bot private and mostly unchanged.

## Phase 3 — Rendering and multimodal input

- [ ] Strategy-agnostic chart renderer
- [ ] Multi-image / multi-timeframe sample format
- [ ] Renderer manifest + hash
- [ ] Visual input masking rules
- [ ] Public synthetic benchmark set

## Phase 4 — Model adapters

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

## Phase 5 — Frozen representations and fine-tuning

- [x] Public design for frozen VLM feature caches
- [x] Generic resumable chunk-cache primitives
- [ ] Full frozen-feature cache example
- [ ] Hash/manifest validation for cached feature chunks
- [ ] LoRA/PEFT reference recipe
- [ ] consumer-GPU profiles
- [ ] checkpoint/resume validation
- [ ] benchmark scripts for time/VRAM/RAM

A frozen representation lets a user run an expensive visual model once, save its output, and test cheaper downstream models many times.

## Phase 6 — Decision models

- [ ] Extended typed `MarketState`
- [ ] visual + numerical fusion interface
- [ ] logistic-regression baseline
- [ ] gradient-boosting baseline
- [ ] small MLP baseline
- [ ] optional compact reasoning-model interface

The rule remains: simple model first, expensive model later.

## Phase 7 — Evaluation

- [ ] Classification/regression metrics
- [ ] R-multiple distribution reports
- [ ] expectancy / profit factor / drawdown
- [ ] asymmetric payoff analysis
- [ ] per-symbol and per-regime breakdowns
- [ ] transaction-cost hooks
- [ ] frozen-output re-evaluation under alternative policies
- [ ] exact lineage between candidates, labels and results

## Phase 8 — Read-only forward validation

- [x] Public read-only forward-validation design
- [ ] Generic append-only observation journal
- [ ] Raw-observation vs derived-decision schema
- [ ] Tests around pauses/weekends/holidays
- [ ] Restart and duplicate handling tests
- [ ] History-revision detector
- [ ] Sanitized forward-audit export

This phase watches a live feed without letting the model place orders.

## Phase 9 — Community hardware matrix

- [ ] CPU-only benchmark
- [ ] NVIDIA 8–12 GB class
- [ ] NVIDIA 16–24 GB class
- [ ] NVIDIA workstation/datacenter class
- [ ] AMD ROCm
- [ ] Intel GPU where practical
- [ ] Windows vs Linux comparisons

## Good first tasks

1. Build three simple public signals and combine them with the deterministic helper.
2. Replace one signal and compare the result fairly.
3. Add a public CSV/Parquet market-data example.
4. Add an MT4/MT5 bridge that exports generic timestamped events.
5. Add a simple chart renderer.
6. Add a frozen-VLM cache example.
7. Add a consumer-GPU benchmark.
8. Improve tests around market-session boundaries.
9. Add a read-only append-only journal.
10. Improve beginner-friendly setup notes.

Start with [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md), then [Integrating an existing bot or EA](INTEGRATING_EXISTING_BOTS.md).
