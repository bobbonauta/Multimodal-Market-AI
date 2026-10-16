# Research runbook: from data to a reviewable result

Use this workflow to plan, run and publish a reproducible experiment. It describes
research operations; it does not disclose the private system's indicators or their
parameters, formulas, names, combinations or implementation.

## 1. Write the question before running the experiment

State what the candidate is supposed to improve over the frozen baseline. Name the
primary metric, population and decision rule for accepting the result before final
evaluation. Keep exploratory findings separate from final evidence.

Public pattern names, timeframe choices and research thresholds may be documented.
They do not authorize disclosure of the private indicators that produce a signal.
Do not infer missing private definitions from a pattern name or reported score.

## 2. Check the data before training

Record source revision, instrument identifiers, timezone, session/calendar rules,
bar-open versus bar-close semantics and actual time bounds. Check duplicate IDs,
timestamp order, gaps, missing values, invalid OHLC relationships and non-finite
values. Classify expected market closures separately from missing observations.

For each decision, join only observations whose availability time is at or before
the decision time. A completed higher-timeframe bar may be used only when it is
available. Never fill a missing observation with a future value.

Save input fingerprints and the audit result. If a provider revises history, retain
the original observed version and identify affected comparisons.

## 3. Freeze cases, splits and the baseline

Use stable case IDs and seal the candidate manifest before attaching future outcomes.
Record chronological split boundaries and purge cases whose outcome windows cross
a protected boundary when the protocol requires it. Fit preprocessing on train only.

Verify prefix invariance and isolated replay before freezing the baseline. Compare
input fingerprints before diagnosing output disagreements. A changed source,
selector, target or baseline creates a new experiment version.

See [freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md) and
[experiment governance](EXPERIMENT_GOVERNANCE.md).

## 4. Compare representations on the same cases

Start with the deterministic baseline, then a numerical baseline. Add an optional
visual path only when the comparison can measure its incremental value. Include
ablations: numerical only, visual only where meaningful, and combined inputs.

Keep case IDs, splits, targets and evaluation rules fixed. For a visual cache, record
model revision, rendering/preprocessing revision, prompt/schema revision and input
hashes. Resume only complete, verified chunks; report skipped and failed cases.

## 5. Report quality, coverage and cost together

For classification, report class support, confusion matrix, per-class precision and
recall, macro-F1 and valid-output coverage. Report abstention/WAIT separately from
missing or malformed predictions. Do not silently remove failed outputs from the
denominator; state how they affect each metric.

For agreement with a deterministic reference, call the metric agreement. It does
not establish predictive accuracy against future outcomes. Keep adapter holdout
scores and reference-agreement arenas separate when their tasks differ.

Include uncertainty with the method and sampling unit. Time-adjacent cases may be
dependent; do not present a naive independent-row interval as stronger evidence
than its assumptions support. Report stability across predefined periods or
instruments when the sample permits it.

Record warm-up separately from steady-state latency, batch size, precision, peak
memory, completed cases, elapsed time and total compute cost when measured. A
throughput optimization needs an output-equivalence check before it replaces the
reference path. See [benchmark format](BENCHMARKING.md).

## 6. Keep a compact experiment record

The following is a template, not a claim that an experiment has run. Replace every
placeholder and omit unavailable optional measurements explicitly.

```yaml
experiment_id: replace-me
status: planned
question: replace-me
source_commit: replace-me
input_manifest_hash: replace-me
case_manifest_hash: replace-me
baseline_revision: replace-me
config_revision: replace-me
timeframes: []  # Public choices may be supplied; no private indicator settings.
research_thresholds: {}  # Metric/selection thresholds with units and meaning.
split:
  train: replace-with-time-bounds
  validation: replace-with-time-bounds
  test: replace-with-time-bounds
  purge_rule: replace-me
target_revision: replace-me
model_revision: replace-me
primary_metric: replace-me
acceptance_rule: replace-me
results: null
limitations: []
```

The public record must not contain private feature names or private indicator
configurations. Keep confidential manifests private; publish sanitized provenance
that identifies the public evidence without exposing the underlying strategy.

## 7. Validate forward and publish the evidence

Observe the frozen output through a read-only bridge. Test restart recovery,
duplicate delivery, delayed data and provider revisions. Log what was available
at each decision, rather than reconstructing that knowledge from revised history.

Before publication, inspect the exact file list and diff, including images, tables,
prompts, logs and metadata. Exclude all private indicators, credentials, private
datasets and account details. Pattern terminology, timeframe choices and research
thresholds are allowed; never reconstruct or guess the private mechanism.

Publish methodology, reproducible commands, measured results and limitations on
GitHub. Clearly label synthetic teaching outputs. Export to Hugging Face only from
the verified canonical revision after CI passes; report an upload as complete only
after checking the remote files. See [Hugging Face export](HUGGING_FACE.md).
