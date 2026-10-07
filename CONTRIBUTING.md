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
- [Experiment and AI-agent governance](docs/EXPERIMENT_GOVERNANCE.md)
- [Roadmap](docs/ROADMAP.md)

## Ground rules

1. **No future leakage.** If a model sees information unavailable at the decision timestamp, the experiment is invalid.
2. **Do not hide assumptions.** State timestamp semantics, split rules, transaction costs, targets and model revisions.
3. **Verify reused data against the current split.** Historical `TRAIN`/`FIT` labels are not enough: inspect actual timestamps and overlap before reusing replay buffers, caches or old training corpora.
4. **Preserve the final holdout.** Do not repeatedly inspect a protected final test period to tune or select weak candidates.
5. **Correctness before speed.** Faster batching or quantization is useful only when its effect on outputs is documented.
6. **Version operational decisions.** Protocol, agent-role, stop/resume and other experiment-governance changes must be committed and pushed before they are treated as active.
7. **Do not upload restricted data.** Contributors are responsible for redistribution rights.
8. **Do not upload credentials or personal account data.**
9. **Do not claim guaranteed profitability.** Report evidence and limitations.
10. **Keep strategy-specific logic modular.** The public core should remain reusable across different research systems.

For the full experiment protocol, including contamination vs non-independent evaluation, see [docs/EXPERIMENT_GOVERNANCE.md](docs/EXPERIMENT_GOVERNANCE.md).

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
- any new dependency or license implication;
- any train/validation/test boundary or data-provenance change;
- whether a protected holdout was accessed.

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

When several AI assistants are involved, prefer one active writer per branch/work tranche and use the others as reviewers or on separate branches. Record handoffs and changes of authority in Git before they take effect.

## Small PRs are welcome

You do not need to build a complete model backend. A useful test, a Windows fix, a benchmark from an unusual GPU, better documentation, a reproducible bug report or a small optimization can all be valuable.
