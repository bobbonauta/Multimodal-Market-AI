# Suggested reading path

New contributors can read the project in this order:

1. `README.md` — project purpose and quick start.
2. `docs/PROJECT_STATUS.md` — what has already been demonstrated.
3. `docs/DATA_SOURCES.md` — how historical market data should be collected and prepared.
4. `docs/ARCHITECTURE.md` — deterministic, multimodal and state layers.
5. `docs/MODEL_ADAPTERS.md` — how model-family adapters are organized.
6. `docs/FINETUNING_GUIDE.md` — how to build a reproducible adaptation run.
7. `docs/MINI_AI_DISTILLATION.md` — how large AI teachers can produce supervision for portable Mini AI students.
8. `docs/TEACHER_STUDENT_EXAMPLE.md` — practical teacher/student workflow.
9. `docs/PORTABLE_AI_ROADMAP.md` — deployment and compression roadmap.
10. `docs/BENCHMARKING.md` — how to report hardware and runtime results.
11. `docs/TRADING_SYSTEM_PATTERNS.md` — example strategy families for experimentation.

The central idea is not to make every user run the largest available AI model. The project aims to make expensive AI useful as a **teacher**, while progressively moving reusable capabilities into smaller specialist models that can run on ordinary machines.
