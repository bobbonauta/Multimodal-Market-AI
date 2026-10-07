# Project status and research evidence

Multimodal Market AI is currently **early alpha**. The public repository contains the causal/multi-timeframe foundation, evaluation utilities and documentation needed to reproduce the research path without publishing any private trading method.

This page separates what is already public, what has been demonstrated in prior internal research, and what still needs an open reproduction.

## Public repository status

The public core currently includes or documents:

- causal OHLCV resampling and higher-timeframe alignment;
- explicit no-future / no-POST input rules;
- tests that reject future higher-timeframe context;
- R-multiple evaluation for asymmetric payoff distributions;
- generic multi-timeframe trading-system research patterns;
- reference CPU/GPU environments and benchmarking guidance;
- repository and experiment governance;
- a public specification for causal candidate manifests;
- a frozen-VLM feature-cache workflow;
- a read-only forward-validation workflow with append-only/deduplicated observation principles.

The next public implementation milestones are:

1. a redistribution-safe market-data connector example;
2. a strategy-agnostic multi-timeframe renderer;
3. at least one open VLM adapter;
4. reusable code for candidate manifests and automated causal audits;
5. a resumable frozen-feature cache helper;
6. a small public fine-tuning example;
7. a generic read-only forward-journal reference implementation;
8. reproducible consumer-GPU benchmarks.

## What prior research has already shown

The project did not start from a blank page. Its architecture is being extracted from a larger experimental research path that used several **internal market-reading systems and private strategy definitions**. Those private rules are deliberately not published here.

The transferable findings are still useful.

### Small multimodal models can learn parts of market reading

A compact fine-tuned vision-language model was able to reproduce several labelled visual/structural market-reading tasks with useful accuracy on a frozen historical evaluation set.

In one internal evaluation, a small VLM reached approximately:

- **0.81 macro-F1** on a directional/structural reading task;
- **above 0.97** on a simpler structured-recognition task;
- around **0.72** on a harder visual task;
- near-perfect agreement on one deterministic-like output task.

These figures are **not yet a public benchmark** and they do **not** demonstrate trading profitability. They show that some visual and multi-timeframe recognition tasks can be learned by relatively small multimodal models on consumer hardware.

### Not every task transfers automatically

A reader trained on one visual schema did not cleanly transfer to a new multi-timeframe layout without further adaptation. Input layout, timeframe hierarchy, prompt/output schema and state representation therefore need to be treated as explicit versioned interfaces.

### Numerical/state representations contain useful information

Separate experiments with lightweight decision models showed that a structured numerical market state contains information beyond a trivial majority baseline, even before adding the full visual reader.

The research direction is therefore not "replace all calculations with one giant AI". It is:

```text
market history
    -> deterministic / numerical layer
    -> causal candidate gate and audit
    -> visual / multimodal reader when useful
    -> typed MarketState or frozen representation
    -> lightweight decision layer
    -> strategy-specific evaluation
```

### Candidate selection must be auditable before labels

Recent internal work reinforced a general methodological rule: the process that decides **which historical rows are worth examining** should be separated from the process that computes **what happened afterward**.

The transferable public pattern is:

```text
causal selector
    -> candidate audit
    -> immutable/hashable candidate manifest
    -> only later compute future-outcome supervision
```

The selector should prove that every timestamp used is available at the decision time and that no target/outcome field influenced candidate selection.

This is now documented in [Public workflow synchronization](PUBLIC_WORKFLOW_SYNC.md).

### Frozen VLM features can separate expensive perception from cheap downstream experiments

Internal research also validated the usefulness of running a small multimodal model in frozen inference mode, caching a representation for each causal candidate, and then reusing those representations for cheaper downstream analysis.

The generalizable engineering lesson is not tied to any private strategy or one model family:

- freeze the VLM during feature extraction;
- do not require future labels for the extraction pass;
- keep protected holdouts closed during development;
- partition long jobs into resumable chunks;
- use atomic writes, completion metadata and content hashes;
- bind every cache to the candidate manifest, model revision, prompt/processor and renderer version.

This lets expensive perception and downstream supervision evolve independently.

### Read-only forward observation is a separate validation stage

A live/broker feed should be testable without enabling execution.

The reusable design keeps:

- raw closed-bar observations separate from decisions/model outputs;
- the journal append-only where practical;
- polling deduplicated;
- restart recovery explicit;
- already-seen history protected against silent mutation;
- public audit exports sanitized from account/private-strategy data.

This stage tests timestamp semantics, causal reconstruction, process continuity and feed behavior. It is not a profitability claim and it is not an execution engine.

### CPU-only research remains valuable

A CPU-only VPS with 6 vCPU and 12 GB RAM has already been sufficient for dataset preparation, deterministic calculations, audits, aggregation and arenas of lightweight tabular/sequence models. GPU time is reserved for the parts that actually require multimodal training or inference.

### Economic evaluation is still open

Predictive accuracy and trading profitability are different questions.

Some earlier experiments used simplified fixed-horizon or fixed-target proxy objectives. Those results are preserved as research evidence, but they are **not treated as final verdicts on systems whose real payoff distribution is asymmetric**.

A system can be economically useful with a win rate below 50% when average winners are much larger than average losers. The public evaluation layer therefore emphasizes:

- expectancy in R;
- profit factor;
- drawdown;
- average win / average loss;
- full positive and negative R distributions;
- robustness across time and instruments.

A losing trade is not automatically a model error if it was a valid setup under the system being studied.

## What has NOT been demonstrated yet

The project does **not** currently claim that:

- one model is universally best for financial markets;
- multimodal AI is always better than numerical models;
- the current public framework is profitable;
- a high win rate is the correct optimization target;
- prior private results automatically reproduce on public datasets;
- results from one asset class transfer unchanged to another;
- a documented internal workflow is already a complete public implementation.

These are research questions or implementation tasks, not assumptions.

## Why publish now?

The useful engineering has become general enough that other researchers can test it on their own systems without access to any proprietary strategy.

A contributor can use trend/pullback logic, breakout/retest, mean reversion, relative-strength models, regime switching, a private strategy, or a completely different financial instrument.

If an improvement to causal alignment, candidate auditing, rendering, VLM inference, feature caching, model adapters, forward journaling, benchmarking or typed states is generalizable, it can improve the open-source core for everyone.

## Reproducibility target

Internal results are motivation. Public claims should eventually be backed by:

1. redistribution-safe or user-provided data;
2. fixed timestamp semantics;
3. frozen train/validation/test periods;
4. no future information in model inputs;
5. an auditable candidate-selection boundary when gating is used;
6. exact base-model and adapter revisions;
7. reproducible commands/configuration;
8. preserved manifests, outputs and checkpoints where licensing permits;
9. hardware/runtime measurements;
10. comparison with simple baselines;
11. separate predictive and economic evaluation;
12. forward-observation evidence when live-feed behavior matters.

See also [Data sources and historical-data workflow](DATA_SOURCES.md), [Model adapters](MODEL_ADAPTERS.md), [Fine-tuning guide](FINETUNING_GUIDE.md), [Public workflow synchronization](PUBLIC_WORKFLOW_SYNC.md), and [Experiment governance](EXPERIMENT_GOVERNANCE.md).
