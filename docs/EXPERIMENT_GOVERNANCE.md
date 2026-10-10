# Experiment and AI-agent governance

This document defines the operational rules for reproducible experiments and AI-assisted repository work in Multimodal Market AI.

The goal is not to prescribe one trading strategy. It is to keep experiments auditable, temporally causal and reproducible when datasets, model families, agents and evaluation protocols evolve.

## 1. One operational pipeline

The project uses one operational path:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

Audits, candidate manifests, model experiments, caches and benchmarks support or validate one of these four stages. They should not become competing operational pipelines without a clear reason.

When proposing a new component, state which of the four jobs it improves or validates.

## 2. Git is the operational source of truth

Operational rules are considered active only after they are written and committed to the repository context where the work is taking place.

This includes:

- experiment protocol changes;
- data-split changes;
- model or checkpoint changes;
- agent-role changes;
- stop/resume decisions;
- assumptions that affect evaluation;
- incidents that can affect reproducibility;
- corrections to previously published experiment metadata.

Chat messages, terminal history or an agent's private context are not sufficient as the only record of an operational decision.

Large generated artifacts do not need to be committed. When they remain outside Git, commit a compact manifest containing enough provenance to identify them: logical identifier/path, hashes where practical, row counts, time bounds, model/checkpoint revision and the command/script that generated them.

## 3. One active writer per branch or work tranche

Only one agent or operator should actively modify the same branch/work tranche at a time.

Other agents may:

- review read-only;
- audit methodology;
- propose changes;
- verify results independently;
- work on explicitly separate ownership areas.

Do not run two autonomous writers against the same branch/work directory unless ownership is explicitly partitioned.

## 4. Freeze the deterministic/core contract before model comparison

Before candidate models are compared, freeze the data/core contract that they share.

At minimum record:

- dataset/source manifest revision;
- actual timestamp range;
- deterministic/core code revision;
- configuration revision;
- record-ID rule;
- required schema;
- timestamp/session semantics;
- target definition;
- allowed/forbidden inputs;
- split rules;
- evaluation metrics.

Useful deterministic freeze checks include:

- prefix invariance under future-appended data;
- isolated-run reproduction;
- exact/expected record IDs;
- input/source hashes;
- explicit schema and unavailable-value handling.

A model comparison should not quietly use a different deterministic core for one candidate.

## 5. Freeze the experiment contract before measuring final results

Before training or final evaluation, record:

- dataset/manifest revision;
- train / validation / test rules;
- embargo/purge rules when used;
- target definition;
- allowed and forbidden input fields;
- exact model revision/checkpoint;
- adapter/fine-tuning configuration;
- random seed when relevant;
- prompt/schema revision for language or vision-language models;
- evaluation metrics;
- execution assumptions that can change economic results.

Changing one of these after seeing evaluation results creates a new experiment version and must be recorded as such.

## 6. Split labels are not enough: verify timestamps

A label such as `TRAIN`, `FIT`, `VAL` or `TEST` is meaningful only inside the split scheme that created it.

When reusing historical data or cached outputs:

1. inspect real decision timestamps;
2. compare them with current split boundaries;
3. check instrument/window overlap;
4. verify embargo/purge rules;
5. record the result before training.

Do not assume an old row labelled `TRAIN` is automatically safe for a newer split.

## 7. Distinguish contamination from non-independent evaluation

### Confirmed contamination

Call an evaluation contaminated when evidence shows that evaluation information, the same examples, overlapping future-dependent labels, or materially overlapping evaluation windows entered training/adaptation in violation of the current protocol.

Such a score must not be promoted as an independent test result.

### Non-independent evaluation

A test can be non-independent without proven direct contamination, for example when evaluating a pretrained model on data that may have appeared in opaque pretraining.

When exact pretraining provenance is unavailable:

- do not claim memorization without evidence;
- do not call the score a clean independent holdout;
- label the limitation explicitly;
- prefer a post-pretraining temporal holdout when independence matters.

## 8. Preserve the final holdout

Do not repeatedly open the final temporal holdout while changing features, thresholds, model family or target semantics.

Use train and validation for iteration.

Open the final holdout only after:

- the operational/data contract is frozen;
- model selection is complete for that comparison;
- no more tuning will be performed from the holdout result.

If the holdout is opened early for diagnosis, record that fact and do not later describe it as untouched final evidence.

## 9. Compare inputs before outputs

When two runs disagree, first verify that they received the same source data.

```text
same input fingerprint -> compare outputs

different input fingerprint -> mark non-comparable
```

Same row count, symbol and time bounds are not proof of identical content.

Also report separately:

- value differences;
- schema differences;
- dtype/representation differences.

## 10. Failures and incidents are provenance

Record material incidents such as:

- out-of-memory failures;
- stale/orphaned processes;
- wrong environment/interpreter;
- dataset path mistakes;
- failed preflight checks;
- checkpoint-resume problems;
- accidental protected-split access;
- history revisions;
- reproducibility/prefix failures.

State whether the incident changed model state, data, outputs, timing only, or nothing at all.

## 11. A checkpoint is not automatically a stop condition

A report, commit or successful verification is evidence, not automatically a blocker.

When the next step is already defined, authorized, read-only/reversible and does not change semantics, the workflow may continue.

Stop for review when proceeding would require a materially new decision, for example:

- changing a frozen core or target meaning;
- inventing a missing domain rule;
- opening a protected holdout;
- enabling order/execution authority;
- destructive or hard-to-reverse actions;
- unresolved leakage/causality;
- paid/expensive compute outside the approved protocol;
- no defined next step.

This avoids both uncontrolled autonomy and unnecessary stop/start fragmentation.

## 12. Questions do not grant broader authority

An AI assistant may ask a narrow question when a genuinely missing methodological rule is required.

That question does not authorize the agent to:

- invent a domain rule;
- change architecture;
- redefine a target;
- open a protected holdout;
- spend money;
- enable execution;
- stop unrelated independent work.

## 13. Separate methodology from private strategy material

The public repository is strategy-agnostic.

Updates derived from private research may contribute general engineering lessons, but must not expose:

- proprietary strategy rules;
- private datasets;
- private decision records that reconstruct a strategy;
- private timeframe hierarchies when they reveal the method;
- private account/broker information;
- confidential experiment artifacts;
- private checkpoints/weights when publication is not intended.

Transfer only reusable methodology, sanitized examples and public-safe evidence.

The working rule is: **open workflow, closed strategy**.

## 14. Maintainer updates and external contributions

### Verified maintainer synchronization

Repository owners/maintainers may update `main` directly when transferring already-reviewed, public-safe and verified material from internal research or performing scoped maintenance.

Before a direct `main` update:

1. verify current `main` head;
2. review the exact public diff;
3. remove private strategy details, credentials, private data and reverse-engineering clues;
4. run relevant tests/checks when code changes;
5. use a normal commit and never force-push over unrelated work.

Temporary branches used for experiments, proposals or drafts do not automatically belong in `main`.

### External contributions

External contributors should use the standard review path:

1. fork or create a feature branch;
2. open a pull request;
3. pass CI and review;
4. merge through GitHub.

See [Repository governance](REPOSITORY_GOVERNANCE.md) and [Contributing](../CONTRIBUTING.md).
