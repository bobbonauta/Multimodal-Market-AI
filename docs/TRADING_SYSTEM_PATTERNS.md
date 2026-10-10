# Example trading-system patterns — simple explanations

This project does not give you one secret strategy.

Instead, it gives you tools that can be used with many different systems.

The examples below are **ideas for research**, not trading advice.

All examples should still fit the same operational pipeline:

```text
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
```

## 1. Multi-timeframe trend + pullback

Idea:

```text
slower view  -> what is the big direction?
middle view  -> is the structure still compatible?
faster view  -> is this a good moment to act?
```

A public example could use:

- a slow trend measure;
- a middle structural rule;
- a faster timing rule.

The exact indicators and timeframe choices are replaceable.

The useful lesson is how to synchronize several time scales without using a bar that was not closed yet.

## 2. Multi-signal confirmation

A multi-signal system uses several small clues.

Example:

```text
signal A = trend clue
signal B = momentum clue
signal C = structure clue
```

Each input signal can say:

```text
+1 = points one way
-1 = points the other way
 0 = no vote from this rule
```

Then a deterministic model combines them.

### Majority example

```text
A = +1
B = +1
C = -1

combined direction = +1
```

### Unanimous example

```text
A = +1
B = +1
C = -1

combined direction = 0
```

Here `0` means the combiner did not choose a direction. A later trading decision layer may map that to `WAIT`; it is not automatically a persistent neutral market state.

### Weighted example

Maybe signal A has proved more useful in your research.

```text
A weight = 0.6
B weight = 0.3
C weight = 0.1
```

Every signal can be replaced and recalculated without rebuilding the whole project.

Read: [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md).

## 3. Breakout + retest

Idea:

```text
price stays in an area
 -> leaves the area
 -> comes back to test it
 -> continues or fails
```

Possible research questions:

- Can deterministic rules define the event?
- Can a visual model distinguish cleaner and noisier cases?
- Does visual AI add anything beyond numerical rules?

## 4. Mean reversion

Idea:

> Price moves far away from a reference and may later move back toward it.

Possible clues:

- distance from a recent average;
- volatility;
- larger-context direction.

Compare models only on the same rows and same time split.

## 5. Relative strength

Instead of looking at one market alone, compare several related markets.

Examples:

- one currency against several others;
- one stock sector against another;
- one index against another;
- related commodities.

The numerical layer should do exact arithmetic. AI can focus on context if it adds useful information.

## 6. Regime-aware systems

A generic system may ask whether current conditions belong to different broad regimes.

For example:

```text
trend-like
range-like
high volatility
low volatility
uncertain
```

These are only example research labels. Do not invent a regime variable merely to force every observation into a class.

The final decision can still be simpler:

```text
LONG | SHORT | WAIT
```

## 7. Event-gated visual AI

Running a large visual model on every bar can be wasteful.

A cheaper research design is:

```text
all observations
 -> cheap deterministic scanner
      -> skip ordinary cases
      -> send selected cases to visual AI
```

The scanner is a research selector. It does not create a new operational pipeline.

## 8. Deterministic model first, AI second

Start with rules you can read and reproduce:

```text
market data
 -> signal A
 -> signal B
 -> signal C
 -> deterministic output
```

Then freeze and audit that deterministic path before comparing AI:

```text
frozen deterministic output
 + extra causal context
 + optional image
 -> candidate statistical/AI model
```

If AI does not improve the result fairly, keep the simpler system.

## 9. AI as another signal

AI does not have to own the whole decision.

It can produce one more clue:

```text
signal A
signal B
signal C
AI signal
      |
      v
deterministic combiner
```

The AI signal should still obey the same causality and evaluation rules.

## 10. Post-decision / management model

AI can also be studied **after** an event already exists.

Example research question:

> Given everything known now, does the situation look like it is improving, deteriorating or becoming uncertain?

This is a different target from the original entry/decision problem. Keep the two experiments separate.

## 11. How to compare two systems fairly

If you change one rule or model, keep the comparison fair.

Use:

- the same historical period;
- the same rows;
- the same train/validation/test split;
- the same target meaning;
- the same costs if economic evaluation is used;
- the same evaluation method;
- the same frozen deterministic/core pipeline where required.

Otherwise you may compare two different problems without noticing.

## 12. Good first experiments

- create three public signals and combine them with majority voting;
- map unresolved output to a separate `WAIT` decision;
- replace one signal and measure what changes;
- connect an existing EA through the integration adapter;
- test prefix invariance before freezing the deterministic core;
- compare a deterministic model with a simple numerical model;
- add a chart image only after the numerical baseline exists;
- run the frozen result in read-only live mode.

The goal is not to force everyone to use the same trading idea. The goal is to make **building, replacing, freezing and testing each piece easy and auditable**.
