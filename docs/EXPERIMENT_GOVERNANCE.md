# Experiment and AI-agent governance

This document defines the operational rules for reproducible experiments and AI-assisted repository work in Multimodal Market AI.

The goal is not to prescribe one research strategy. It is to keep experiments auditable, temporally causal and reproducible when datasets, model families, agents and evaluation protocols evolve.

## 1. Git is the operational source of truth

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

Large generated artifacts do not need to be committed. When they remain outside Git, commit a compact manifest containing enough provenance to identify them: path or logical identifier, hashes where practical, row counts, time bounds, model/checkpoint revision and the command or script that generated them.

## 2. One active writer per branch or work tranche

Only one agent or operator should actively modify the same branch/work tranche at a time.

Other agents may:

- review read-only;
- audit methodology;
- propose changes;
- verify results independently;
- work on explicitly separate ownership areas.

Do not run two autonomous writers against the same branch and work directory unless ownership is explicitly partitioned. This reduces conflicting commits, duplicate runs, mixed provenance and accidental changes to a running experiment.

A change of active executor should be recorded before the new executor starts modifying the same work tranche.

## 3. Freeze the experiment contract before measuring results

Before a training or evaluation run, record the experiment contract. At minimum this should identify:

- dataset or manifest revision;
- actual timestamp range of every input pool;
- train / validation / test rules;
- embargo or purge rules when used;
- target definition;
- allowed and forbidden input fields;
- model repository and exact revision/checkpoint;
- adapter/fine-tuning configuration;
- random seed when relevant;
- prompt/schema revision for language or vision-language models;
- evaluation metrics;
- execution assumptions that can change economic results, such as costs or fill conventions.

Changing any of these after seeing evaluation results creates a new experiment version and must be recorded as such.

## 4. Split labels are not enough: verify timestamps

A label such as `TRAIN`, `FIT`, `VAL` or `TEST` is meaningful only inside the split scheme that created it.

When reusing a historical dataset, replay buffer, cache or checkpoint-training corpus in a new experiment:

1. inspect the real decision timestamps;
2. compare them with the current split boundaries;
3. check symbol/instrument overlap and window overlap;
4. verify that any embargo/purge requirement still holds;
5. record the result before training.

Do not assume that an old row labelled `TRAIN` is safe for a newer validation scheme.

For time-window inputs, nearby timestamps on the same instrument may share much of the same historical context. Exact row identity is therefore not the only possible source of leakage.

## 5. Distinguish confirmed contamination from non-independent evaluation

Use precise language.

### Confirmed contamination

Call an evaluation contaminated when evidence shows that evaluation information, the same examples, overlapping future-dependent labels, or materially overlapping evaluation windows entered the training/adaptation process in a way that violates the current protocol.

Such a score must not be promoted as an independent validation/test result. Preserve it as historical evidence if useful, mark it clearly, fix the training/evaluation split, and rerun the comparison.

### Non-independent evaluation

A test can be non-independent without proven direct contamination. A common example is evaluating a pretrained model on historical data from a period or domain that may have been included in opaque pretraining data.

When exact pretraining provenance is unavailable:

- do not claim proven memorization without evidence;
- do not call the score a clean independent holdout;
- label the limitation explicitly;
- prefer a post-pretraining temporal holdout when a genuinely independent comparison is required.

This distinction prevents both overclaiming leakage and overclaiming independence.

## 6. Preserve the final holdout

Do not repeatedly open the final temporal holdout to debug weak candidates, tune thresholds or decide which model to keep.

Use train and validation data for iteration. Open the final holdout only after:

- the candidate is worth evaluating;
- the protocol is frozen;
- model selection is complete for that comparison;
- no further tuning will be performed from the holdout result.

If the holdout is opened early for a diagnostic reason, record that fact and do not later describe it as untouched final test evidence.

## 7. Failures and incidents are part of provenance

Record material incidents before proceeding, including for example:

- out-of-memory failures;
- stale or orphaned training processes;
- wrong environment/interpreter;
- unexpected GPU/CPU use;
- dataset path mistakes;
- failed preflight checks;
- checkpoint-resume problems;
- accidental access to a protected split.

The record should state whether the incident changed model state, data, outputs, timing only, or nothing at all.

## 8. Questions do not grant broader authority

An AI assistant may ask a narrow question when a genuinely missing methodological rule is required to proceed.

That question does not automatically authorize the agent to:

- invent a domain rule;
- change the architecture;
- redefine a target;
- open a protected holdout;
- spend money or use paid compute;
- stop unrelated independent work.

If one subtask is blocked, other authorized independent subtasks should continue unless the recorded workflow says otherwise.

## 9. Separate methodology from private strategy material

The public repository is strategy-agnostic. Updates derived from private research may contribute general engineering lessons, but must not expose:

- proprietary strategy rules;
- private datasets;
- private labels or decision records that reconstruct a strategy;
- private account/broker information;
- confidential experiment artifacts;
- private checkpoints or weights when publication is not intended.

Transfer only reusable methodology, sanitized examples and public-safe evidence.

The working rule is: **open workflow, closed strategy**.

## 10. Maintainer updates and external contributions

The repository distinguishes trusted maintainer synchronization from external contribution flow.

### Verified maintainer synchronization

Repository owners/maintainers may update `main` directly when transferring already-reviewed, public-safe and verified material from internal research or performing scoped repository maintenance.

Before a direct `main` update:

1. verify the current `main` head;
2. review the exact public diff;
3. remove private strategy details, credentials, private data and reverse-engineering clues;
4. run relevant tests/checks when code changes;
5. use a normal commit and never force-push over unrelated work.

Temporary branches used for experiments, proposals, explanations or drafts do not automatically belong in `main`. Once a branch contains verified canonical material, the canonical content should be absorbed into `main` rather than allowing parallel sources of truth to accumulate.

### External contributions

External contributors should use the standard review path:

1. fork or create a feature branch;
2. open a pull request;
3. pass CI and review;
4. merge through GitHub.

See [Repository governance](REPOSITORY_GOVERNANCE.md) and [Contributing](../CONTRIBUTING.md).
