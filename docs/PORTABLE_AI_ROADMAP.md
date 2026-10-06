# Portable Mini AI roadmap

This roadmap focuses on the project's teacher-to-student direction: use capable AI systems to create high-quality supervision, then compress useful behaviour into smaller models that can run on widely available hardware.

## Phase A — Teacher outputs

- define a stable multimodal input schema;
- collect causal teacher outputs from one or more model families;
- normalize outputs into compact structured fields;
- preserve teacher identity, revision, prompt/config and decoding settings;
- store disagreement and uncertainty rather than hiding it;
- keep future/outcome information outside teacher inputs.

## Phase B — Structured state

- convert teacher and deterministic outputs into a typed `MarketState`;
- separate exact calculations from qualitative interpretation;
- version the state schema;
- make state records cacheable and reproducible;
- preserve enough provenance to regenerate each state.

## Phase C — Student models

Compare several lightweight students on exactly the same examples:

- logistic / linear baselines;
- tree and gradient-boosting models;
- small MLPs;
- compact sequence models;
- lightweight VLM adapters;
- small language/state models;
- direct classification heads that avoid long autoregressive decoding.

## Phase D — Compression

For promising students, test:

- LoRA / QLoRA;
- quantization;
- pruning where appropriate;
- feature distillation;
- representation distillation;
- ONNX / TensorRT / OpenVINO or other deployment formats;
- CPU and low-VRAM inference.

## Phase E — Retention tests

Measure how much teacher capability survives compression:

```text
teacher quality
    vs
student quality
    vs
student cost
```

Track:

- macro / per-class metrics;
- teacher/student disagreement;
- latency;
- throughput;
- RAM / VRAM;
- energy/cost where measurable;
- robustness across symbols, assets and timeframes.

## Phase F — Deployment tiers

The project should eventually document practical tiers such as:

```text
Tier 0  CPU only
Tier 1  4–8 GB VRAM
Tier 2  8–12 GB VRAM
Tier 3  16–24 GB VRAM
Tier 4  cloud / workstation teacher
```

A user should be able to identify which components can run locally and which require a larger teacher model.

## Phase G — Community model zoo

If licensing permits, contributors may publish:

- adapter recipes;
- benchmark manifests;
- compact student checkpoints;
- quantized variants;
- task-specific heads;
- teacher/student comparison reports.

Every published artifact should identify its base model, training source, license, task, hardware and reproducible evaluation protocol.
