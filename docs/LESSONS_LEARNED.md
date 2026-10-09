# Failure modes and lessons learned

This document records general failure modes encountered during internal market-AI research. The private strategy and private datasets are intentionally omitted. The goal is to preserve the engineering lessons so other users do not need to repeat the same mistakes.

## 1. Do not confuse persistent state with transient confirmation

A variable that describes an ongoing state is not the same thing as a flag that says whether the current observation confirms that state.

**Failure mode:** a temporary lack of confirmation is encoded as a new state/class.

**Consequence:** target definitions change meaning, trained models optimize the wrong task, and downstream metrics become invalid.

**Prevention:** version the target/state contract and keep persistent state, current confirmation and unavailable/unknown status in separate fields.

## 2. Missing is not neutral

Unavailable data, not-yet-initialized state, disagreement and a legitimate neutral state are different concepts.

**Failure mode:** all of them are represented by the same value.

**Consequence:** state machines acquire impossible transitions and models learn artifacts of data availability.

**Prevention:** make missing/unknown explicit and reject illegal enum values instead of coercing them silently.

## 3. Compare semantic roles, not similar column names

The same-looking field name can mean different things in different configurations.

**Failure mode:** two series are compared because their names appear analogous even though their roles differ.

**Consequence:** a large apparent disagreement may be entirely artificial.

**Prevention:** attach explicit semantic roles/schema metadata and validate role compatibility before comparing values. If roles differ, require an explicit mapping.

## 4. Fail closed on required inputs

A manifest is useful only if it proves the files actually consumed by the computation.

**Failure mode:** code skips a missing manifest entry with `continue` or treats every missing file as optional.

**Consequence:** an output may look reproducible while depending on an untracked input.

**Prevention:** classify inputs as required or optional. Missing required input or hash mismatch must stop the pipeline.

## 5. File existence is not proof of completion

Long jobs are interrupted.

**Failure mode:** resume logic sees an output file and assumes the chunk is complete.

**Consequence:** partial or stale artifacts silently enter later stages.

**Prevention:** use atomic writes plus completion metadata, artifact hash, dependency fingerprint and exact expected record IDs. Reuse only when all checks pass.

## 6. Dependency changes must invalidate cached artifacts

Model revision, renderer, prompt, preprocessing, source data and code can all change an output.

**Failure mode:** only the output file hash is checked.

**Consequence:** an old cache is reused under a new experiment definition.

**Prevention:** fingerprint every material dependency and invalidate automatically when any dependency is added, removed or changed.

## 7. Do not use silent inner joins as validation

**Failure mode:** two datasets are merged with an inner join and the reduced row count is accepted.

**Consequence:** missing or extra records disappear instead of causing an error.

**Prevention:** compare exact ID sets first, reject duplicates, missing and extra IDs, then use a validated one-to-one join.

## 8. Split by the full outcome lifecycle, not only decision time

A row may be created before a train/validation boundary while its target depends on data after that boundary.

**Failure mode:** the split uses only `decision_ts`.

**Consequence:** training labels contain validation-period information.

**Prevention:** track `outcome_end_ts` (or equivalent) and purge training rows whose label path crosses the cutoff.

## 9. Fit preprocessing on training data only

**Failure mode:** normalization/PCA/statistics are fitted on the full dataset or refitted separately on validation.

**Consequence:** information about the validation/test distribution leaks into training or comparisons become inconsistent.

**Prevention:** fit preprocessing once on training and apply it unchanged elsewhere. A useful test mutates validation values and verifies that training statistics remain identical.

## 10. Feature availability needs its own timestamp

A row timestamp does not prove every feature was known at that time.

**Failure mode:** a feature derived later is attached to an earlier decision row.

**Consequence:** future information enters the model even though the main dataframe looks time-sorted.

**Prevention:** for causality-sensitive features, record or derive `available_at` and enforce `available_at <= decision_ts`.

## 11. Retrospective audit labels must not become model inputs

Some useful diagnostic categories can only be determined after observing the future.

**Failure mode:** an audit-only class migrates into a feature because it is convenient or predictive.

**Consequence:** severe target leakage.

**Prevention:** mark retrospective fields explicitly as `audit_only`/future-derived and keep them outside feature allowlists.

## 12. Document the filter the code actually executes

**Failure mode:** documentation describes a conceptual multi-stage gate while production code applies only one of those stages; marginal diagnostics are mistaken for cumulative filters.

**Consequence:** researchers believe they are evaluating a different candidate population from the one actually used.

**Prevention:** generate/report executed gate logic from code/config where practical and distinguish descriptive diagnostics from filtering operations.

## 13. Protect the final holdout

**Failure mode:** the test period is repeatedly opened to choose thresholds, features or models.

**Consequence:** the test set becomes another validation set.

**Prevention:** freeze choices on training/validation, record the policy/config hash, then open the protected holdout only for the declared evaluation.

## 14. Run cheap baselines before expensive GPU work

**Failure mode:** a large multimodal run starts before proving that the dataset, split and simple baseline are correct.

**Consequence:** expensive compute measures a broken pipeline or a problem already solved by simpler features.

**Prevention:** naive baseline -> tabular baseline -> tiny dry run -> interruption/resume test -> dependency-invalidation test -> full expensive run.

## 15. Multimodal features must prove incremental value

A vision-language model can contain signal and still add nothing useful once a strong numerical baseline is present.

**Failure mode:** multimodal fine-tuning continues simply because the representation looks sophisticated.

**Consequence:** more cost and complexity without measurable gain.

**Prevention:** evaluate the multimodal representation alone and combined with the numerical baseline on the exact same rows/split. Stop when incremental value is not demonstrated.

## 16. Predictive improvement is not economic edge

**Failure mode:** better AUC/correlation/error is presented as proof of a profitable trading system.

**Consequence:** statistical signal and economic usefulness are conflated.

**Prevention:** keep predictive metrics and strategy-specific economic evaluation separate, including costs and robustness checks where appropriate.

## 17. Ambiguous event order should remain ambiguous

OHLC bars often cannot tell which of two intrabar events happened first.

**Failure mode:** code invents an order and converts ambiguity into a deterministic target.

**Consequence:** labels contain fake precision.

**Prevention:** mark same-bar order as unknown/censored unless higher-resolution data proves the sequence.

## 18. Historical aggregation needs real session semantics

**Failure mode:** higher timeframes are built only as fixed UTC buckets without checking provider session anchors, pauses, holidays or DST.

**Consequence:** derived bars may not match the bars that were actually visible to the original system/provider.

**Prevention:** document timestamp semantics and session anchors. If the authoritative rule is unknown, mark the derived series as not certified rather than guessing.

## 19. Synthetic tests are necessary but not live certification

**Failure mode:** a synthetic DST/restart/history-revision test passes and is treated as proof that a live feed behaves the same way.

**Consequence:** engineering tests are overclaimed as provider evidence.

**Prevention:** distinguish synthetic correctness, historical reproduction and live/read-only validation.

## 20. Sampling choices are part of the experiment

**Failure mode:** multiple candidates from one event/group are reduced to one row without documenting the rule.

**Consequence:** reported performance may depend on an arbitrary sampling convention.

**Prevention:** record the sampling unit, grouping key and weighting rule; test alternatives before treating results as general.

## 21. A failed hypothesis is useful evidence

Several important improvements came from discovering that an assumption was wrong rather than from confirming it.

**Prevention against wasted work:** preserve rejected hypotheses, the test that falsified them and the corrected interpretation. Do not rewrite history so that only successful experiments remain visible.

## Recommended preflight checklist

Before a long experiment:

- freeze the candidate/record universe;
- verify exact IDs and source hashes;
- verify the target/state contract version;
- verify feature availability;
- verify the purged temporal split;
- fit preprocessing on training only;
- run naive and tabular baselines;
- run a small deterministic dry run;
- force an interruption and verify safe resume;
- mutate one dependency and verify invalidation;
- keep the protected holdout closed;
- only then start expensive inference or fine-tuning.

These rules are strategy-agnostic and apply equally to an existing EA, a Python bot or a new research system.
