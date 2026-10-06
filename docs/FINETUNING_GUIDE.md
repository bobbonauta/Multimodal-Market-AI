# Fine-tuning guide for multimodal market readers

This document describes a **strategy-agnostic** path for adapting an open multimodal model to market-reading tasks.

It is deliberately written as a reproducible research recipe rather than a promise that one model, dataset or training method will work for every market.

## 1. Define the task before training

Do not start with "train an AI to trade". Split the problem into testable tasks.

Examples:

- identify directional structure;
- classify regime: trend / range / transition;
- recognize whether multiple timeframes agree;
- detect an ambiguous or noisy chart state;
- convert visual context into a typed `MarketState`;
- rank already-defined candidate events.

The target should be defined before the model sees validation/test outcomes.

## 2. Build a causal dataset

Each training sample should be reconstructable at a historical decision timestamp.

Typical record:

```json
{
  "sample_id": "EURUSD_2021-03-10T12:00:00Z",
  "decision_ts": "2021-03-10T12:00:00Z",
  "images": {
    "fast": "images/..._fast.png",
    "middle": "images/..._middle.png",
    "slow": "images/..._slow.png"
  },
  "context": {
    "symbol": "EURUSD"
  },
  "target": {
    "regime": "trend"
  }
}
```

Rules:

- all rendered bars must be closed at or before `decision_ts`;
- no future outcome may be encoded in filenames, overlays or metadata presented to the model;
- train/validation/test must be chronological;
- the same market event should not leak into multiple splits through near-duplicate windows;
- keep supervision separate from model inputs.

## 3. Render images deterministically

For visual fine-tuning, the renderer is part of the dataset definition.

Freeze and record:

- chart width/height;
- number of bars shown;
- timeframe order;
- candle style;
- overlays/indicators;
- axis behavior;
- colors if semantically meaningful;
- renderer version.

If the renderer changes materially, treat the result as a new dataset version.

## 4. Freeze a base model revision

Before training, record the exact base checkpoint.

Example metadata:

```yaml
model_id: OpenGVLab/InternVL3_5-2B
revision: <exact commit or snapshot>
precision: bf16
attention_backend: sdpa
```

Do not rely only on a moving `main` or `latest` revision.

Also record the base-model license and whether redistributed adapters are permitted.

## 5. Start with parameter-efficient fine-tuning

For consumer GPUs, LoRA/PEFT-style training is usually a better starting point than full-model fine-tuning.

A common pattern is:

```text
base VLM
  - visual backbone frozen
  - language/model blocks frozen except LoRA targets
  - multimodal projector optionally trainable
  - LoRA on selected attention/MLP projections
```

This can reduce VRAM and make experimentation practical on 8–24 GB consumer GPUs, depending on model size and image/token settings.

Exact target modules are architecture-specific. Do **not** copy target names blindly between InternVL, Qwen and Gemma.

## 6. Use a replay/curriculum strategy when extending an existing reader

When adapting an already useful model to a new task or new multi-timeframe layout, training only on the new task can cause forgetting.

A simple strategy is to mix:

```text
old-task replay examples
+
new-task examples
```

The ratio is experiment-specific. The goal is to learn the new representation while preserving previously validated capabilities.

Always evaluate the old tasks again after training.

## 7. Response-only supervision

For instruction/chat-style VLM fine-tuning, compute loss on the desired assistant response rather than training the model to reproduce the whole prompt when the training stack supports it.

This keeps the optimization focused on the structured answer.

Example target:

```json
{
  "direction": "long",
  "regime": "trend",
  "ambiguous": false
}
```

Prefer short structured outputs when the task is classification/state extraction. Long prose increases decoding cost and makes evaluation harder.

## 8. Run a real optimizer smoke test

Before committing hours of GPU time, prove that training actually changes the intended parameters.

A good smoke test should verify:

- forward pass succeeds;
- loss is finite;
- gradients are finite;
- expected trainable tensors receive gradients;
- an optimizer step changes expected weights;
- frozen weights stay frozen;
- VRAM/RAM are within budget.

A process that merely runs without OOM is not enough.

## 9. Prove checkpoint/resume before the long run

A serious training run should be resumable.

Checkpoint at least:

- trainable weights;
- optimizer state;
- scheduler state if used;
- training step;
- random-number-generator state when practical;
- dataset/configuration manifest.

Test resume deliberately before starting a multi-hour run.

Recommended workflow:

```text
start training
 -> save checkpoint after 1 real step
 -> reload checkpoint
 -> confirm weights/optimizer/step state
 -> only then approve full run
```

## 10. Estimate runtime from measured work

Do not estimate a full run from theory alone.

Measure several real training groups/steps and calculate:

```text
seconds per optimizer step
x remaining optimizer steps
+ safety margin
```

Record:

- batch size;
- gradient accumulation;
- image count/resolution;
- precision;
- GPU model;
- peak VRAM;
- system RAM;
- estimated total time.

This lets contributors decide whether to run locally or use a cloud GPU.

## 11. Example configuration skeleton

A generic experiment configuration could look like:

```yaml
experiment: market_reader_v1
seed: 20261006

model:
  family: internvl
  model_id: <upstream model>
  revision: <exact revision>
  precision: bf16
  freeze_vision: true

adapter:
  method: lora
  rank: 16
  alpha: 32
  dropout: 0.05
  target_modules:
    - <architecture-specific module names>

training:
  epochs: 1
  micro_batch_size: 1
  gradient_accumulation: 4
  learning_rate: 0.000005
  checkpoint_every_steps: 100

input:
  images_per_sample: 3
  layout: fast_middle_slow
  renderer_version: v1

evaluation:
  freeze_validation_before_training: true
  keep_test_closed: true
```

This is an example structure, not a recommended universal set of hyperparameters.

## 12. Evaluate recognition before economic value

A market reader should first be evaluated on the task it was trained to perform.

Examples:

- macro-F1;
- class-level precision/recall;
- confusion matrix;
- structured-output validity;
- agreement with reference labels;
- behavior on ambiguous cases.

Only after the reading/state output is frozen should a downstream trading policy evaluate economic performance.

This prevents the model from being selected only because a particular backtest happened to look profitable.

## 13. Keep economic evaluation strategy-specific

A generic visual reader does not know the correct exit policy for every trading system.

Preserve model outputs so downstream researchers can test different policies without retraining the VLM.

For asymmetric systems, evaluate:

- R distribution;
- expectancy;
- profit factor;
- drawdown;
- average winner / loser;
- positive tail such as `+2R`, `+3R`, `+4R+`;
- stability by year/symbol/regime.

Do not optimize only for win rate.

## 14. Comparing different base models fairly

If comparing InternVL, Qwen, Gemma or another family, keep constant wherever possible:

```text
same train records
same validation records
same chart images
same labels
same split boundaries
same output schema
same evaluation code
same economic policy
```

Each family receives its **own** LoRA/PEFT adapter. Learned adapters are not portable between unrelated architectures.

Compare both quality and cost:

- recognition quality;
- training time;
- inference latency;
- VRAM/RAM;
- structured-output reliability;
- batch equivalence;
- checkpoint size;
- hardware cost.

## 15. Local GPU vs cloud GPU

Use the smallest sensible resource for each stage.

```text
CPU/VPS
  -> data preparation
  -> deterministic features
  -> audits
  -> lightweight baselines

consumer GPU
  -> small VLM inference
  -> LoRA smoke tests
  -> small/medium fine-tuning

cloud GPU
  -> larger model families
  -> parallel model arena
  -> experiments exceeding local VRAM/time budget
```

A cloud GPU should not spend expensive time doing work that a CPU machine could prepare beforehand.

## 16. What to commit to Git

Good to commit:

- code;
- configs;
- small synthetic examples;
- manifests;
- aggregate metrics;
- documentation;
- tiny fixtures required by tests.

Usually do not commit:

- base-model weights;
- large LoRA checkpoints;
- licensed/raw historical datasets;
- private strategy labels;
- generated image banks with unclear redistribution rights;
- API keys or broker credentials.

Store large artifacts separately and publish them only when their licenses allow it.

## 17. Suggested first public adapter experiment

A practical first community milestone is:

1. choose one small openly usable VLM;
2. create a tiny synthetic/public multi-timeframe dataset;
3. implement its framework adapter;
4. run inference on 5-20 samples;
5. fine-tune a small LoRA if licensing/hardware permit;
6. prove checkpoint/resume;
7. publish hardware and runtime results;
8. keep the experiment small enough that another contributor can reproduce it.

The goal of the first experiment is not maximum profitability or maximum model size. It is a clean end-to-end path that others can extend.

See [Model adapters](MODEL_ADAPTERS.md), [Data sources](DATA_SOURCES.md), and [Project status](PROJECT_STATUS.md).