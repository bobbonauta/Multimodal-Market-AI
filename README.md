# Multimodal Market AI

**Add AI to an existing trading bot, or build a simple deterministic system from scratch and improve it step by step.**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Project status](https://img.shields.io/badge/status-early%20alpha-orange.svg)](#project-status)

## In one sentence

This repository helps you **connect market data, simple rules, existing bots and AI without mixing everything together or accidentally using future information**.

You can use it in two ways:

```text
A) I already have a bot
   my bot -> this framework -> tests / models / AI

B) I do not have a bot
   market data -> my simple rules -> deterministic model -> tests / models / AI
```

You do not need to publish your private strategy.

> This is a research and engineering framework. It is not a ready-made trading strategy, a signal service or a promise of profit.

## If you already have a bot

You do **not** need to rewrite thousands of lines of code.

Your existing EA, Python bot or backtester can keep doing what it already does.

It can export a small row such as:

```text
event ID
exact time
symbol
its own state or features
```

This project can then add market context that was really available at that moment, run tests, build datasets and compare models.

Simple picture:

```text
existing EA / bot
      |
      v
small integration adapter
      |
      +--> causal market data
      +--> extra numerical context
      +--> optional chart / visual AI
      |
      v
simple model or AI model
      |
      v
score / ranking / analysis / read-only live test
```

Start here: [Integrating an existing bot or EA](docs/INTEGRATING_EXISTING_BOTS.md).

## If you do not have a bot yet

You can build a simple system directly inside this repository.

The easiest first step is a **deterministic model**.

“Deterministic” means:

> Same data + same rules = same answer.

A simple system may use several small signals.

For example:

```text
rule A: trend
rule B: momentum
rule C: structure
        |
        v
majority / unanimous / weighted vote
        |
        v
final deterministic signal
```

Every rule is replaceable. You can remove one rule, add another, recalculate the model and compare the result.

Read the simple explanation: [Multi-signal and deterministic model](docs/MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md).

Run the public example:

```bash
python examples/deterministic_multi_signal.py
```

## What is a multi-signal system?

A **signal** is one clue.

A **multi-signal system** uses several clues instead of trusting only one.

Imagine three people looking at the weather:

- one sees dark clouds;
- one feels strong wind;
- one hears thunder.

Each clue says something. The final decision uses the clues together.

A market system can do the same thing with independent rules.

In the public helper:

- `+1` means a rule points one way;
- `-1` means it points the other way;
- `0` means that rule has no opinion right now.

The project can combine these signals with:

- **majority** — more votes win;
- **unanimous** — all active votes must agree;
- **weighted** — some rules count more than others.

The exact indicators and rules are yours.

## Why build a deterministic model before AI?

Because AI should have something simple to beat.

A good order is:

```text
1. simple rules
2. deterministic model
3. simple statistical model
4. optional multimodal / visual AI
5. compare them on the same data
```

If a simple model works as well as a much larger AI, the larger AI may not be worth the cost.

## What this project can do

The public code already includes tools for:

- joining market data to the exact time of a decision;
- building higher timeframes without looking into the future;
- checking that a feature really existed when the decision was made;
- keeping train, validation and test periods separate;
- detecting missing, duplicate or changed records;
- sealing files with hashes so stale results are not reused by mistake;
- resuming long jobs safely;
- connecting an existing bot to the research pipeline;
- combining simple directional signals into a deterministic model;
- comparing simple baselines with more expensive AI models;
- testing live data in read-only mode before execution is ever considered.

## A simple full path

A complete experiment can look like this:

```text
market data
   |
   v
simple signals or existing bot events
   |
   v
deterministic model / candidate list
   |
   v
causal audit
   |
   v
train / validation / test split
   |
   +--> simple numerical baseline
   |
   +--> optional visual / multimodal model
   |
   v
fair comparison on the same rows
   |
   v
read-only live validation
```

Nothing forces you to use every step.

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

The event at `10:07` can see the bar closed at `10:05`. It cannot see the bar that closes at `10:10`, because that bar was still in the future at `10:07`.

## Deterministic model example

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

print(result)
```

You can replace `trend`, `momentum` and `structure` with your own rules. The rest of the pipeline can stay the same.

## What does “causal” mean?

It means **do not use information from the future**.

Example:

```text
Decision time: 10:07
Bar closed at: 10:05  -> allowed
Bar closed at: 10:10  -> not allowed yet
```

This sounds obvious, but it is one of the easiest mistakes to make when working with historical data.

## What does “baseline” mean?

A **baseline** is a simple model used as a reference.

Example:

```text
simple deterministic model = baseline A
simple numerical model     = baseline B
large visual AI            = model C
```

If model C does not improve on A or B, more complexity may not help.

## What does “read-only live test” mean?

The model watches live data and writes its answer, but it **cannot place or change orders**.

This lets you check:

- timestamps;
- missing data;
- restarts;
- duplicate events;
- latency;
- whether live behavior matches the offline tests.

Only after that should a separate project decide whether a model output may affect execution.

## Mistakes we already made so you do not have to repeat them

The repository also records errors found during internal research.

Examples:

- mixing a long-lived state with a short-lived confirmation;
- treating missing information like a real signal;
- comparing two columns that had similar names but different meanings;
- reusing an old cache after one of its inputs changed;
- training preprocessing on validation/test data;
- letting a future outcome cross a time split;
- using audit-only future information as a model feature;
- checking the final test set too many times;
- spending GPU time before testing a cheap baseline;
- assuming a visual model is useful just because it contains some signal.

See [Failure modes and lessons learned](docs/LESSONS_LEARNED.md).

## Research results we can share safely

Internal work has shown several general lessons:

- fixing data or target definitions can change earlier conclusions;
- simple numerical models can contain useful out-of-sample information;
- a visual representation can contain information but still add no useful value beyond a simpler model;
- better prediction metrics do not automatically mean a profitable system;
- expensive model work should be resumable and tied to exact data IDs;
- post-decision or trade-management questions can be studied separately from entry questions.

Private strategy rules, private datasets and private economic results are not published here.

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

## Main rules of the project

- **Bring your own strategy** — or build a simple public deterministic one here.
- **Do not look into the future** — every input must exist at decision time.
- **Keep pieces separate** — data, signals, labels, models and evaluation should not be mixed together.
- **Change one piece at a time** — then measure what changed.
- **Simple before expensive** — baseline first, GPU later.
- **Fail closed** — bad or missing data should stop the pipeline instead of being silently ignored.
- **AI must earn its place** — if it adds nothing, do not force it into the system.

## Project status

**Early alpha.** The causal core, deterministic combiner and existing-bot integration pieces are usable research building blocks. More public data connectors, model adapters and complete end-to-end examples are still being added.

## Documentation

Start with these three pages:

1. [Multi-signal and deterministic model](docs/MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md)
2. [Integrating an existing bot or EA](docs/INTEGRATING_EXISTING_BOTS.md)
3. [Failure modes and lessons learned](docs/LESSONS_LEARNED.md)

More technical material:

- [Project status and research evidence](docs/PROJECT_STATUS.md)
- [Historical data sources](docs/DATA_SOURCES.md)
- [Model adapters](docs/MODEL_ADAPTERS.md)
- [Fine-tuning guide](docs/FINETUNING_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Example trading-system patterns](docs/TRADING_SYSTEM_PATTERNS.md)
- [Reference research environment](docs/RESEARCH_ENVIRONMENT.md)
- [Benchmarking](docs/BENCHMARKING.md)
- [Roadmap](docs/ROADMAP.md)
- [Repository governance](docs/REPOSITORY_GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)

## Disclaimer

This software is for research and education. Financial markets involve risk. Nothing in this repository is investment advice or a guarantee of future results.

## License

Code in this repository is licensed under the Apache License 2.0. Datasets, model weights and third-party models may have separate licenses.
