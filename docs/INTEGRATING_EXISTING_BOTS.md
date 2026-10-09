# Connect an existing bot or EA — simple guide

This page is for people who already have a trading bot, EA or backtester.

The main idea is simple:

> **Do not rewrite your bot. Let it keep doing its job. Send only the information needed for research to this framework.**

## 1. The small bridge between your bot and this project

Think of your bot and this project as two separate boxes.

```text
YOUR BOT
   |
   | sends a small event
   v
THIS PROJECT
   |
   | checks time and data
   | adds market context
   | can run simple models or AI
   v
RESULT FILE / SCORE / REPORT
```

At first, the result should be **read-only**. It should not place trades.

## 2. What should the bot send?

At minimum, one row should contain:

| field | simple meaning |
|---|---|
| `event_id` | a unique name for this event |
| `decision_ts` | the exact time when the bot made the decision |
| `symbol` | the market or instrument |
| your own values | information your bot already knew at that time |

Example:

```csv
event_id,decision_ts,symbol,system_score,state_a,state_b
x001,2026-01-01T10:07:00Z,SYNTH,0.62,1.4,-0.2
x002,2026-01-01T10:10:00Z,SYNTH,0.47,1.1,0.3
```

You do **not** need to explain how `system_score`, `state_a` or `state_b` were calculated. They can stay private.

Do not export passwords, API keys or account secrets.

## 3. If your bot is written in Python

Python bots can pass a table directly to the integration helper.

```python
from multimodal_market_ai.integration import attach_causal_market_context

joined = attach_causal_market_context(bot_events, closed_bars)
```

What happens?

1. The function checks that every event has a unique ID.
2. It checks the event time.
3. It finds the latest market bar that was already closed.
4. It adds that bar to the event.
5. It refuses to use a future bar.

Your private columns are kept unchanged.

## 4. If your bot is an MT4 or MT5 EA

The EA does not need Python inside it.

The easiest research bridge is usually a small file or database.

```text
MT4 / MT5 EA
    |
    | writes one row when something important happens
    v
CSV / JSON / SQLite
    |
    v
Python research process
    |
    v
model result / report
```

A generic EA row could look like:

```text
event_id,timestamp_utc,symbol,event_type,state_1,state_2
```

Then Python can:

1. read the row;
2. check that the time is valid;
3. add only market data that already existed;
4. run a deterministic model, numerical model or AI model;
5. write a result somewhere else.

Example result:

```json
{
  "event_id": "x001",
  "model_revision": "example-v1",
  "quality_score": 0.71,
  "risk_score": 0.29
}
```

These names are only examples.

## 5. Start with old data before live data

Do not start by connecting AI to live trading.

A safer order is:

```text
old bot events
 -> check IDs and times
 -> add causal market context
 -> check for future-information mistakes
 -> create outcomes later
 -> split data by time
 -> simple deterministic baseline
 -> simple numerical baseline
 -> optional AI
 -> read-only live test
```

This lets you find mistakes when nothing can affect real orders.

## 6. Keep the two worlds separate

### Your bot owns

- its private strategy;
- its indicators;
- its candidate rules;
- its execution logic;
- broker and account settings.

### This framework can own

- timestamp checks;
- market-data alignment;
- dataset IDs and hashes;
- train/validation/test separation;
- leakage checks;
- deterministic signal combination;
- model comparison;
- cache/resume tools;
- read-only live validation.

This separation is useful because you can improve the research layer without touching the code that already works inside your bot.

## 7. You can also rebuild part of the bot as a public deterministic model

Maybe your old bot has a very large signal section and you want to test a cleaner version.

You can export or recalculate a few simple signals:

```text
signal A
signal B
signal C
```

Then combine them with the public deterministic helper.

Example:

```python
from multimodal_market_ai.deterministic import combine_directional_signals

result = combine_directional_signals(
    data,
    ["signal_a", "signal_b", "signal_c"],
    policy="majority",
)
```

Now you have a small public model that can be changed one rule at a time.

Read: [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md).

## 8. What can AI do after the bot is connected?

AI does not need to replace the bot.

It can be tested as:

- a candidate ranker;
- a quality score;
- a market-context reader;
- an anomaly detector;
- a visual chart reader;
- a risk or uncertainty estimate;
- a continuation/deterioration estimate after an event already exists.

If the AI adds nothing useful, leave it out.

## 9. What is a read-only live test?

The model watches real incoming data and writes its answer, but cannot place an order.

Check:

- Does every event arrive once?
- Are timestamps correct?
- What happens after a restart?
- Does the data provider change old bars?
- Is the model too slow?
- Does live behavior look like the historical test?

Only after this stage should execution integration even be discussed.

## 10. Common mistakes to avoid

Do not:

- use future information in a feature;
- join rows only because they are in the same position;
- silently throw away unmatched events;
- calculate preprocessing again on validation/test data;
- reuse an old cache only because the file exists;
- keep looking at the final test set while changing the model;
- assume that AI must improve a mature bot.

More examples: [Failure modes and lessons learned](LESSONS_LEARNED.md).
