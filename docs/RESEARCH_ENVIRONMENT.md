# Reference research environment

This document records the hardware and tooling that have been used during the research that motivated Multimodal Market AI. These are **reference configurations, not minimum requirements**.

The project is intentionally designed so that useful work can be done on ordinary CPU machines and consumer GPUs. Contributors are encouraged to publish results from different hardware so the community can build realistic performance expectations.

## Main local research workstation

A large part of the current multimodal prototyping has been performed on a normal consumer desktop rather than a datacenter machine:

| Component | Reference system |
|---|---|
| CPU | AMD Ryzen 7 5700X3D |
| GPU | NVIDIA GeForce RTX 4070 SUPER, 12 GB VRAM |
| System RAM | 64 GB DDR4-3600 |
| OS | Windows desktop environment |
| Python | 3.11.x in the original research environment |
| CUDA toolkit used in the research environment | 12.6 |
| NVIDIA runtime observed during research | CUDA 12.7-capable driver stack |

This machine has been sufficient for substantial experimentation with small/medium vision-language models, LoRA-style adaptation, causal data preparation, chart rendering, inference caching and numerical-model development.

### Example local multimodal workload

One reference experiment used an InternVL3.5-2B-class multimodal model with BF16/SDPA and trainable adapters while keeping the visual backbone frozen.

Observed during the experiment:

- approximately 5.6 GiB CUDA memory allocated at peak by the training process;
- approximately 7.0 GiB total GPU memory observed through `nvidia-smi`, including desktop overhead;
- approximately 4.8 GiB process RAM;
- a 7,000-example / 1,750-optimizer-step fine-tuning plan estimated at roughly 3 h 50 min nominal and about 4 h 35 min with a 20% planning margin;
- checkpoint/resume was tested so a long local run did not need to be treated as an all-or-nothing job.

These numbers are not promises: model versions, sequence lengths, image counts, precision, attention implementation, operating system and background applications can change memory and speed substantially.

## CPU-only VPS used for research

A separate CPU-only VPS has also been useful for work that does not require GPU acceleration:

| Component | Reference VPS |
|---|---|
| CPU | 6 vCPU AMD EPYC-class |
| RAM | 12 GB |
| GPU | None |
| OS | Windows Server 2025 |

CPU tasks have included dataset preparation, deterministic feature/state construction, evaluation, aggregation, audit scripts and lightweight tabular/sequence-model experiments.

In one historical CPU-only model arena, around two dozen tabular/sequence model variants completed in a little over two hours total. The heaviest individual process in that run stayed below about 1 GB RSS. This is one reason the project separates CPU-suitable deterministic/numerical work from expensive multimodal GPU work.

## Cloud GPU research

Cloud GPUs have been used only when a model or experiment did not fit sensibly on the local 12 GB GPU. Prior research included runs on NVIDIA RTX 4090-class 24 GB GPUs and RTX PRO 6000-class 96 GB GPUs.

The public project should make cloud use optional. The preferred workflow is:

1. prepare and validate data locally or on CPU;
2. run small smoke tests;
3. estimate time and VRAM before a full run;
4. use cloud GPU only for the part that genuinely needs it;
5. checkpoint and preserve outputs so expensive work is not repeated unnecessarily.

## AI-assisted engineering and research

The research and software-development workflow has itself been multimodal and multi-agent.

Human maintainers define the domain problem, research constraints, evaluation rules and acceptance criteria. AI coding/reasoning tools have been used as assistants for implementation, review and auditing, including:

- **Claude Code** — implementation assistance, code review, experiment scripting and long-form repository work;
- **OpenAI Codex** — independent code/repository analysis, implementation assistance, testing and audit work;
- **ChatGPT** — architecture discussion, independent review, research planning and cross-checking of experiment interpretation.

This is deliberate. One objective of the project is to explore whether multiple AI assistants can help build and audit a complex research system while the repository, tests and reproducible artifacts remain the source of truth.

AI-generated proposals are **not automatically accepted as correct**. Important changes should be checked through code review, deterministic tests, causal/leakage audits and reproducible experiment outputs. Contributors are free to use any coding assistant or no assistant at all.

## Why publish hardware information?

We want contributors to be able to answer practical questions before investing time:

- Can I run the causal/numerical stack on CPU only?
- Can I test the visual path on 8–12 GB VRAM?
- Which models fit on my GPU?
- Does a lower-VRAM implementation preserve equivalent outputs?
- How much faster is one GPU generation than another?
- Are Windows, Linux, CUDA and ROCm results comparable?

For that reason, benchmark pull requests should include hardware, OS, software versions, model revision, precision, batch size, image/input shape and enough command/configuration information to reproduce the measurement.

See [BENCHMARKING.md](BENCHMARKING.md) for the proposed reporting format.
