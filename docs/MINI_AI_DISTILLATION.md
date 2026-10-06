# From large AI systems to portable Mini AI

One of the central research goals of **Multimodal Market AI** is to use larger and more capable AI systems as teachers, then extract the reusable knowledge they produce into smaller specialist models that can run on ordinary hardware.

The project is not limited to training one large model. The intended workflow is closer to:

```text
large / capable teacher models
        |
        +-- visual interpretation
        +-- structured explanations
        +-- market-state labels
        +-- numerical / categorical outputs
        +-- ambiguity / confidence information
        v
curated causal training dataset
        v
small specialist models
        |
        +-- compact VLM adapters
        +-- tabular / sequence models
        +-- lightweight MLP / tree heads
        +-- distilled typed-state models
        +-- quantized local models
        v
CPU / consumer GPU / laptop / edge deployment
```

## Why this matters

Large multimodal models can be powerful teachers, but they are often too slow, expensive or memory-hungry to run over millions of historical market states or to deploy continuously on ordinary machines.

A smaller model does not need to reproduce everything the teacher knows. It only needs to reproduce the useful subset of behaviour required by a specific market task.

Examples:

- recognize a market regime;
- detect a structural phase;
- classify a multi-timeframe relationship;
- convert several chart/timeframe observations into a typed `MarketState`;
- rank candidate events;
- estimate whether a visual review is needed;
- reproduce a teacher's stable categorical interpretation without generating long text.

This can make a system dramatically cheaper and easier to deploy.

## What "extract knowledge" means here

The project uses **teacher-student / distillation-style research**, not direct copying of another model's weights.

Useful supervision can come from:

- structured outputs produced by a teacher model;
- human-reviewed labels generated with AI assistance;
- consensus between multiple teacher models;
- intermediate typed states;
- compact numerical summaries;
- chart-reading categories;
- confidence / disagreement labels;
- cached historical teacher outputs.

Those outputs can then become training examples for a smaller model, subject to the license and usage terms of every upstream model and dataset.

## A practical example

A large VLM may receive three synchronized charts and return a structured answer such as:

```json
{
  "higher_tf_state": "trend_up",
  "middle_tf_state": "pullback",
  "lower_tf_state": "reacceleration",
  "alignment": "partial",
  "ambiguity": 0.18
}
```

Instead of running that VLM forever, the project can preserve many such causal examples and train a much smaller model to reproduce this compact state directly.

The larger model remains useful as a **teacher, auditor or fallback**, while the smaller model becomes the normal runtime component.

## Multiple teachers

The framework is intentionally compatible with using more than one AI family.

For example:

```text
InternVL teacher ----+
Qwen-VL teacher -----+--> normalized supervision --> Mini AI
Gemma teacher -------+
Human review --------+
Numerical engines ---+
```

Different teachers can be strong at different subtasks. The goal is not to declare one universal winner, but to preserve useful capabilities and combine them into a smaller task-specific model where possible.

## Why typed state is important

A typed intermediate state reduces the amount of information a small model must learn.

Instead of feeding thousands of raw values or asking a small language model to understand long free-form explanations, the pipeline can convert observations into a compact representation:

```text
raw market data + charts
        v
teacher / deterministic readers
        v
MarketState
        v
small decision / recognition model
```

This also makes caching, auditing and model replacement easier.

## Deployment targets

The long-term objective is to support useful Mini AI models on hardware such as:

- CPU-only VPS;
- consumer NVIDIA GPUs;
- AMD / ROCm systems;
- ordinary desktops;
- laptops;
- small local servers;
- potentially other low-resource or edge environments when model size allows it.

"Run everywhere" does not mean every model must run on every device. It means the architecture should allow expensive teacher work to be converted into smaller deployable components whenever the task permits it.

## What contributors can research

Useful contributions include:

- teacher-output dataset builders;
- teacher consensus / disagreement methods;
- knowledge-distillation losses;
- direct classification heads replacing autoregressive text generation;
- quantization experiments;
- LoRA / QLoRA recipes;
- feature and representation distillation;
- compact sequence models;
- student-model benchmarking;
- CPU inference optimization;
- model conversion / export;
- ONNX / TensorRT / OpenVINO / ROCm paths where licensing and compatibility allow;
- tests showing how much teacher quality is retained after compression.

## Evaluation

A Mini AI should not be accepted merely because it is smaller.

It should be compared with its teacher on:

- recognition quality;
- class-level metrics;
- calibration / confidence;
- disagreement cases;
- latency;
- RAM / VRAM;
- throughput;
- robustness across symbols and timeframes;
- downstream economic metrics where appropriate.

The project should preserve cases where the small model disagrees with the teacher, because those examples are especially useful for future training.

## Licensing and responsible use

Teacher outputs, model APIs, open weights and datasets can have different licenses and terms. Contributors are responsible for ensuring that a proposed teacher-student pipeline permits the intended use and redistribution.

This repository should never assume that outputs or weights from every AI system are freely redistributable.

The open-source framework provides the infrastructure; users choose compatible models and data sources for their own experiments.
