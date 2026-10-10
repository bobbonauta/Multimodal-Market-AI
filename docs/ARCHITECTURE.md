# Architecture

Multimodal Market AI uses one operational pipeline with four stages:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

Everything else in the repository exists to implement, test or validate one of those four jobs.

The project is strategy-agnostic. A private system can plug into these stages without publishing the rules that define its strategy.

## Stage 1 — Acquire

Purpose: obtain the market case that was actually available at the decision time.

Possible inputs include:

- provider or broker data;
- closed bars;
- synchronized higher timeframes;
- events exported by an existing EA or Python bot;
- related-market context.

Requirements:

- timestamp semantics must be explicit;
- future bars are forbidden;
- raw/provider observations should preserve enough provenance to reproduce later transformations;
- history revisions should be detected or versioned, not silently rewritten.

## Stage 2 — Extract

Purpose: convert the acquired case into useful information.

This stage can contain deterministic or numerical processing such as:

- timeframe aggregation;
- feature calculation;
- structural facts;
- relative-strength calculations;
- multi-signal rules;
- event gating;
- outputs imported from an existing private bot;
- optional visual/multimodal perception.

Every extracted field used by a decision must have a known availability time.

The same input plus the same deterministic version/configuration should produce the same canonical output.

### Deterministic core

The deterministic core should be auditable independently from later model evaluation.

Before it is treated as frozen, test at least:

- prefix invariance: adding later data does not rewrite old canonical records;
- isolated execution: a fresh process reproduces the same result;
- stable IDs and required schema;
- source/input fingerprints;
- unavailable values remain unavailable rather than being invented.

See [Deterministic freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md).

### Optional visual/multimodal extraction

Visual AI is optional, not a mandatory pipeline stage.

A VLM may:

- emit a structured perception result; or
- act as a frozen feature extractor.

Model revision, renderer version, prompt/schema and candidate/input provenance should be recorded.

If a visual model adds no useful information beyond the deterministic/numerical baseline, it does not need to be used.

## Stage 3 — Decide

Purpose: turn extracted information into the action to take now.

A public trading example is:

```text
LONG | SHORT | WAIT
```

Other applications can use different names.

`WAIT` is a decision-layer concept: do not perform either action yet.

It must not automatically be confused with:

- a rule-level `0` meaning “this one rule did not vote”;
- missing/unavailable information;
- a longer-lived internal state maintained by a private system.

Decision logic may be:

- deterministic;
- logistic regression;
- gradient boosting;
- MLP or sequence model;
- compact language/reasoning model;
- another replaceable classifier/regressor.

The framework does not prescribe the final model family.

### Model comparison happens after the pipeline is stable

Candidate models should be compared using the same:

- dataset;
- split;
- allowed inputs;
- target semantics;
- metrics;
- frozen deterministic/core pipeline.

A more complex model wins only if it demonstrates a real, robust improvement.

## Stage 4 — Apply

Purpose: pass the decision to the outside world.

The normal first implementation should be read-only:

```text
decision -> file / database / log / display / external consumer
```

A bridge should transport the decision and its provenance. It should not implement a second independent copy of the strategy.

If an optional field is absent, preserve that absence. If a field is only available in the future, reject it.

Execution-capable integration is a separate safety boundary and is not implied by the existence of a read-only bridge.

## Research and validation plane

Research tools surround the operational pipeline instead of becoming extra operational stages.

```text
                    provenance / hashes
                           |
                           v
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
   |          |          |        |
 timing    replay /    splits /  read-only
 audit      freeze      metrics   forward
   |          |          |        |
   +----------+----------+--------+
              evaluation
```

### Candidate manifests

A deterministic candidate selector may create a smaller research population before expensive model work.

A manifest should record:

- unique candidate IDs;
- decision timestamps;
- source revision/hash;
- selector revision;
- causal-input audit;
- content hash.

Candidate selection must not use future-dependent target/outcome information.

### Train / validation / test

For supervised experiments:

- actual timestamps define the split;
- a target whose outcome ends after a boundary must be purged from the earlier partition when required;
- fitted preprocessing is learned from training rows only;
- the final holdout is protected until the experiment contract is frozen.

### Caches and artifacts

Derived artifacts should be reusable only when their dependencies still match.

Useful controls include:

- source hashes;
- model/config fingerprints;
- exact record IDs;
- completeness flags;
- atomic writes;
- fail-closed behavior for corrupt or incomplete sidecars.

## Read-only forward validation

Before execution-capable integration, the same frozen logic should be observable on live or broker-specific data without order functions.

A forward observer should:

- consume only completed observations;
- separate raw observations from derived decisions;
- deduplicate repeated polling;
- recover safely after restart;
- detect history revisions;
- preserve enough provenance to compare live output with the frozen offline core.

Read-only forward validation proves engineering behavior. It does not prove profitability.

## Causality contract

For every decision timestamp `t`:

1. every input used by the decision must have been available by `t`;
2. a higher-timeframe bar can be used only after it is closed;
3. future/outcome fields are forbidden from model input;
4. candidate selection must not use future-dependent labels;
5. train/validation/test separation follows real timestamps;
6. preprocessing is fitted on training only;
7. cached outputs are bound to enough provenance to prevent stale reuse;
8. adding later data must not silently rewrite earlier canonical deterministic records;
9. required record IDs and schema are explicit;
10. missing optional data remains missing rather than being invented;
11. raw forward observations and derived decisions stay semantically separate;
12. input mismatch is reported as non-comparable before output differences are interpreted.

Violating this contract is a correctness bug, not merely a modeling choice.
