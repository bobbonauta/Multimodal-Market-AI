# Public workflow: causal candidates, frozen VLM features and read-only forward validation

This document captures reusable engineering patterns extracted from private market-research work without publishing any proprietary trading strategy.

The principle is simple: **open workflow, closed strategy**.

The public project can describe how to build, audit, cache and validate a multimodal market pipeline while keeping private the exact strategy rules, thresholds, signal semantics, private labels, datasets and checkpoints.

The public core now includes strategy-agnostic primitives for artifact seals and exact record matching, purged temporal splits with training-only numeric statistics, allowlisted causal feature checks, and resumable chunk caches. A [reproducible synthetic example](../examples/synthetic_candidates/README.md) publishes source observations, an explicit selector and its candidate manifest. A reusable candidate-manifest interface and a frozen-feature adapter remain separate milestones.

## 1. Separate candidate selection from future outcomes

A useful market-AI workflow should not start by letting a model search the entire history with future outcomes already attached.

A safer structure is:

```text
raw / normalized history
        -> deterministic candidate selector
        -> causal audit
        -> immutable candidate manifest
        -> model / representation stage
        -> future-outcome labels and economic evaluation in a separate process
```

The candidate selector may encode a generic event gate, regime filter, structural condition or other user-defined precondition, but it must use only information available at the historical decision timestamp.

The key rule is:

> Freeze which historical rows are candidates before computing or exposing any future-outcome label used to evaluate those candidates.

This prevents accidental circularity where the definition of an interesting event is influenced by what happened after the event.

## 2. Causal candidate manifest

Before expensive model inference or training, create a reproducible manifest of the selected candidates.

A candidate audit should verify at least:

- every timestamp-bearing input used by the selector is `<= decision_ts`;
- no future/outcome/target field is used by the selector;
- the split is derived from actual timestamps, not trusted only from an old `TRAIN`/`TEST` label;
- candidate identifiers are unique;
- duplicate instrument/time/event keys are detected;
- the source dataset and selector version are recorded;
- the resulting manifest receives a content hash.

The feature-level causal audit helper requires an explicit allowlist and availability timestamp for each selected input. It rejects declared forbidden columns and fails closed when required timestamps or columns are missing or invalid.

A strategy-agnostic metadata record may look like:

```yaml
schema: candidate_manifest_v1
split: train
candidate_count: <count>
source_manifest_sha256: <hash>
candidate_file_sha256: <hash>
selector_revision: <revision>
causality:
  result: pass
  future_timestamp_violations: 0
selector_target_columns_used: []
duplicates: 0
```

The public repository does not need the private candidate rows themselves. The reusable idea is the audit contract and provenance structure.

## 3. Frozen VLM feature extraction

A vision-language model does not always need to be fine-tuned or asked to generate text for every downstream experiment.

Another useful pattern is to use a **frozen multimodal model as a feature extractor**:

```text
causal rendered sample
        -> frozen VLM
        -> hidden representation / feature vector
        -> cached feature artifact
        -> lightweight downstream model or analysis
```

During this stage:

- the base model is in evaluation/frozen mode;
- there is no optimizer step;
- no future-outcome label is required for feature extraction;
- protected test/holdout data stays closed during development;
- model revision, processor revision, prompt/schema and renderer version are recorded;
- the cache is treated as a derived artifact, not as raw data.

This can make large experiments practical because the expensive visual pass is performed once while many inexpensive downstream heads can reuse the same frozen representation.

### Chunked and resumable feature caches

Long extraction jobs should be restartable.

A robust chunk should have:

- a deterministic partition key;
- sample IDs in stable order;
- feature shape/dtype metadata;
- model and renderer provenance;
- source candidate-manifest hash;
- output content hash;
- wall time / throughput metadata when benchmarking matters;
- an explicit `complete` flag.

Recommended write pattern:

```text
compute chunk
    -> write temporary file
    -> fsync/close when appropriate
    -> atomic rename to final artifact
    -> write sidecar metadata + hash
```

On resume, skip a chunk only when its metadata says it is complete **and** its stored hash matches the actual artifact.

A file merely existing is not proof that a previous run finished correctly.

The generic chunk-cache helper implements atomic data and metadata writes, dependency-bound reuse, exact expected chunk IDs, invalidation of stale or interrupted chunks, and a completeness check. Applying this helper to a particular frozen model and feature schema remains the caller's responsibility.

## 4. Labels remain a separate downstream process

The candidate manifest and frozen feature cache should not contain future-dependent supervision unless the experiment explicitly creates a separate labelled derivative.

A clean lineage is:

```text
candidate_manifest_v1
        |
        +--> frozen_features_v1
        |
        +--> future_outcomes_v1
                    |
                    v
              supervised head
```

This makes it possible to change an evaluation target without rebuilding the candidate selector, and to reuse the same frozen perception layer for multiple downstream research questions.

It also makes audits easier: a reviewer can distinguish what existed at `decision_ts` from information that was computed later for supervision.

## 5. Read-only forward validation

Historical backtests are not enough to verify that a causal pipeline behaves correctly on a live broker/data feed.

A safe intermediate stage is a **read-only forward observer**. It watches the live feed but cannot place orders.

Recommended architecture:

```text
live/broker feed
    -> raw closed-bar observation journal
    -> causal reconstruction / state calculation
    -> model observation or decision record
    -> sanitized audit output
```

The observer should be an observer, not an actor.

### Raw observations and decisions are different things

Keep raw feed observations in a separate namespace/table from derived decisions or model outputs.

This prevents a raw low-level bar from being mistaken for a system decision and makes provenance clearer.

Example logical separation:

```text
raw_observations
  identity
  instrument
  timeframe
  closed_at
  raw_payload

decisions
  identity
  instrument
  decision_ts
  derived_state
  model_revision
  output
```

The exact schema is application-specific, but the semantic separation should be explicit.

### Append-only and deduplicated journal

A forward journal should prefer append-only semantics.

Use a stable uniqueness key such as:

```text
(feed identity, instrument, timeframe, closed timestamp)
```

or the appropriate equivalent for the source.

Repeated polling and process restarts must not create duplicate observations.

### Closed bars only

The pipeline should know whether the latest market bar is still forming.

Only a bar whose interval has completed may be treated as a closed historical fact for a bar-close decision pipeline.

Special cases worth testing include:

- market pauses;
- weekends;
- holidays;
- delayed ticks;
- restart after the expected close time;
- provider-specific timestamp semantics.

### Restart recovery

After a restart, the observer should recover missing closed observations when the source allows it, while preserving deduplication.

A restart must not silently reset the context window if that would change the meaning of later decisions.

### Detect historical revisions

Some feeds may revise OHLC/spread/history already seen by the observer.

If a previously journaled closed bar changes, do not silently rewrite history and pretend the old decision was made from the new value.

Prefer one of these explicit policies:

- stop and raise a history-revision incident;
- preserve both revisions with provenance;
- mark the affected downstream decision lineage as non-comparable.

The correct policy depends on the research use case, but silent mutation is the dangerous option.

## 6. Sanitized forward evidence

A public audit does not need to contain brokerage credentials, account numbers or private strategy outputs.

Useful public evidence may include:

- observer version;
- feed/timestamp semantics in generic form;
- number of observed closed bars;
- duplicate count;
- gap/recovery checks;
- history-revision behavior;
- test results from synthetic fixtures;
- hashes of sanitized manifests;
- limitations and unresolved assumptions.

Keep private:

- credentials;
- account identifiers;
- private broker/account bindings;
- proprietary signal details;
- private decision records that reconstruct a strategy.

## 7. End-to-end public research pattern

The reusable workflow can be summarized as:

```text
historical / live observations
        -> immutable or append-only raw record
        -> causal normalization and timeframe construction
        -> deterministic candidate gate
        -> candidate causality audit
        -> frozen candidate manifest
        -> optional frozen VLM feature cache
        -> downstream supervised/unsupervised models
        -> separately computed outcomes/economic evaluation
        -> frozen experiment protocol
        -> read-only forward observer
        -> sanitized audit
```

This architecture intentionally separates four questions:

1. **Was the information available at the time?**
2. **Which cases were selected without looking at the future?**
3. **What representation did the model extract from those cases?**
4. **What happened later, and how should that be evaluated?**

Keeping those questions separate is one of the strongest defenses against accidental leakage and irreproducible market-AI results.

## 8. Public/private boundary

Safe to publish when strategy-agnostic:

- pipeline architecture;
- causality contracts;
- generic schemas;
- synthetic fixtures;
- hashing/manifests;
- resumable-cache patterns;
- read-only logging patterns;
- tests for duplicate/gap/restart/history-revision behavior;
- generic benchmark methodology.

Keep private when it would expose the underlying system:

- proprietary setup definitions;
- exact private trigger semantics;
- thresholds and parameter combinations that reconstruct the method;
- private timeframe hierarchies when they are part of the strategy itself;
- private labels or decision history;
- non-redistributable datasets;
- private checkpoints/weights;
- account, credential or broker-binding data;
- internal counts/results when they would materially reveal the strategy.

The purpose of this repository is to make the **research process** reproducible without turning a private strategy into public source code.
