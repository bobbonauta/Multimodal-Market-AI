# Integrating an existing bot or EA

Multimodal Market AI is designed to sit **beside** an existing trading system. You do not need to rewrite a large EA or Python bot, and you do not need to publish the rules that make that system proprietary.

The integration boundary is deliberately small:

```text
existing system
   -> timestamped event / candidate / state
   -> causal context adapter
   -> audited dataset
   -> baseline and/or multimodal model
   -> score / context / estimate
   -> research, read-only monitoring, or optional feedback to the existing system
```

## 1. What the existing system should export

At minimum, export one row for each event you want the AI layer to study:

| field | purpose |
|---|---|
| `event_id` | stable unique identity |
| `decision_ts` | exact timestamp at which the event existed |
| `symbol` | instrument identifier |
| strategy-owned state/features | only values already known at `decision_ts` |

Optional fields can include the system's own candidate type, confidence, indicator values, regime labels or any private numerical state. The framework does not need to understand how those values were produced.

A generic CSV can therefore look like:

```csv
event_id,decision_ts,symbol,system_score,state_a,state_b
x001,2026-01-01T10:07:00Z,SYNTH,0.62,1.4,-0.2
x002,2026-01-01T10:10:00Z,SYNTH,0.47,1.1,0.3
```

Do **not** export account credentials, API keys or information that is not required by the experiment.

## 2. Python bots

A Python bot can pass a `pandas.DataFrame` directly to `attach_causal_market_context`.

```python
from multimodal_market_ai.integration import attach_causal_market_context

joined = attach_causal_market_context(bot_events, closed_bars)
```

The adapter preserves the original event fields and attaches only market bars that were closed by the event timestamp.

Use one instrument per call. Multi-instrument systems can group events by symbol and process each symbol against its own market series.

## 3. MT4 / MT5 EAs

An EA does not need Python embedded inside the trading logic. A low-coupling bridge is safer during research.

Recommended progression:

```text
EA
 -> append CSV / JSON / SQLite event journal
 -> Python watcher or scheduled importer
 -> causal context + model
 -> separate output file / database table
```

For MetaTrader, the EA can append one compact row only when something meaningful happens. A generic row might contain:

```text
event_id,timestamp_utc,symbol,event_type,state_1,state_2,...
```

The Python side can then:

1. normalize timestamps to UTC;
2. verify unique event IDs;
3. attach only closed market context;
4. add numerical or visual representations;
5. run a model;
6. write a separate result such as:

```json
{
  "event_id": "x001",
  "model_revision": "example-v1",
  "quality_score": 0.71,
  "risk_score": 0.29
}
```

The names above are examples, not required model outputs.

During development, keep the result **read-only**: log it, compare it with subsequent outcomes, and do not let it place or modify orders.

## 4. Historical integration first

Before live use, export historical decisions from the existing system and reconstruct the information that was actually available at each decision time.

Recommended sequence:

```text
historical events
 -> exact IDs + timestamps
 -> causal context attachment
 -> leakage audit
 -> labels/outcomes created separately
 -> purged temporal split
 -> naive baseline
 -> tabular baseline
 -> optional multimodal representation
 -> incremental-value comparison
```

The same event population and split should be used when comparing models. Otherwise a better score may simply come from evaluating different rows.

## 5. Keep the strategy and the AI layer separate

A useful boundary is:

**Strategy-owned**
- candidate creation;
- private rules;
- proprietary indicators/state;
- execution logic;
- account and broker configuration.

**Framework-owned**
- timestamp validation;
- causal market alignment;
- dataset identity/provenance;
- train/validation/test discipline;
- feature availability checks;
- model comparison;
- resumable inference/cache;
- reproducible evaluation.

This separation allows an open integration layer without publishing the strategy.

## 6. Possible AI roles

The framework does not force a single use case. An existing system can use a learned layer for research into:

- candidate ranking;
- quality or uncertainty scoring;
- market-context classification;
- anomaly detection;
- visual pattern representation;
- risk/deterioration estimation;
- post-decision continuation modelling;
- identifying cases where a deterministic system behaves differently across regimes.

A model should earn its place. Compare it against simple baselines and keep it out if it adds no useful information.

## 7. Read-only forward validation

After offline validation, connect the adapter to the live data flow but keep execution disabled.

Verify:

- timestamps and session boundaries;
- restart behavior and duplicate handling;
- data revisions;
- exact correspondence between observed events and model outputs;
- latency;
- whether model behavior remains consistent with offline evaluation.

Only after this stage should a project separately decide whether any model output may influence execution.

## 8. What not to do

Do not:

- let a historical label leak into the exported state;
- join on approximate row position when stable IDs exist;
- regenerate validation/test preprocessing statistics separately;
- silently drop unmatched events with an inner join;
- reuse a cache only because the file exists;
- tune repeatedly against the final holdout;
- assume an AI model must improve a mature deterministic system.

See [Failure modes and lessons learned](LESSONS_LEARNED.md) for the reasoning behind these rules.
