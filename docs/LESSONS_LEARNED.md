# Mistakes we learned from — simple version

This page records mistakes found during internal research.

The private strategy is not shown here. Only the lesson is shared.

The goal is simple: **other people should not have to lose time repeating the same mistakes.**

## 1. Do not mix a long-lived state with a short-lived confirmation

**Mistake:** treating “the current bar does not confirm the state” as if the whole state changed.

**Why it is bad:** the target changes meaning and the model may learn the wrong problem.

**What to do:** store long-lived state and current confirmation as separate fields.

## 2. Missing data is not the same as a real neutral answer

**Mistake:** using one value for “missing”, “not ready yet”, “disagreement” and “real neutral”.

**Why it is bad:** the model cannot tell what really happened.

**What to do:** give missing/unknown information its own clear meaning.

## 3. Similar column names can still mean different things

**Mistake:** comparing two columns only because their names look similar.

**Why it is bad:** you may see a huge disagreement that is not real.

**What to do:** first check what each column actually means and what role it plays.

## 4. Required files must really be checked

**Mistake:** a needed input file is missing, but the program quietly skips it.

**Why it is bad:** the result may depend on something that was never recorded correctly.

**What to do:** mark inputs as required or optional. Missing required input = stop.

## 5. A file existing does not mean the job finished correctly

**Mistake:** a long job stops halfway, but the output file exists, so the next run trusts it.

**Why it is bad:** half-finished data can enter the experiment.

**What to do:** save completion information, hashes and exact record IDs. Reuse only if all checks pass.

## 6. If an input changes, old cached output may be wrong

**Mistake:** changing source data, model version or preprocessing but keeping the old cache.

**Why it is bad:** the output may belong to an older experiment.

**What to do:** fingerprint the important inputs and invalidate the cache when any of them changes.

## 7. Do not let joins silently throw rows away

**Mistake:** joining two tables and accepting that some rows disappear.

**Why it is bad:** missing records can hide instead of causing an error.

**What to do:** compare exact ID sets first, then join one-to-one.

## 8. A target can cross a time split

**Mistake:** putting a row in training because the decision happened before the cutoff, even though the future outcome used for its label finishes after the cutoff.

**Why it is bad:** training can contain information from validation time.

**What to do:** track when the full outcome ends and remove rows that cross the boundary.

## 9. Fit preprocessing on training data only

**Mistake:** calculating normalization or other statistics using validation/test data too.

**Why it is bad:** the training process learns something about the future test distribution.

**What to do:** fit preprocessing once on training and reuse it unchanged.

## 10. Every feature has a time when it becomes available

**Mistake:** assuming that because a row is stamped `10:00`, every value inside it was already known at `10:00`.

**Why it is bad:** some features may actually use later information.

**What to do:** record or calculate `available_at` and require:

```text
available_at <= decision_time
```

## 11. Future-only audit information must not become a model input

**Mistake:** creating a useful label after seeing the future, then accidentally feeding it back into the model.

**Why it is bad:** this is direct leakage.

**What to do:** mark future-derived fields as audit-only and block them from model inputs.

## 12. Documentation must match what the code really does

**Mistake:** the document says the system uses three filters, while the code actually uses only one.

**Why it is bad:** people think they are testing a different system.

**What to do:** keep the written rules and executed rules synchronized.

## 13. Protect the final test set

**Mistake:** looking at the final test period again and again while changing the model.

**Why it is bad:** the test slowly becomes another validation set.

**What to do:** make choices on train/validation first. Open the final holdout only when the experiment is frozen.

## 14. Cheap tests come before expensive GPU jobs

**Mistake:** starting a large multimodal run before checking the data and simple baseline.

**Why it is bad:** expensive compute may be testing a broken pipeline.

**What to do:** use this order:

```text
simple baseline
 -> small dry run
 -> resume test
 -> cache invalidation test
 -> only then full expensive run
```

## 15. A visual model must add value, not just look impressive

**Mistake:** continuing VLM/fine-tuning work because the visual model has some signal.

**Why it is bad:** a simple numerical model may already contain the same useful information.

**What to do:** compare both models on the same rows and ask whether the visual model adds something extra.

## 16. Better prediction does not automatically mean better trading

**Mistake:** saying “the model score improved, so the strategy is profitable”.

**Why it is bad:** prediction quality and economic result are different questions.

**What to do:** report predictive metrics and economic evaluation separately.

## 17. If event order is unknown, keep it unknown

**Mistake:** one OHLC bar touches two important levels and the code guesses which happened first.

**Why it is bad:** the label contains invented precision.

**What to do:** mark the order as unknown unless finer data proves it.

## 18. Timeframe aggregation depends on real market sessions

**Mistake:** building higher timeframes only with simple UTC buckets while ignoring provider sessions, holidays, pauses or daylight-saving changes.

**Why it is bad:** your derived bars may not match what the real system saw.

**What to do:** document the provider/session rules. If you do not know them, say the aggregation is not certified.

## 19. Synthetic tests are useful, but they are not live proof

**Mistake:** a fake restart/DST test passes, so we claim the live provider is proven safe.

**Why it is bad:** a real feed can behave differently.

**What to do:** separate:

```text
synthetic test
historical reproduction
live read-only validation
```

## 20. Sampling rules can change the result

**Mistake:** many possible events exist, but one is selected without documenting how.

**Why it is bad:** performance may depend on that hidden choice.

**What to do:** record the sampling rule and test alternatives.

## 21. A wrong idea that gets disproved is still useful

**Mistake:** hiding failed hypotheses and keeping only successful ones.

**Why it is bad:** the same wrong path may be repeated later.

**What to do:** record what was believed, how it was tested, and what the test proved instead.

## Before a long experiment: simple checklist

Before spending a lot of time or GPU money, check:

- Are the exact record IDs frozen?
- Are source hashes recorded?
- Is the target/state meaning written down?
- Does every feature exist by decision time?
- Are time splits clean?
- Was preprocessing fitted only on training?
- Did a simple deterministic baseline run?
- Did a simple numerical baseline run?
- Can an interrupted job resume safely?
- Does changing one dependency invalidate old cache?
- Is the final test set still closed?

Only after these checks should a long expensive model run start.

These lessons apply to an existing EA, a Python bot or a new deterministic system built inside this repository.
