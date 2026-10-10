# Project status — simple version

Multimodal Market AI is still **early alpha**, but the public structure is now much clearer.

## The operational pipeline is fixed conceptually

The project uses four jobs:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

This is the main operational path.

Training, candidate manifests, VLM experiments, caches, audits and benchmarks are supporting research tools around that path. They are not separate mandatory pipelines.

## What already exists publicly

The repository includes:

- causal market-data alignment;
- higher-timeframe construction without using future bars;
- feature-availability checks;
- a public deterministic multi-signal combiner;
- a runnable deterministic example;
- an adapter for connecting events from an existing bot;
- train/validation/test split helpers;
- file hashes, seals and exact record-ID checks;
- resumable cache building blocks;
- a reproducible synthetic candidate example;
- beginner-friendly integration documentation;
- the four-stage operational-pipeline specification;
- the deterministic freeze/replay protocol;
- documentation for fine-tuning, multimodal models and read-only forward validation;
- a list of mistakes found during internal research so other users can avoid them.

## Two ways to start

### You already have a bot

```text
your bot
 -> ACQUIRE/import its event
 -> EXTRACT causal context
 -> DECIDE / analyse
 -> APPLY as read-only output
```

### You do not have a bot

```text
market data
 -> simple signals
 -> deterministic EXTRACT
 -> DECIDE
 -> APPLY as read-only output
```

## What changed in the public workflow

Earlier documentation could make the research stack look like one long mandatory chain.

The updated design makes a stronger distinction:

### Operational pipeline

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

### Research/validation around it

```text
causal audits
hashes / manifests
prefix replay
train / validation / test
simple baselines
optional AI / VLM
fair comparison
read-only forward validation
```

This avoids adding models or sub-pipelines only because they exist.

## Deterministic freeze is now part of the public method

A deterministic core should not be called stable only because it produces output once.

The public freeze protocol now documents checks such as:

- future-appended data must not rewrite old canonical records;
- isolated execution should reproduce sequential execution;
- source/input fingerprints should match before outputs are compared;
- record IDs and required schema should remain stable;
- value differences should be separated from dtype/schema differences;
- unavailable information must not be invented;
- model comparisons should reuse the same frozen core.

The repository documents this protocol. A reusable public code helper for all of these freeze checks is still future work.

## Decision semantics are kept separate

A single signal can abstain (`0` in the public helper).

A final decision layer can choose `WAIT`.

A private implementation can also maintain a longer-lived internal state.

These concepts are deliberately documented separately so one value does not accidentally acquire three different meanings.

## What internal research has taught us

Private research is used to extract general engineering lessons. Private strategy rules and private results are not copied into this repository.

General lessons that are safe to share include:

### Simple models matter

A deterministic or simple numerical baseline should be tested before an expensive AI model.

### Visual information is not automatically incremental value

A VLM can contain signal without improving a stronger numerical baseline.

### Better prediction is not automatically economic edge

Predictive quality and economic evaluation are different questions.

### Input identity matters

Two runs with different source fingerprints are not a clean output comparison, even if row counts and date ranges look similar.

### The future must not rewrite the past

Re-running a causal deterministic core with extra future data should leave old canonical records unchanged.

### A bridge should transport, not duplicate

External read-only integration should consume a frozen result instead of creating an independent second implementation of the strategy.

## What we do NOT claim

This repository does not claim that:

- the public framework is profitable;
- one model family is best for all markets;
- visual AI always beats numerical models;
- a deterministic core is certified for every user simply because the protocol is documented;
- every private research result reproduces on public data;
- every documented design already has a complete public implementation.

## Important next steps

1. public market-data examples;
2. reusable deterministic prefix/freeze audit helpers;
3. an MT4/MT5 read-only bridge example;
4. append-only forward-journal code and restart tests;
5. deterministic feature plugin interface;
6. simple public statistical baselines;
7. a public chart renderer;
8. open multimodal model adapters;
9. more consumer-hardware benchmarks.

See the [roadmap](ROADMAP.md) for the full list.
