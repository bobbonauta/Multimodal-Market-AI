# Multimodal Market AI

**Add AI to an existing trading bot, or build a deterministic market system from scratch and improve it step by step.**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Project status](https://img.shields.io/badge/status-early%20alpha-orange.svg)](#project-status)

## In one sentence

This repository helps you **acquire market data, extract causal information, make a decision and safely pass that decision onward** without mixing strategy logic, AI, evaluation and execution into one opaque block.

You do not need to publish your private strategy.

> This is a research and engineering framework. It is not a ready-made trading strategy, a signal service or a promise of profit.

## The project now uses one simple operational pipeline

Everything fits inside four jobs:

```text
1. ACQUIRE
   get the market case that really exists now
        |
        v
2. EXTRACT
   calculate or import the useful information
        |
        v
3. DECIDE
   choose what to do now
        |
        v
4. APPLY
   send the decision to a safe output / bridge / execution layer
```

For a trading system, a public example of the decision stage is:

```text
LONG
SHORT
WAIT
```

`WAIT` means: do not perform LONG or SHORT yet.

This is different from:

- one small signal saying “I have no opinion”;
- a private internal state that may persist for longer;
- a missing/unavailable value.

Do not automatically combine those ideas into one variable.

Read: [Operational pipeline](docs/OPERATIONAL_PIPELINE.md).

## If you already have a bot

You do **not** need to rewrite thousands of lines of code.

Your existing EA, Python bot or backtester can keep doing what it already does.

It can export a small record such as:

```text
event ID
exact time
symbol
its own state / values
```

Then this project can attach only market context that really existed at that time, run audits, build datasets and compare models.

```text
YOUR BOT
   |
   v
small adapter / bridge
   |
   +--> causal market data
   +--> optional extra context
   +--> optional model / AI
   |
   v
read-only result / score / report
```

The bridge should transport the result. It should not secretly rebuild a second copy of your strategy.

Start here: [Integrating an existing bot or EA](docs/INTEGRATING_EXISTING_BOTS.md).

## If you do not have a bot yet

You can build a deterministic system directly inside this repository.

“Deterministic” means:

> Same data + same rules = same answer.

A simple public example can combine several small signals:

```text
rule A: trend clue
rule B: momentum clue
rule C: structure clue
        |
        v
majority / unanimous / weighted vote
        |
        v
deterministic result
```

Every rule is replaceable.

Read: [Multi-signal and deterministic model](docs/MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md).

Run:

```bash
python examples/deterministic_multi_signal.py
```

## A multi-signal system, explained simply

A **signal** is one clue.

Imagine three people looking at the weather:

- one sees dark clouds;
- one feels strong wind;
- one hears thunder.

Each clue says something. A final rule combines the clues.

In the public helper:

- `+1` = this rule points one way;
- `-1` = this rule points the other way;
- `0` = this rule is not voting right now.

The combiner supports:

- **majority** — more active votes win;
- **unanimous** — all active votes must agree;
- **weighted** — some rules count more than others.

A final `det_signal = 0` means the combiner did not choose either side. A trading application may map that result to `WAIT`; it is not automatically a third persistent market direction.

## Deterministic first, AI later

AI should have something simple and reproducible to beat.

The order is:

```text
build the deterministic/data path
        |
        v
prove it is causal and reproducible
        |
        v
freeze that version
        |
        v
compare simple and complex models fairly
```

A deterministic system is not considered stable only because it ran once.

The public freeze protocol checks ideas such as:

- adding future data must not rewrite old historical records;
- isolated runs should match sequential runs;
- inputs must be fingerprinted before outputs are compared;
- value changes must be separated from dtype/schema differences;
- unavailable fields must not be invented;
- the frozen core should be reused unchanged during model comparison.

Read: [Deterministic freeze protocol](docs/DETERMINISTIC_FREEZE_PROTOCOL.md).

## Research tools support the pipeline — they are not extra pipelines

The repository also contains:

- causal timestamp checks;
- higher-timeframe construction without future bars;
- feature-availability audits;
- exact record-ID checks;
- artifact hashes and seals;
- purged train/validation/test splitting;
- resumable caches;
- deterministic candidate manifests;
- simple-model baselines;
- optional visual / multimodal experiments;
- read-only forward-validation design.

They support the four operational jobs:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

A VLM, gradient-boosting model or other AI model is a candidate component, not a mandatory new stage.

## Fair model comparison

Do not choose the final model family first.

Once the pipeline and deterministic core are frozen, compare candidate models using the same:

- dataset;
- time split;
- inputs;
- target;
- metrics;
- deterministic/core pipeline.

If a more complex model does not improve the result, it does not need to be used.

## A simple full research path

```text
ACQUIRE
   |
   v
EXTRACT
   |
   v
DECIDE
   |
   v
APPLY read-only

Around those four steps:

causal audit
record IDs + hashes
train / validation / test
simple baseline
optional AI / VLM
fair comparison
forward validation
```

This keeps the operational system simple while still allowing serious research.

## Existing-bot example

```python
import pandas as pd

from multimodal_market_ai.integration import attach_causal_market_context

bot_events = pd.DataFrame(
    {
        "event_id": ["evt-1", "evt-2"],
        "decision_ts": ["2026-01-01T10:07:00Z", "2026-01-01T10:10:00Z"],
        "bot_state": [0.25, 0.62],
    }
)

bars = pd.DataFrame(
    {
        "open": [100.0, 101.0],
        "high": [102.0, 103.0],
        "low": [99.0, 100.0],
        "close": [101.0, 102.0],
    },
    index=pd.to_datetime(["2026-01-01T10:05:00Z", "2026-01-01T10:10:00Z"]),
)

joined = attach_causal_market_context(bot_events, bars)
print(joined)
```

The event at `10:07` can use the bar closed at `10:05`. It cannot use the bar that closes at `10:10`.

## Deterministic example

```python
import pandas as pd

from multimodal_market_ai.deterministic import combine_directional_signals

frame = pd.DataFrame(
    {
        "trend": [1, 1, -1],
        "momentum": [1, -1, -1],
        "structure": [0, 1, -1],
    }
)

result = combine_directional_signals(
    frame,
    ["trend", "momentum", "structure"],
    policy="majority",
)
```

Replace the three example rules with your own rules. The rest of the project can stay the same.

## What “causal” means

It means **do not use information from the future**.

```text
Decision time: 10:07
Bar closed at: 10:05  -> allowed
Bar closed at: 10:10  -> not allowed yet
```

## What “read-only” means

A read-only consumer watches data and records what the system would say, but it cannot place or modify orders.

Check:

- timestamps;
- missing data;
- duplicate events;
- restart behavior;
- historical revisions;
- latency;
- whether live outputs match the frozen offline logic.

Read-only validation is an engineering proof. It is not proof of profitability.

## Mistakes already documented

The repository records general mistakes found during internal research so other people do not need to repeat them.

Examples:

- confusing a persistent state with a temporary confirmation;
- confusing missing data with a real neutral answer;
- treating a rule-level `0` as the same thing as final `WAIT`;
- comparing fields with similar names but different meanings;
- reusing stale caches;
- allowing future outcomes to cross a time split;
- opening the final holdout repeatedly;
- running expensive models before a cheap baseline;
- adding new models or sub-pipelines before the basic pipeline is complete;
- comparing outputs before confirming the inputs are identical;
- allowing future-appended data to rewrite old deterministic records.

See: [Lessons learned](docs/LESSONS_LEARNED.md).

## Quick start

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
python examples/deterministic_multi_signal.py
python examples/existing_bot_integration.py
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
python examples\deterministic_multi_signal.py
python examples\existing_bot_integration.py
```

## Main rules

- **One operational pipeline** — acquire, extract, decide, apply.
- **Bring your own strategy** — or build a deterministic one here.
- **Do not look into the future** — every input must exist at decision time.
- **Keep meanings separate** — signal abstention, WAIT, missing data and internal state are different concepts.
- **Freeze before final comparison** — stable data path and deterministic core first.
- **Compare models fairly** — same rows, split, inputs, target and metrics.
- **Simple before expensive** — baseline first, GPU later.
- **Fail closed** — missing required information should stop or defer the step, not be invented.
- **Bridge, do not duplicate** — external integration should transport a frozen result rather than reimplement the strategy.
- **AI must earn its place** — if it adds nothing useful, leave it out.

## Project status

**Early alpha.** The public deterministic combiner, causal helpers, integration adapter and research-safety primitives are usable building blocks. The four-stage operational pipeline and deterministic-freeze protocol are now documented; full public MT4/MT5 bridging, forward journals and model adapters remain ongoing work.

## Documentation

Start here:

1. [Operational pipeline](docs/OPERATIONAL_PIPELINE.md)
2. [Multi-signal and deterministic model](docs/MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md)
3. [Deterministic freeze protocol](docs/DETERMINISTIC_FREEZE_PROTOCOL.md)
4. [Integrating an existing bot or EA](docs/INTEGRATING_EXISTING_BOTS.md)
5. [Lessons learned](docs/LESSONS_LEARNED.md)

More technical material:

- [Architecture](docs/ARCHITECTURE.md)
- [Public research workflow](docs/PUBLIC_WORKFLOW_SYNC.md)
- [Project status](docs/PROJECT_STATUS.md)
- [Historical data sources](docs/DATA_SOURCES.md)
- [Model adapters](docs/MODEL_ADAPTERS.md)
- [Fine-tuning guide](docs/FINETUNING_GUIDE.md)
- [Example trading-system patterns](docs/TRADING_SYSTEM_PATTERNS.md)
- [Experiment governance](docs/EXPERIMENT_GOVERNANCE.md)
- [Benchmarking](docs/BENCHMARKING.md)
- [Roadmap](docs/ROADMAP.md)
- [Repository governance](docs/REPOSITORY_GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)

## Disclaimer

This software is for research and education. Financial markets involve risk. Nothing in this repository is investment advice or a guarantee of future results.

## License

Code in this repository is licensed under the Apache License 2.0. Datasets, model weights and third-party models may have separate licenses.
