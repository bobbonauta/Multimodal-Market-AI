# Benchmarking guide

Multimodal Market AI welcomes benchmark results from consumer PCs, workstations, CPU-only servers and cloud GPUs. The goal is not to build a leaderboard for its own sake, but to understand what kinds of multimodal market research are practical on real hardware.

## Minimum information for a useful benchmark

Please report:

- CPU model and logical/core count;
- GPU model and VRAM, if used;
- system RAM;
- operating system;
- Python version;
- relevant framework versions (`torch`, `transformers`, CUDA/ROCm, etc.);
- exact model repository and revision/commit when applicable;
- precision/quantization;
- input shape, image count and sequence/token limits;
- batch size and gradient accumulation;
- whether KV cache, gradient checkpointing, SDPA/FlashAttention or other accelerators were enabled;
- number of examples / optimizer steps;
- wall-clock time;
- peak process RAM and peak GPU memory where measurable;
- command or configuration needed to reproduce the run.

## Correctness before speed

A faster path should not be called equivalent unless output equivalence has actually been measured.

Autoregressive multimodal models can change output under batching, different kernels, precision changes or different attention implementations even when the same weights and inputs are used. Benchmark pull requests should therefore distinguish clearly between:

- **throughput-only experiments**;
- **numerically equivalent optimizations**;
- **task-equivalent optimizations**;
- **non-equivalent but potentially useful approximations**.

## Suggested result format

```yaml
hardware:
  cpu: AMD Ryzen 7 5700X3D
  gpu: NVIDIA RTX 4070 SUPER 12GB
  ram_gb: 64
software:
  os: Windows
  python: 3.11.x
  torch: x.y.z
  transformers: x.y.z
  cuda: 12.x
model:
  name: example/model
  revision: commit-or-tag
  precision: bf16
workload:
  task: inference
  images_per_case: 3
  image_size: 448
  cases: 100
  batch_size: 1
results:
  seconds_per_case: 0.0
  cases_per_second: 0.0
  peak_vram_gib: 0.0
  peak_ram_gib: 0.0
correctness:
  reference: serial-greedy
  compared_cases: 100
  exact_match_cases: 100
notes: >
  Anything needed to reproduce or interpret the result.
```

## What not to submit as a benchmark

Avoid benchmark claims based only on screenshots or undocumented notebook state. Results that cannot be reproduced can still be discussed in an issue, but they should not be used as reference numbers in project documentation.
