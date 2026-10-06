# Contributing

Thanks for considering a contribution to Multimodal Market AI.

The project is intentionally open to researchers, traders, ML engineers, students and hobbyists using very different hardware and market ideas. You do not need access to expensive GPUs to contribute.

## Good contribution areas

Useful contributions include:

- causal multi-timeframe utilities;
- public-data connectors with clear licensing;
- chart rendering;
- VLM adapters;
- lower-VRAM inference or fine-tuning;
- CPU baselines;
- sequence models;
- typed market-state extensions;
- caching/checkpointing;
- leakage tests;
- Windows/Linux/ROCm support;
- reproducible hardware benchmarks;
- documentation and examples;
- bug fixes.

See also:

- [Architecture](docs/ARCHITECTURE.md)
- [Trading system patterns](docs/TRADING_SYSTEM_PATTERNS.md)
- [Research environment](docs/RESEARCH_ENVIRONMENT.md)
- [Benchmarking guide](docs/BENCHMARKING.md)
- [Roadmap](docs/ROADMAP.md)

## Ground rules

1. **No future leakage.** If a model sees information unavailable at the decision timestamp, the experiment is invalid.
2. **Do not hide assumptions.** State timestamp semantics, split rules, transaction costs, targets and model revisions.
3. **Correctness before speed.** Faster batching or quantization is useful only when its effect on outputs is documented.
4. **Do not upload restricted data.** Contributors are responsible for redistribution rights.
5. **Do not upload credentials or personal account data.**
6. **Do not claim guaranteed profitability.** Report evidence and limitations.
7. **Keep strategy-specific logic modular.** The public core should remain reusable across different research systems.

## Development setup

```bash
git clone https://github.com/bobbonauta/Multimodal-Market-AI.git
cd Multimodal-Market-AI
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

## Pull requests

A useful PR should explain:

- what problem it solves;
- what changed;
- how it was tested;
- whether outputs changed;
- hardware/software used when performance is involved;
- any new dependency or license implication.

For model integrations, include the exact model repository and revision when possible.

For benchmark PRs, follow [docs/BENCHMARKING.md](docs/BENCHMARKING.md).

## AI-assisted contributions

AI coding assistants are welcome. The project itself has used Claude Code, OpenAI Codex and ChatGPT as research/engineering assistants.

AI-generated code is not exempt from review. Contributors remain responsible for:

- understanding what the code does;
- checking licenses and provenance;
- running tests;
- avoiding secrets and private data;
- verifying causal correctness;
- describing limitations accurately.

## Small PRs are welcome

You do not need to build a complete model backend. A useful test, a Windows fix, a benchmark from an unusual GPU, better documentation, a reproducible bug report or a small optimization can all be valuable.
