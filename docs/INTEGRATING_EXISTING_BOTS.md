# Connect an existing bot or EA — simple guide

This page is for people who already have a trading bot, EA or backtester.

The main idea is simple:

> **Do not rewrite your bot. Let it keep doing its job. Send only the information needed for research to this framework.**

## 1. Where your bot fits

The project uses four operational jobs:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

An existing bot can plug in at different points.

Example:

```text
YOUR BOT
   |
   | exports a timestamped event/state
   v
ACQUIRE / EXTRACT adapter
   |
   v
DECIDE with rules or model
   |
   v
APPLY as read-only result
```

Your bot does not need to reveal how its private rules work.

## 2. The small bridge

Think of the bot and this project as two separate boxes.

```text
YOUR BOT OR FROZEN CORE
   |
   | sends a small record
   v
BRIDGE
   |
   | validates ID, time and availability
   v
THIS PROJECT / EXTERNAL CONSUMER
   |
   v
RESULT FILE / SCORE / REPORT
```

At first, the result should be **read-only**. It should not place trades.

The bridge should transport meaning, not recreate the whole strategy.

## 3. What should the bot send?

At minimum, one row should contain:

| field | simple meaning |
|---|---|
| `event_id` | a unique name for this event |
| `decision_ts` | the exact time when the event/decision existed |
| `symbol` | the market or instrument |
| your own values | information your bot already knew at that time |

Example:

```csv
event_id,decision_ts,symbol,system_score,state_a,state_b
x001,2026-01-01T10:07:00Z,SYNTH,0.62,1.4,-0.2
x002,2026-01-01T10:10:00Z,SYNTH,0.47,1.1,0.3
```

You do **not** need to explain how private fields were calculated.

Do not export passwords, API keys or account secrets.

## 4. Missing optional values must stay missing

If your frozen core has an optional field that is not available yet, do not invent a value to complete the row.

```text
available now   -> send it
not available   -> keep it empty/unavailable
available later -> do not send it as if it existed now
```

The availability time matters as much as the value.

## 5. If your bot is written in Python

Python bots can pass a table directly to the integration helper.

```python
from multimodal_market_ai.integration import attach_causal_market_context

joined = attach_causal_market_context(bot_events, closed_bars)
```

The helper:

1. checks unique event IDs;
2. checks event time;
3. finds the latest already-closed market bar;
4. attaches that causal context;
5. refuses to use a future bar.

Your private columns remain unchanged.

## 6. If your bot is an MT4 or MT5 EA

The EA does not need Python inside it.

A simple research bridge can use:

```text
MT4 / MT5 EA
    |
    v
CSV / JSON / SQLite / IPC
    |
    v
Python research process
    |
    v
read-only result
```

A generic row could contain:

```text
event_id,timestamp,symbol,event_type,state_1,state_2
```

Then Python can:

1. read the row;
2. verify identity and time;
3. attach only causal data;
4. run a deterministic/statistical/AI model;
5. write a separate result.

## 7. Freeze one canonical core

If you are rebuilding part of a large bot as a deterministic system, avoid maintaining two independent copies of the same logic.

A safer pattern is:

```text
one canonical deterministic core
        |
        | frozen output record
        v
bridge / EA / service
```

Before freezing the core, use replay and prefix-invariance checks.

Read: [Deterministic freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md).

## 8. Start with old data before live data

A safer order is:

```text
old bot events
 -> check IDs and times
 -> attach causal market context
 -> test deterministic replay
 -> freeze the core/contract
 -> build outcomes separately
 -> split by time
 -> simple baseline
 -> optional AI
 -> read-only live test
```

This finds errors when nothing can affect real orders.

## 9. Keep responsibilities separate

### Your bot/private core owns

- private strategy rules;
- proprietary indicators;
- candidate/setup rules;
- any private internal state;
- execution logic and broker/account settings.

### This framework can own

- timestamp checks;
- market-data alignment;
- dataset IDs and hashes;
- train/validation/test separation;
- leakage checks;
- deterministic signal combination;
- reproducibility/freeze checks;
- model comparison;
- cache/resume tools;
- read-only live validation.

## 10. You can rebuild only the part you want

Maybe your old bot has a large signal section but you want a smaller auditable version.

Export or recalculate a few replaceable signals:

```text
signal A
signal B
signal C
```

Then use:

```python
from multimodal_market_ai.deterministic import combine_directional_signals

result = combine_directional_signals(
    data,
    ["signal_a", "signal_b", "signal_c"],
    policy="majority",
)
```

You can map the final directional result to a separate decision layer such as `LONG / SHORT / WAIT`.

## 11. What can AI do after the bot is connected?

AI does not need to replace the bot.

It can be tested as:

- a candidate ranker;
- a quality score;
- a market-context reader;
- an anomaly detector;
- a visual chart reader;
- a risk or uncertainty estimate;
- a continuation/deterioration estimate after an event already exists.

These are different research targets. Keep their meaning separate.

If AI adds nothing useful, leave it out.

## 12. What is a read-only live test?

The model watches incoming data and writes its answer, but cannot place an order.

Check:

- Does every event arrive once?
- Are timestamps correct?
- What happens after restart?
- Does the provider revise old bars?
- Does a frozen offline event reproduce live?
- Is latency acceptable?

Read-only validation proves transport and causality behavior, not profitability.

## 13. Common mistakes to avoid

Do not:

- use future information in a feature;
- silently discard unmatched events;
- invent unavailable optional fields;
- rebuild strategy logic independently inside the bridge;
- reuse stale caches;
- repeatedly open the final holdout;
- compare outputs before confirming input fingerprints;
- assume AI must improve a mature bot.

More examples: [Lessons learned](LESSONS_LEARNED.md).
