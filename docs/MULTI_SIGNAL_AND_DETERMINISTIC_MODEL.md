# Multi-signal and deterministic model — explained simply

This page explains two ideas used by this project:

1. **multi-signal**: use more than one simple clue;
2. **deterministic model**: write exact rules that always give the same answer from the same data.

You do not need to be a programmer or a trader to understand the idea.

## 1. What is a signal?

A **signal** is just the answer to one small question.

For example:

- Is the recent trend pointing up?
- Is price moving faster than before?
- Is price above a reference level?
- Is volatility too high?

One signal should answer **one simple question**.

A signal is not automatically a trade.

Think of three friends looking at the same sky:

- friend A says: “the clouds are dark”;
- friend B says: “the wind is getting stronger”;
- friend C says: “I can hear thunder”.

Each friend gives one clue. The final decision — “take an umbrella” — can use all three clues together.

That is the basic idea of a **multi-signal system**.

## 2. What does multi-signal mean?

**Multi-signal** means that the system does not depend on only one clue.

Instead, several independent rules produce small opinions. Then another rule combines them.

A very simple public convention is:

- `+1` = this rule points upward / positive;
- `-1` = this rule points downward / negative;
- `0` = this rule has no opinion right now.

In this public helper, `0` means only **“this rule is not voting”**. It is not a special market state.

Example:

| rule | answer |
|---|---:|
| trend rule | +1 |
| momentum rule | +1 |
| structure rule | -1 |

A majority system would produce `+1`, because two rules point up and one points down.

## 3. What is a deterministic model?

A **deterministic model** is a machine made of exact rules.

If you give it the same data twice, it gives the same answer twice.

There is no randomness and no “AI intuition”.

Example:

```text
IF rule A says +1
AND rule B says +1
AND rule C says +1
THEN final signal = +1
```

Or:

```text
IF at least 2 rules out of 3 say +1
THEN final signal = +1
```

The important part is that the rules are written down and can be checked.

This makes a deterministic model useful as the **first version of a system** and as a **baseline** to compare against AI.

## 4. Three simple ways to combine signals

The public helper supports three common ideas.

### A. Majority

The side with more votes wins.

```text
+1, +1, -1  -> +1
-1, -1, +1  -> -1
+1, -1,  0  ->  0   (tie)
```

This is easy to understand and is often a good first experiment.

### B. Unanimous

All active signals must agree.

```text
+1, +1, +1 -> +1
-1, -1, -1 -> -1
+1, +1, -1 -> 0
```

This is stricter. It usually produces fewer decisions.

### C. Weighted

Some rules can be more important than others.

Example:

```text
trend     weight 0.6
momentum  weight 0.3
structure weight 0.1
```

If the trend rule says `+1`, it counts more than the structure rule.

Weights should be chosen carefully and tested on past data without looking into the future.

## 5. A theoretical system anyone can replace

Imagine a completely generic system with three rules.

### Rule A — trend

Ask:

> Is a faster measure of price above a slower measure?

Possible output:

```text
above  -> +1
below  -> -1
```

### Rule B — momentum

Ask:

> Is price moving in the same direction as the trend right now?

Possible output:

```text
moving up   -> +1
moving down -> -1
unclear     -> 0
```

### Rule C — structure

Ask:

> Is price on the positive or negative side of a recent reference area?

Possible output:

```text
positive side -> +1
negative side -> -1
inside/noisy  -> 0
```

Now combine them with majority voting.

This is only a teaching example. You can replace every rule.

For example, another person could use:

- volume instead of momentum;
- volatility instead of structure;
- a custom indicator from an existing EA;
- a neural network output as one of the signals;
- signals from different timeframes;
- signals from different markets.

The rest of the repository does not need to change.

## 6. The important idea: replace the signals, not the whole project

Suppose your first version uses:

```text
signal_A = trend
signal_B = momentum
signal_C = structure
```

Later you discover that `signal_B` is weak.

You can replace only that part:

```text
signal_A = trend
signal_B = new_rule
signal_C = structure
```

Then recalculate the deterministic model and compare the new results with the old ones.

You do **not** need to rebuild the whole project.

This is one of the main goals of Multimodal Market AI: keep each part separate enough that it can be changed and tested without destroying everything else.

## 7. You can build your own system directly inside this repository

You do not need an existing bot.

A complete path can start here:

```text
market data
   -> create simple signals
   -> combine signals with deterministic rules
   -> obtain candidates / decisions
   -> attach causal multi-timeframe context
   -> record what happened later
   -> split past data into train / validation / test
   -> compare simple models
   -> optionally add visual / multimodal AI
   -> read-only live test
```

This means the repository can be used in two ways:

### Path 1 — you already have a bot

```text
your bot
 -> integration adapter
 -> causal data + AI experiments
```

### Path 2 — you have no bot yet

```text
public deterministic model
 -> your own signals
 -> your own deterministic strategy
 -> causal data + AI experiments
```

Both paths can later use the same auditing, caching, model-comparison and multimodal tools.

## 8. Why build the deterministic model before AI?

Because AI should have something simple to beat.

If a simple three-rule system works as well as a large model, the large model may not be worth the cost.

A sensible order is:

```text
1. simple deterministic rules
2. simple statistical / tabular model
3. optional multimodal model
4. compare them on the same rows
```

This helps avoid wasting GPU time and makes errors easier to find.

## 9. How the public Python helper works

The repository provides:

```python
from multimodal_market_ai.deterministic import combine_directional_signals
```

Your data can contain three signal columns:

```python
import pandas as pd

frame = pd.DataFrame(
    {
        "trend": [1, 1, -1],
        "momentum": [1, -1, -1],
        "structure": [0, 1, -1],
    }
)
```

Then combine them:

```python
from multimodal_market_ai.deterministic import combine_directional_signals

result = combine_directional_signals(
    frame,
    ["trend", "momentum", "structure"],
    policy="majority",
)

print(result)
```

The result adds:

- `det_score`: how strongly the active signals lean one way;
- `det_active_signals`: how many rules voted;
- `det_signal`: the final deterministic answer.

The helper does **not** tell you which indicators to use. That is intentional. Your signals are your system.

## 10. From deterministic model to AI-assisted model

Once you have a deterministic model, AI can be added in several ways.

### AI as a filter

```text
deterministic candidate
 -> AI says high quality / low quality
```

### AI as another signal

```text
trend signal
momentum signal
structure signal
AI signal
      -> deterministic combiner
```

### AI as a second-stage model

```text
deterministic system
 -> candidate dataset
 -> AI learns which situations behave differently
```

### AI for post-decision analysis

```text
trade/event already exists
 -> AI estimates continuation, deterioration or uncertainty
```

The deterministic system remains visible and auditable in every case.

## 11. What must not change when you compare versions

If you replace a signal, compare old and new systems fairly.

Keep these things the same:

- the same historical period;
- the same market rows;
- the same train/validation/test split;
- the same transaction-cost assumptions;
- the same evaluation method.

Otherwise you may think the new rule is better only because it was tested on easier data.

## 12. The main rule

The model should be easy to change but hard to fool.

Build small pieces. Test each piece. Keep timestamps causal. Keep the final holdout protected. Compare simple systems before expensive ones.

Then replace one piece at a time and measure whether it actually improved the result.
