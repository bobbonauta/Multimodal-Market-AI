# Large-sample visual arena — October 2026

This page publishes aggregate, public-safe results from a second internal multimodal arena.

It is deliberately separate from the adapter-training arena in
[MODEL_ARENA_RESULTS.md](MODEL_ARENA_RESULTS.md): the two experiments use different populations,
metrics and purposes, so their headline numbers must not be compared directly.

> These are research results, not trading results and not evidence of profitability.

## What was tested

Five open vision-language model configurations were evaluated on the same frozen population:

- Qwen3-VL 2B;
- InternVL 3.5 2B (R2 configuration);
- Qwen3-VL 4B;
- Qwen2.5-VL 7B;
- Qwen3-VL 8B.

The arena used:

- 1,000 frozen cases per model;
- two 500-case tranches, called A and B;
- 5,000/5,000 valid model outputs;
- zero missing, duplicate or extra case IDs in the audited outputs;
- the same frozen evaluation contract for all candidates;
- a separate independent recomputation of the aggregate statistics.

The public names **Task A** and **Task B** are aliases for two related visual views. Their private
strategy meaning is intentionally not published.

The comparison reference is a binary deterministic output. It is a **reference anchor, not ground
truth**. The visual model can also emit a third non-directional class, so agreement with the binary
reference must not be read as accuracy.

## Aggregate results

Agreement confidence intervals are 95% Wilson intervals.

| Model | Task A agreement vs reference | Task B agreement vs reference | Task A/B internal agreement | Mean sec/case |
|---|---:|---:|---:|---:|
| Qwen3-VL 8B | **0.603 [0.572–0.633]** | 0.414 [0.384–0.445] | 0.369 | 1.83 |
| Qwen3-VL 2B | 0.564 [0.533–0.594] | 0.476 [0.445–0.507] | 0.297 | **1.03** |
| Qwen3-VL 4B | 0.556 [0.525–0.587] | 0.480 [0.449–0.511] | 0.360 | 1.48 |
| InternVL 3.5 2B (R2) | 0.549 [0.518–0.580] | 0.395 [0.365–0.426] | **0.516** | 1.06 |
| Qwen2.5-VL 7B | 0.501 [0.470–0.532] | **0.496 [0.465–0.527]** | 0.324 | 1.80 |

`Task A/B internal agreement` measures whether the two visual views returned the same directional
class. It is not an accuracy score.

## What changed when the sample became larger

The large-sample run adds information that a small holdout cannot provide on its own:

- all five candidates completed 1,000 cases rather than a few hundred;
- the two 500-case tranches produced closely aligned aggregate behaviour, with per-model differences
  on the main agreement measures within roughly 0.03;
- Qwen3-VL 8B was the only candidate whose Task A agreement interval was entirely above 0.55;
- Task B remained difficult for every candidate: no model exceeded 0.496 agreement with the binary
  reference;
- InternVL 3.5 2B showed the highest agreement between the two visual views, while not leading the
  reference-agreement metrics;
- throughput differed materially across models, reinforcing that model size alone is not a useful
  deployment rule.

A separate independent recomputation of the 5,000 output records found **zero discrepancies** in
the published aggregate counts and agreement statistics.

## Why this does not replace the earlier arena

The earlier public arena reports adapted holdout **macro-F1** after a controlled fine-tuning
experiment. This arena reports **agreement statistics** from a larger frozen inference population.

Therefore:

```text
adapted holdout macro-F1 != large-sample reference agreement
```

A model can rank differently between the two experiments without either result being wrong.
The experiments answer different questions:

- the fine-tuning arena asks how well an adapted model learned two held-out classification tasks;
- the large-sample arena asks how stable and consistent candidate visual outputs are across a much
  larger shared population and against a deterministic comparison anchor.

## Operational lessons

1. A smoke test should validate loading and the output contract before a large GPU run.
2. Every candidate should receive the same frozen cases and contract.
3. Large runs should be split into resumable tranches without changing case identity.
4. Completeness checks should cover missing, duplicate and extra IDs, not only row count.
5. Aggregate results should be independently recomputed from the raw outputs.
6. A deterministic reference should not be mislabeled as ground truth.
7. A third visual class can lower raw agreement with a binary reference and must be reported
   explicitly in the interpretation.
8. Throughput should be measured from the real run, not inferred from parameter count.

## What remains private

This public report does not disclose:

- proprietary strategy rules;
- the private meaning of Task A or Task B;
- private timeframe hierarchies;
- private instruction/skill text;
- private thresholds, labels or feature names;
- raw private cases or chart images;
- adapter weights or model artifacts;
- entry, exit, stop or trailing logic.

This follows the project rule:

> **Open workflow, closed strategy.**
