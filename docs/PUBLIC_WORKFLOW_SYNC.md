# Public workflow: research and validation around one operational pipeline

This document describes reusable engineering patterns learned from private market-research work without publishing any proprietary trading strategy.

The rule is:

> **Open workflow, closed strategy.**

The operational system stays simple:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

Research tools such as candidate manifests, frozen VLM features, train/validation/test splits and read-only forward observers exist to build or validate those four stages. They are not separate mandatory pipelines.

## 1. Freeze the operational meaning before expensive research

Before training a large model, make sure the four jobs are clear.

### ACQUIRE

What market/event data exists at the decision time?

### EXTRACT

What causal facts or features are produced from that data?

### DECIDE

What is the decision target and what does each possible decision mean?

### APPLY

Where does the decision go, starting preferably with a read-only output?

Changing one of these meanings after seeing results creates a new experiment version.

## 2. Keep signal abstention, WAIT and internal state separate

A single signal may have no vote.

A final decision layer may choose `WAIT`.

A private system may maintain a longer-lived internal state.

These are different concepts and should not be silently stored as one variable.

For a public trading example:

```text
LONG
SHORT
WAIT
```

`WAIT` means no new LONG/SHORT action now. The public framework does not prescribe one proprietary explanation for every WAIT case.

## 3. Deterministic core before model selection

The deterministic/data path should be reproducible before it becomes the base for model comparison.

Useful checks include:

- source/input hashes;
- exact record IDs;
- stable required schema;
- feature availability times;
- prefix invariance under future-appended data;
- isolated-run reproduction;
- explicit handling of missing/unavailable values.

Once the agreed checks pass, freeze that deterministic version for the comparison.

See [Deterministic freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md).

## 4. Candidate selection is a research tool

A deterministic selector may identify a smaller set of historical cases for a specific experiment.

A safe structure is:

```text
causal historical observations
        -> deterministic candidate selector
        -> candidate audit
        -> immutable candidate manifest
        -> optional models / representations
        -> future outcomes computed separately
```

The selector must use only information available at `decision_ts`.

A candidate manifest should record at least:

- unique candidate IDs;
- decision timestamps;
- source revision/hash;
- selector revision;
- causal-audit result;
- content hash.

Freeze the candidate population before exposing future-dependent outcomes used for evaluation.

## 5. Frozen VLM features are optional

A VLM is one possible tool inside research, not a required stage of every system.

One efficient pattern is:

```text
causal rendered sample
        -> frozen VLM
        -> feature vector
        -> sealed/resumable cache
        -> lightweight downstream comparison
```

During frozen feature extraction:

- the base model does not train;
- no future outcome is needed to create the feature;
- exact model/revision is recorded;
- renderer/preprocessing/prompt/schema revisions are recorded;
- exact sample IDs are recorded;
- incomplete chunks are not reusable.

A visual representation containing information does not automatically mean it improves a simpler numerical baseline. Incremental value must be measured on the same rows and split.

## 6. Labels and outcomes remain downstream

Keep information known at decision time separate from facts computed later.

```text
causal case / candidate
        |
        +--> deterministic / numerical / visual features
        |
        +--> future outcome or target
                    |
                    v
             supervised evaluation
```

This lets one set of causal inputs be reused for different research questions without redefining what was known at the time.

## 7. Train / validation / test discipline

A split label is not enough by itself.

Verify the real timestamps.

For supervised experiments:

- training uses the past;
- validation is used for development/model choice;
- final test/holdout stays closed until the protocol is frozen;
- a row whose outcome lifecycle crosses a boundary should be purged when required;
- preprocessing statistics are fitted on training only.

If the final holdout is repeatedly opened while choices are still changing, it is no longer a clean final test.

## 8. Compare candidate models only after the contract is frozen

Do not choose a model because it is fashionable or large.

Compare candidates using the same:

- dataset;
- rows/record IDs;
- time split;
- allowed inputs;
- target semantics;
- metrics;
- frozen deterministic/core pipeline.

Possible candidates can include simple rules, statistical/tabular models and multimodal models.

If the complex model does not add robust value, keep the simpler one.

## 9. Read-only forward validation

After the offline core is stable, observe the same logic on a live/provider feed without giving it order authority.

Recommended pattern:

```text
live/provider feed
    -> append-only raw observation journal
    -> frozen causal extraction
    -> decision record
    -> read-only bridge/output
    -> sanitized audit
```

The bridge should transport the frozen result rather than recreate the strategy independently.

### Closed observations only

For a bar-close system, only completed bars are historical facts.

Test:

- pauses;
- weekends/holidays;
- delayed data;
- restart recovery;
- timestamp semantics;
- provider history revisions.

### Do not silently rewrite live history

If a provider changes a previously observed bar, preserve provenance and mark affected comparisons instead of pretending the old decision saw the revised value.

## 10. Input mismatch comes before output mismatch

Before saying two executions disagree, confirm they received the same input.

```text
same input fingerprint -> compare outputs

different input fingerprint -> mark non-comparable
```

Same row count and same start/end timestamps do not prove identical content.

## 11. Continuous work does not mean uncontrolled work

A safe workflow does not need to stop after every report or commit.

If the next step is already authorized, read-only/reversible and does not change semantics, it can continue.

Stop for review when the next step would require something materially new, for example:

- changing the frozen core or target meaning;
- opening a protected holdout;
- inventing a missing domain rule;
- enabling execution/order authority;
- destructive or hard-to-reverse changes;
- unresolved causality/leakage;
- paid/expensive compute outside the approved experiment.

A checkpoint is evidence, not automatically a blocker.

## 12. Public/private boundary

Safe public material includes strategy-agnostic:

- four-stage pipeline architecture;
- causal contracts;
- deterministic freeze/replay methodology;
- candidate manifests;
- split discipline;
- cache/provenance patterns;
- synthetic examples;
- read-only bridging patterns;
- benchmark methodology;
- failure modes and lessons learned.

Keep private:

- proprietary setup definitions;
- exact strategy rules and thresholds;
- private timeframe hierarchies when they reveal the method;
- private labels/decision history that reconstruct the strategy;
- private datasets and economic results;
- private prompts/checkpoints/weights when publication is not intended;
- account, credential and broker-binding details.

The public goal is to make the **engineering process** reproducible while allowing every user to plug in a different private or public strategy.
