# Multimodal model arena — public results

This page publishes aggregate metrics from an internal multimodal research arena.

The strategy, proprietary features, exact market-state definitions, private datasets and trained adapters are not published. The metrics are useful on their own for understanding model behaviour, compute cost and experimental design.

> These are research results, not trading results and not evidence of profitability.

## What was tested

The same adapter-training recipe was applied to several open multimodal / vision-language models.

The experiment used:

- 1,824 training examples;
- 200 validation examples;
- 256 final holdout examples;
- one training epoch;
- checkpoint selection using validation only;
- the final holdout opened once, after checkpoint selection;
- explicit overlap checks between training/validation/holdout identities and image hashes.

The public score below is the mean macro-F1 across **two related three-class classification views**, called **Task A** and **Task B** here. Their private strategy meaning is intentionally not published.

## Aggregate holdout results

| Model | Untuned/base score | Adapted holdout score | Delta | GPU used | Training sec/example | Approx. pod cost |
|---|---:|---:|---:|---|---:|---:|
| Liquid 3B | 0.1931 | 0.1911 | -0.0020 | A40 | 2.362 | $1.05 |
| Qwen3-VL 4B | 0.2875 | **0.7485** | +0.4610 | A40 | 2.079 | $1.00 |
| Qwen3-VL 8B | 0.2624* | **0.8764** | +0.6140 | RTX 4090 | **1.683** | $1.34 |
| Gemma 4 26B-A4B | 0.5000* | **0.6502** | +0.1502 | A100 SXM 80 GB | **1.144** | $2.05 |
| MiniCPM-V 4.6 | 0.2971 | 0.2078 | -0.0893 | A40 | 2.592 | $1.08 |
| Qwen2.5-VL 7B | 0.3150 | **0.7454** | +0.4304 | RTX 4090 | 3.097 | $1.90 |
| Gemma 4 12B | 0.3654* | **0.7886** | +0.4232 | A40 | 2.153 | $1.15 |
| InternVL 3.5 14B | 0.3047 | **0.4971** | +0.1924 | A40 | 5.577 | $2.24 |

`*` Some earlier untuned/base measurements used a different numerical precision or quantization from the adapted run. For that reason, the **absolute adapted holdout scores are more directly comparable with each other than every base-to-adapter delta**.

No winner or deployment decision is implied by this table.

## Why one aggregate number is not enough

Two models show the problem clearly.

### Qwen3-VL 8B

| Metric | Task A | Task B | Mean |
|---|---:|---:|---:|
| Holdout macro-F1 | 0.8967 | 0.8562 | **0.8764** |

Both tasks improved strongly and neither collapsed to one class.

### InternVL 3.5 14B

| Metric | Task A | Task B | Mean |
|---|---:|---:|---:|
| Holdout macro-F1 | **0.7720** | **0.2222** | **0.4971** |

The mean score looks substantially better than the untuned baseline, but Task B did not learn the problem well. This is exactly why model evaluation should report both:

1. an aggregate score;
2. per-task / per-group results;
3. class-collapse diagnostics.

A single headline number can hide a serious failure.

## Models stopped before a full result

### Pixtral 12B

The full run was stopped because measured throughput was too low for the value of the experiment:

- about 1.1 cases/minute on an A40 during the observed run;
- about 33.9 GB peak VRAM in the smoke test;
- roughly $0.24 spent before stopping;
- no final adapted holdout score was produced.

The important lesson is not that the model is bad. The lesson is that **an experiment can be economically irrational even when it is technically possible**.

### Mistral Small 3.1 24B

The run was also stopped for compute efficiency:

- RTX 4090 smoke test hit CUDA OOM during backward;
- A40 smoke/run path was technically viable;
- measured training speed was about 0.8 steps/minute, roughly 18 seconds/example at that stage;
- roughly $0.79 spent before stopping;
- no final adapted holdout score was produced.

Again, this is not a general quality judgment about the model. It is a result for this specific workload and adapter recipe.

## Compute lessons

### Cheaper GPU per hour does not always mean cheaper experiment

The Qwen3-VL 8B run is a useful example. An RTX 4090 had a higher hourly price than an A40 in this environment, but its measured training throughput made the total job competitive.

The correct comparison is approximately:

```text
total compute cost = hourly price × real job duration
```

not simply:

```text
cheapest hourly GPU = cheapest experiment
```

### Smoke-test speed is only a rough estimate

A three-case or three-step smoke test is excellent for finding:

- out-of-memory errors;
- loading failures;
- broken dependencies;
- obviously impossible configurations.

It is not always a reliable predictor of full-run throughput. Validation, generation, checkpointing and other stages may have very different speeds.

### Bigger is not automatically better

In this arena:

- an 8B model produced the highest observed adapted aggregate score;
- a 14B model improved overall but failed badly on one subtask;
- a larger MoE model was fast on an A100 but did not produce the highest holdout score;
- some smaller models improved strongly while another smaller model became worse after adaptation.

Model size alone is therefore a poor selection rule.

## Artifact-delivery rule

The experiment also reinforced a simple operational rule for trained adapters and other large artifacts:

```text
train
  -> save adapter/checkpoint
  -> calculate SHA-256
  -> transfer
  -> verify SHA-256 at destination
  -> only then remove the temporary source copy
```

In the final transfer batch, all **36/36 expected SHA-256 checks matched** before the temporary VPS copies were allowed to be removed.

## What these results do not reveal

The published numbers do not include:

- proprietary strategy rules;
- exact private signal construction;
- private timeframe hierarchy;
- entry/exit logic;
- private feature names;
- private event records;
- private chart images or datasets;
- trained adapter weights;
- account, broker or execution details.

This follows the project rule:

> **Open workflow, closed strategy.**

## Reusable experimental lessons

The results support a few general rules:

1. Freeze the dataset and evaluation contract before comparing models.
2. Use the same train/validation/holdout population for candidates.
3. Select checkpoints on validation, not on the final holdout.
4. Open the final holdout once.
5. Report subgroup/task metrics, not only one mean score.
6. Detect class collapse explicitly.
7. Measure actual runtime, VRAM and total cost.
8. Stop experiments whose cost is no longer justified.
9. Keep negative results: they prevent other people from repeating the same expensive mistake.
10. Treat model size as one engineering variable, not as a quality ranking.
