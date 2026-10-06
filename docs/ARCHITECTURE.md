# Architecture

Multimodal Market AI separates exact market computation from learned perception and learned decision-making.

## Layer 1 — Market data

Input data may come from Forex, indices, commodities, equities, crypto or other time-series sources. The public core assumes timestamps have explicit semantics and strongly prefers timezone-aware bar-close timestamps.

## Layer 2 — Deterministic / numerical processing

This layer is responsible for calculations that should not depend on a generative model:

- timeframe aggregation;
- feature calculation;
- pivots / sequences / structural facts;
- timestamp availability;
- event gating;
- deterministic validation;
- causal alignment.

The same input should produce the same output.

## Layer 3 — Visual / multimodal processing

This layer is intended for tasks that are difficult to encode as exact rules:

- chart structure recognition;
- global visual context;
- ambiguous or tolerant relationships;
- pattern description;
- qualitative state extraction.

Future model adapters should expose structured output and preserve model/version/prompt provenance.

## Layer 4 — Typed market state

The numerical and multimodal branches meet in a compact intermediate representation.

A typed state should make it possible to:

- compare different VLM families without rewriting the decision layer;
- cache expensive visual interpretation;
- audit exactly which information reached a decision model;
- separate perception quality from economic outcomes.

`MarketState` in the initial public release is intentionally minimal. The schema will grow through backwards-compatible typed extensions where practical.

## Layer 5 — Decision models

Decision models may be simple or complex: logistic regression, gradient boosting, MLPs, sequence models, small language models, or task-specific heads.

The public project does not prescribe a trading strategy. A decision layer should consume only information available at the decision timestamp.

## Layer 6 — Evaluation

Prediction quality and economic quality are different questions.

The evaluation stack should support at least:

- classification/regression metrics;
- per-symbol and per-time-period breakdowns;
- expectancy in R;
- profit factor;
- average win / average loss;
- maximum drawdown in R;
- return-distribution tails;
- costs/slippage when the user has valid execution data.

A system with a low win rate can still have positive expectancy when winners are materially larger than losers. For that reason, win rate alone must never be treated as a profitability verdict.

## Causality contract

For every decision timestamp `t`:

1. all input bars must have close timestamps `<= t`;
2. a higher-timeframe bar can be used only after that higher-timeframe bar is closed;
3. target/outcome fields are never allowed in model input;
4. train/validation/test splits must respect time;
5. any fitted preprocessing must be trained only on the training side of the split;
6. cached model outputs must be keyed by enough provenance to prevent silent reuse after input/model/prompt changes.

Violating this contract is considered a correctness bug, not merely a modeling choice.
