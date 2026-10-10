# Multi-signal and deterministic model — explained simply

This page explains two ideas:

1. **multi-signal** — use more than one simple clue;
2. **deterministic model** — write exact rules that always give the same answer from the same data.

You do not need to be a programmer or trader to understand the idea.

## 1. What is a signal?

A signal is the answer to one small question.

Examples:

- Is the recent trend pointing up?
- Is price moving faster than before?
- Is price above a reference level?
- Is volatility too high?

One signal should answer one simple question.

A signal is not automatically a trade.

Think of three people looking at the weather:

- one sees dark clouds;
- one feels strong wind;
- one hears thunder.

Each person gives one clue. A later rule combines the clues.

That is the basic idea of a multi-signal system.

## 2. Public signal convention

The helper in this repository uses:

```text
+1 = this rule points one way
-1 = this rule points the other way
 0 = this rule is not voting right now
```

The `0` belongs to the **individual signal**.

It does not automatically mean:

- a neutral market regime;
- missing data;
- a persistent internal state;
- the final system decision.

Keep those meanings separate.

## 3. The final decision is a different layer

After signals are combined, a trading system may choose:

```text
LONG
SHORT
WAIT
```

`WAIT` means: do not perform LONG or SHORT yet.

A caller may map a deterministic `det_signal = 0` to `WAIT`, but the two ideas should still be documented separately:

```text
signal-level 0 -> this rule or combiner has no directional choice
final WAIT     -> the decision layer chooses no action now
```

A private system may also keep an internal state that lasts longer than one decision. That is another separate concept.

## 4. What is a deterministic model?

A deterministic model is a machine made of exact rules.

If you give it the same data twice, it should give the same answer twice.

There is no randomness and no hidden AI intuition.

Example:

```text
IF rule A says +1
AND rule B says +1
AND rule C says +1
THEN result = +1
```

Or:

```text
IF at least 2 rules out of 3 say +1
THEN result = +1
```

The rules can be checked and replaced.

## 5. Three simple ways to combine signals

### Majority

The side with more active votes wins.

```text
+1, +1, -1 -> +1
-1, -1, +1 -> -1
+1, -1,  0 ->  0
```

### Unanimous

All active signals must agree.

```text
+1, +1, +1 -> +1
-1, -1, -1 -> -1
+1, +1, -1 -> 0
```

### Weighted

Some rules can count more than others.

```text
signal A weight = 0.6
signal B weight = 0.3
signal C weight = 0.1
```

Weights should be chosen and tested without looking into future evaluation data.

## 6. A theoretical replaceable system

Imagine three generic rules.

### Rule A — trend

Ask:

> Is a faster measure above or below a slower measure?

### Rule B — momentum

Ask:

> Is price currently moving in the same direction as the trend clue?

### Rule C — structure

Ask:

> Is price on one side or the other of a recent reference area?

Then combine the three rules.

This is only a teaching example.

Another user could replace them with:

- volume;
- volatility;
- a private indicator from an EA;
- relative strength;
- an AI output;
- signals from another timeframe;
- signals from another market.

The rest of the repository does not need to change.

## 7. Replace the signals, not the whole project

Suppose version 1 is:

```text
A = trend
B = momentum
C = structure
```

Later you decide B is weak.

Version 2 can be:

```text
A = trend
B = new_rule
C = structure
```

Recalculate the deterministic output and compare the two versions fairly.

Do not rebuild the whole project just because one rule changed.

## 8. Where this fits in the operational pipeline

The project uses four jobs:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

A multi-signal deterministic system normally belongs mostly in **EXTRACT**, and it may also provide a simple baseline for **DECIDE**.

Example:

```text
market data
 -> calculate signals
 -> combine them deterministically
 -> decision layer maps the result to LONG / SHORT / WAIT
 -> read-only output
```

Read: [Operational pipeline](OPERATIONAL_PIPELINE.md).

## 9. Build the deterministic core before AI

AI should have a simple baseline to beat.

A sensible order is:

```text
1. deterministic rules
2. prove the deterministic output is causal and reproducible
3. freeze that version
4. simple statistical model
5. optional multimodal model
6. compare them on the same data
```

If a large AI model does not improve on the simpler system, more complexity may not help.

## 10. A deterministic model is not frozen just because it runs

Before you call the deterministic core stable, test that:

- adding later data does not change old historical records;
- isolated runs reproduce sequential runs;
- input hashes match before outputs are compared;
- required record IDs are stable;
- schema differences are separated from value differences;
- unavailable information is not invented.

Read: [Deterministic freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md).

## 11. Public Python helper

The repository provides:

```python
from multimodal_market_ai.deterministic import combine_directional_signals
```

Example:

```python
import pandas as pd

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

The result contains:

- `det_score` — how strongly active signals lean one way;
- `det_active_signals` — how many rules voted;
- `det_signal` — the deterministic directional result.

The helper does not tell you which indicators to use. Your signals are your system.

## 12. AI can be added without replacing the deterministic core

### AI as another clue

```text
signal A
signal B
signal C
AI signal
   -> deterministic combiner
```

### AI as a second-stage decision model

```text
deterministic extracted state
 + other causal features
 -> model
 -> LONG / SHORT / WAIT
```

### AI as post-decision analysis

```text
an event already exists
 -> AI estimates continuation, deterioration or uncertainty
```

These are different experiments. Do not merge them into one unexplained target.

## 13. Compare versions fairly

When you replace a signal or model, keep constant:

- historical period;
- market rows;
- train/validation/test split;
- target meaning;
- costs if economic evaluation is used;
- evaluation method;
- frozen deterministic/core pipeline where required.

Otherwise you may think the new version is better only because it was tested on an easier problem.

## Main rule

Build small pieces. Give every field one clear meaning. Keep timestamps causal. Freeze the deterministic core before final model comparison. Change one piece at a time and measure what actually improved.
