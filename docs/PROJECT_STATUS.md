# Project status — simple version

Multimodal Market AI is still **early alpha**, but several useful building blocks already work.

## What already exists

The public repository includes:

- causal market-data alignment;
- higher-timeframe construction without using future bars;
- checks that a feature really existed at decision time;
- a public deterministic multi-signal combiner;
- a runnable deterministic example;
- an adapter for connecting events from an existing bot;
- train/validation/test split helpers;
- file hashes, seals and exact record-ID checks;
- resumable cache building blocks;
- a reproducible synthetic candidate example;
- documentation for fine-tuning, multimodal models and read-only live validation;
- a list of mistakes found during internal research so other users can avoid them.

## Two ways to start

### You already have a bot

```text
your bot
 -> export timestamped events
 -> attach causal market context
 -> test simple models
 -> optionally test AI
```

### You do not have a bot

```text
market data
 -> create simple signals
 -> deterministic multi-signal model
 -> create candidates
 -> test simple models
 -> optionally test AI
```

See [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md).

## What internal research has taught us

Private research is used to learn engineering lessons, but private strategy rules and private results are not copied into this repository.

The useful general lessons include:

### Simple models matter

A simple numerical or deterministic model should be tested before an expensive AI model.

If a large model does not improve on the simple baseline, more training may not be useful.

### Visual AI can contain information without adding enough value

A visual representation may contain real signal, but that does not automatically mean it improves an already strong numerical baseline.

The correct question is:

> Does this extra model add useful information on the same rows and the same split?

### Better prediction does not automatically mean profit

A model can improve a prediction score without proving a positive economic edge.

Prediction and economic evaluation must stay separate.

### Correct data contracts matter

If a target, state definition or input meaning is wrong, results built on top of it may also be wrong.

Changing a contract should invalidate dependent artifacts and trigger revalidation.

### Post-decision questions can be separate

AI does not need to create the original signal.

It can also study what happens after an event exists, for example continuation, deterioration or uncertainty.

## What we do NOT claim

This repository does not claim that:

- the public framework is profitable;
- one AI model is best for all markets;
- visual AI always beats numerical models;
- a high win rate is always better;
- private research results automatically reproduce on public data;
- every documented design already has a complete implementation.

## What comes next

Important next steps include:

1. public market-data examples;
2. an MT4/MT5 bridge example;
3. more deterministic feature plugins;
4. a public chart renderer;
5. open multimodal model adapters;
6. simple public statistical baselines;
7. full read-only live-journal examples;
8. more consumer-hardware benchmarks.

See the [roadmap](ROADMAP.md) for the full list.
