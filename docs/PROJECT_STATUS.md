# Project status and research evidence

Multimodal Market AI is currently **early alpha**. The public repository provides a causal/multi-timeframe foundation, integration helpers for existing trading systems, reproducibility utilities and documentation for adding numerical or multimodal AI without publishing a private strategy.

This page separates what is already public, what has been demonstrated in internal research, and what still needs open reproduction.

## Public repository status

The public core currently includes or documents:

- causal OHLCV resampling and higher-timeframe alignment;
- a generic adapter that attaches closed market context to events emitted by an existing bot;
- explicit no-future / no-POST input rules;
- feature-level availability audits;
- R-multiple evaluation for asymmetric payoff distributions;
- artifact sealing, dependency fingerprints and exact record-ID checks;
- purged temporal splits with training-only preprocessing statistics;
- resumable chunk caches with atomic writes;
- generic multi-timeframe research patterns;
- a public specification for causal candidate manifests;
- a reproducible synthetic candidate workflow;
- a frozen-VLM feature-cache workflow;
- a read-only forward-validation workflow with append-only/deduplicated observation principles;
- a failure-modes guide based on mistakes found during internal research.

The next public implementation milestones include:

1. redistribution-safe market-data connector examples;
2. richer adapters for MT4/MT5 and other external systems;
3. a strategy-agnostic multi-timeframe renderer;
4. at least one open VLM adapter;
5. a reusable candidate-manifest reference implementation;
6. a small public fine-tuning example;
7. a generic read-only forward-journal reference implementation;
8. reproducible consumer-GPU benchmarks.

## What prior research has already shown

The project did not start from a blank page. Its architecture is extracted from a larger experimental research path that used internal market-reading systems and private strategy definitions. Those private rules, target definitions, datasets and economic results are deliberately not published here.

The transferable findings are still useful.

### Existing systems can be augmented instead of replaced

A mature bot does not need to be rewritten around an AI model. A cleaner boundary is:

```text
existing system
    -> timestamped candidates/state
    -> causal context + audit
    -> numerical and/or multimodal model
    -> score / estimate / ranking
    -> research, read-only validation, or optional feedback to the original system
```

This allows the original strategy and execution logic to remain private while the surrounding AI/research layer stays reproducible.

### Correcting the causal contract can change earlier conclusions

Internal audits found that a mismatch between different state/confirmation semantics could invalidate dependent targets and results. The general lesson is that target/state contracts must be explicit, versioned and tested before downstream metrics are trusted.

Earlier private scores that depended on superseded contracts are not treated as current public evidence.

### Lightweight numerical baselines matter

Recent internal work confirmed that a lightweight numerical/state model can retain useful predictive information outside the training period. This does not prove profitability, but it establishes a meaningful comparison point that should be tested before spending GPU time on larger multimodal models.

### Multimodal signal is not the same as incremental value

A frozen multimodal representation can contain measurable information and still add little or nothing once a strong numerical baseline is present.

That distinction matters. The recommended protocol is:

```text
naive baseline
    vs
numerical baseline
    vs
frozen multimodal representation
    vs
numerical + multimodal
```

on the **same rows, split, weighting and metrics**. Further fine-tuning should not be automatic when the multimodal representation fails to demonstrate useful incremental value.

### Predictive improvement is not economic edge

Internal holdout work reinforced a separate lesson: a model can improve prediction/filtering metrics without establishing a positive economic edge.

The project therefore keeps predictive evaluation and strategy-specific economic evaluation separate. Better AUC, calibration, ranking or error metrics are evidence about prediction, not proof of a profitable trading system.

### Post-decision / post-entry modelling is a separate research problem

Current internal research is also studying whether information observed **after an initial decision** can help estimate continuation, deterioration or risk. This is intentionally separated from entry prediction.

The transferable lesson is architectural: one AI component does not need to decide everything. Candidate generation, context reading, ranking and post-decision management can be different tasks with different targets and validation rules.

No private management rule or strategy-specific target is published here.

### Candidate selection must be auditable before labels

The process that decides which historical rows are worth examining should be separated from the process that computes what happened afterward.

```text
causal selector
    -> candidate audit
    -> immutable/hashable candidate manifest
    -> only later compute future-outcome supervision
```

Every selector input must have been available at the decision timestamp, and target/outcome fields must not influence candidate selection.

### Frozen features make expensive perception reusable

A small multimodal model can be run once in frozen inference mode and its representations cached for cheaper downstream experiments, provided the cache is bound to the exact candidate population, model revision, preprocessing, renderer/prompt/configuration and code/data dependencies.

Long inference jobs should be chunked, atomic, resumable and fail closed on stale or incomplete artifacts.

### Read-only forward observation is a separate validation stage

A live/broker feed should be testable without enabling execution.

The reusable design keeps:

- raw closed-bar observations separate from decisions/model outputs;
- the journal append-only where practical;
- polling deduplicated;
- restart recovery explicit;
- already-seen history protected against silent mutation;
- public audit exports sanitized from account/private-strategy data.

This stage validates timestamp semantics, causal reconstruction, process continuity and feed behavior. It is not a profitability claim and it is not an execution engine.

## Lessons from failures

A major purpose of the public repository is to preserve errors that should not be repeated. Internal work has exposed failure modes involving:

- persistent state vs transient confirmation;
- missing/unknown values being mistaken for real states;
- semantic-role mismatches between apparently similar columns;
- required files silently skipped from manifests;
- stale or partial cache reuse;
- non-purged temporal splits;
- preprocessing leakage;
- future/audit-only information entering features;
- ambiguous intrabar ordering being treated as known;
- repeated tuning on protected holdouts;
- expensive GPU work started before cheap baselines and dry runs.

The sanitized engineering lessons are documented in [Failure modes and lessons learned](LESSONS_LEARNED.md).

## What has NOT been demonstrated yet

The project does **not** currently claim that:

- one model is universally best for financial markets;
- multimodal AI is always better than numerical models;
- the current public framework is profitable;
- every existing bot benefits from an AI layer;
- a high win rate is the correct optimization target;
- prior private results automatically reproduce on public datasets;
- results from one asset class transfer unchanged to another;
- a documented internal workflow is already a complete public implementation.

These are research questions or implementation tasks, not assumptions.

## Why publish now?

The engineering is general enough that someone with an existing EA, Python bot, backtester or private strategy can test the same research discipline without revealing their rules.

A contributor can keep candidate generation private and contribute only generic improvements to causal alignment, integration adapters, candidate auditing, rendering, VLM inference, feature caching, model comparison, forward journaling or benchmarking.

## Reproducibility target

Public claims should eventually be backed by:

1. redistribution-safe or user-provided data;
2. fixed timestamp semantics;
3. stable event/candidate IDs;
4. frozen train/validation/test periods;
5. purging when a target lifecycle crosses a split boundary;
6. no future information in model inputs;
7. an auditable candidate-selection boundary when gating is used;
8. exact base-model and adapter revisions;
9. reproducible commands/configuration;
10. preserved manifests, outputs and checkpoints where licensing permits;
11. hardware/runtime measurements;
12. comparison with naive and numerical baselines;
13. separate predictive and economic evaluation;
14. read-only forward evidence when live-feed behavior matters.

See also [Integrating an existing bot or EA](INTEGRATING_EXISTING_BOTS.md), [Failure modes and lessons learned](LESSONS_LEARNED.md), [Data sources](DATA_SOURCES.md), [Model adapters](MODEL_ADAPTERS.md), [Fine-tuning guide](FINETUNING_GUIDE.md), [Public workflow synchronization](PUBLIC_WORKFLOW_SYNC.md), and [Experiment governance](EXPERIMENT_GOVERNANCE.md).
