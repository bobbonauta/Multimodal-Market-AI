# Architecture

Multimodal Market AI separates exact market computation from learned perception, learned decision-making and later economic evaluation.

The public architecture is strategy-agnostic. Private systems may plug into the interfaces without publishing the rules that define their setups.

## Layer 1 — Market data

Input data may come from Forex, indices, commodities, equities, crypto or other time-series sources. The public core assumes timestamps have explicit semantics and strongly prefers timezone-aware bar-close timestamps.

Raw/provider data should be preserved or journaled with enough provenance to reproduce later transformations.

## Layer 2 — Deterministic / numerical processing

This layer is responsible for calculations that should not depend on a generative model:

- timeframe aggregation;
- feature calculation;
- pivots / sequences / structural facts;
- timestamp availability;
- event gating;
- deterministic validation;
- causal alignment.

The same input and versioned configuration should produce the same output.

## Layer 2.5 — Candidate gate and immutable manifest

Before expensive model work, a deterministic selector may identify a smaller set of candidate events.

The selector must be auditable independently from the downstream target.

A candidate manifest should record enough information to prove that:

- every selector input existed at `decision_ts`;
- no future/outcome field was used to choose the candidate;
- the active temporal split was derived from real timestamps;
- duplicate candidate keys were checked;
- source and selector revisions are known;
- the final candidate artifact has a reproducible hash.

The candidate set should be frozen before future-outcome labels are computed or exposed to the downstream experiment.

See [Public workflow synchronization](PUBLIC_WORKFLOW_SYNC.md).

## Layer 3 — Visual / multimodal processing

This layer is intended for tasks that are difficult to encode as exact rules:

- chart structure recognition;
- global visual context;
- ambiguous or tolerant relationships;
- pattern description;
- qualitative state extraction.

Model adapters should preserve model/version/prompt/renderer provenance.

Two broad modes are supported conceptually:

1. **direct inference** — the model emits a structured state or description;
2. **frozen feature extraction** — the model remains frozen and its hidden representation is cached for downstream models.

Frozen feature caches must remain linked to the exact candidate manifest, model revision, processor/prompt and renderer version that produced them.

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

A downstream supervised head may join frozen features with separately computed labels, but the lineage between candidate selection, model input and future-dependent supervision must remain explicit.

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

## Layer 7 — Read-only forward validation

Before any execution-capable integration, the same causal pipeline should be testable as a read-only observer against a live or broker-specific feed.

A forward observer should:

- consume only completed observations according to the source timestamp semantics;
- journal raw observations separately from derived decisions/model outputs;
- deduplicate repeated polling;
- recover safely after restarts;
- detect or explicitly version revisions to already-seen history;
- preserve enough context that a restart does not silently change later decisions;
- emit sanitized audit evidence without exposing account or private-strategy data.

This layer validates engineering and causality behavior. It does not imply order execution or profitability.

## Causality contract

For every decision timestamp `t`:

1. all input bars must have close timestamps `<= t`;
2. a higher-timeframe bar can be used only after that higher-timeframe bar is closed;
3. target/outcome fields are never allowed in model input;
4. train/validation/test splits must respect time;
5. any fitted preprocessing must be trained only on the training side of the split;
6. cached model outputs/features must be keyed by enough provenance to prevent silent reuse after input/model/prompt changes;
7. deterministic candidate selection must not use future-dependent labels or prices;
8. the candidate manifest should be frozen before future-outcome supervision is generated for that experiment;
9. raw forward observations and derived decisions should remain semantically separate;
10. previously observed market history must not be silently rewritten without provenance.

Violating this contract is considered a correctness bug, not merely a modeling choice.
