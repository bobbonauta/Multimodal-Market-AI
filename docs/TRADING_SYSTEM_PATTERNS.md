# Example trading-system patterns — simple explanations

This project does not give you one secret strategy.

Instead, it gives you tools that can be used with many different systems.

The examples below are **ideas for research**, not trading advice.

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

The exact indicators are replaceable.

Why use this pattern?

Because it teaches how to combine several time scales without accidentally using a bar that was not closed yet.

## 2. Multi-signal confirmation

A multi-signal system uses several small clues.

Example:

```text
signal A = trend clue
signal B = momentum clue
signal C = structure clue
```

Each signal can say:

```text
+1 = points one way
-1 = points the other way
 0 = no opinion from this rule
```

Then a deterministic model can combine them.

### Majority example

```text
A = +1
B = +1
C = -1

final answer = +1
```

### Unanimous example

```text
A = +1
B = +1
C = -1

final answer = 0 because they do not all agree
```

### Weighted example

Maybe signal A has proved more reliable in your research.

You can give it more weight:

```text
A weight = 0.6
B weight = 0.3
C weight = 0.1
```

The important idea is not the exact rule. The important idea is that **every signal can be replaced and recalculated without rebuilding the whole project**.

Read the full simple guide: [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md).

## 3. Breakout + retest

Idea:

```text
price stays in an area
 -> leaves the area
 -> comes back to test it
 -> continues or fails
```

Possible research questions:

- Can simple rules find the range?
- Can a visual model tell a clean retest from a messy one?
- Does visual AI add anything beyond numerical rules?

## 4. Mean reversion

Idea:

> Price moves far away from a normal reference, then may move back toward it.

Possible clues:

- distance from a recent average;
- volatility;
- whether the larger market direction supports or fights the return.

You can compare:

```text
numbers only
vs
numbers + chart image
```

## 5. Relative strength

Instead of looking at one market alone, compare several related markets.

Examples:

- one currency against several others;
- one stock sector against another;
- one index against another;
- related commodities.

The numerical layer should do the arithmetic. AI can then focus on context instead of trying to read exact maths from pixels.

## 6. Regime switching

Markets do not always behave the same way.

A simple system may first ask:

```text
Is the market trending?
Is it moving sideways?
Is volatility high?
Is volatility low?
```

Then it can choose a different rule for each situation.

```text
market data
 -> regime estimate
      -> trend rules
      -> range rules
      -> wait / uncertain rules
```

## 7. Event-gated visual AI

Running a large visual model on every bar can be wasteful.

A cheaper design is:

```text
all bars
 -> cheap deterministic scanner
      -> boring case: skip
      -> interesting case: ask visual AI
```

Think of the cheap scanner as a radar. It finds moments worth examining more closely.

## 8. Deterministic model first, AI second

This is one of the most important patterns in the repository.

Start with rules you can read:

```text
market data
 -> signal A
 -> signal B
 -> signal C
 -> deterministic final answer
```

Then test whether AI can add something:

```text
deterministic answer
 + extra market context
 + optional image
 -> AI / statistical model
```

If the AI does not improve the result fairly, keep the simpler model.

## 9. AI as another signal

AI does not have to own the whole decision.

It can simply produce one more clue:

```text
trend signal
momentum signal
structure signal
AI signal
      |
      v
deterministic combiner
```

This keeps the final system easier to inspect.

## 10. Post-decision / management model

AI can also be studied **after** an event already exists.

Example research question:

> Given everything known now, does the situation look like it is improving, deteriorating or becoming uncertain?

This is different from asking the AI to create the original entry.

## 11. How to compare two systems fairly

If you change one rule, keep the test fair.

Use:

- the same historical period;
- the same rows;
- the same train/validation/test split;
- the same costs;
- the same evaluation method.

Otherwise you may compare two different problems without noticing.

## 12. Good first experiments

Simple community projects include:

- create three public signals and combine them with majority voting;
- replace one signal and measure what changes;
- connect an existing EA through the integration adapter;
- compare a deterministic model with a simple numerical model;
- add a chart image only after the numerical baseline exists;
- run the same model in read-only live mode.

The goal is not to force everyone to use the same trading idea. The goal is to make **building, replacing and testing each piece easy and auditable**.
