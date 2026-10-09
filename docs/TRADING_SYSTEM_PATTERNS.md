# Example market-system research patterns

Multimodal Market AI is strategy-agnostic. It does not ship a proprietary trading method or claim that one particular setup is profitable.

What it can provide is a common research stack for building, comparing and auditing different kinds of market systems. This page gives several **generic patterns** that contributors can implement with public data or their own rules.

The examples below are research templates, not trading recommendations.

## 1. Multi-timeframe trend + pullback system

A classic structure is:

```text
higher timeframe
    -> define trend / regime
middle timeframe
    -> confirm structure
lower timeframe
    -> time the entry
```

Example research logic:

- higher timeframe: a public trend or regime definition;
- middle timeframe: a structural or directional confirmation;
- lower timeframe: a public timing rule such as pullback/re-acceleration;
- stop: structural invalidation or a volatility-normalized distance;
- exit: fixed R target, trailing structure, or a staged exit policy.

This family is easy to implement and gives a good baseline for testing causal multi-timeframe alignment.

### Why it can adapt slowly

Many traditional multi-timeframe systems use several smoothed signals at once. Smoothing and confirmation windows can reduce noise, but they can also react slowly after a regime change.

That makes this family useful as a **slow-adapting baseline** when testing whether a learned visual/numerical state representation reacts earlier without becoming unstable.

## 2. Multi-signal confirmation system

A second generic pattern combines several independently computed observations, for example:

- current price/candle direction;
- one or more momentum measurements;
- a trend or slope estimate;
- volatility context;
- distance from a recent public structural reference.

A deterministic version can define an explicit confirmation policy. A learned version can instead estimate whether temporary disagreement between inputs carries useful information.

The exact indicators, thresholds and confirmation semantics are intentionally left to the user. The public framework focuses on causal synchronization, feature availability and fair comparison between deterministic and learned alternatives.

## 3. Breakout + retest system

```text
range / compression
      -> breakout
      -> retest
      -> continuation or failure
```

Research questions:

- Can a deterministic layer define the range and breakout exactly?
- Can a visual model distinguish clean retests from noisy false breaks?
- Does the same logic transfer across Forex, indices and commodities?
- Is a visual model useful only near events, allowing a cheap event gate to skip most bars?

This pattern is especially suitable for event-gated VLM research.

## 4. Mean-reversion system

Possible ingredients:

- distance from a rolling mean or VWAP-like reference;
- z-score / normalized deviation;
- volatility regime;
- higher-timeframe direction as a veto;
- re-entry into a statistical band.

A useful experiment is to compare:

1. pure numerical features;
2. numerical features + chart image;
3. a typed state that combines both.

Mean-reversion systems are a good reminder that the same visual shape can mean different things in different volatility regimes.

## 5. Relative-strength / cross-market system

Instead of looking at one chart in isolation, construct a relative-strength state from a basket of related instruments.

Examples:

- currency-strength models built from many FX crosses;
- sector-relative equity strength;
- commodity spread relationships;
- index-relative momentum;
- cross-asset risk-on / risk-off context.

The numerical layer should calculate exact cross-market quantities. A multimodal layer can then focus on context rather than trying to reproduce arithmetic from pixels.

## 6. Regime-switching system

A single strategy often behaves very differently in:

- trend;
- range;
- high volatility;
- low volatility;
- transition periods.

A regime system first estimates a state, then changes the downstream rule or model.

```text
market data
   -> regime/state model
       -> trend policy
       -> range policy
       -> transition / wait policy
```

Possible regime detectors include:

- deterministic volatility/trend statistics;
- HMMs or clustering;
- tree models;
- sequence models;
- visual/multimodal readers.

This is one of the clearest uses for a typed intermediate `MarketState`.

## 7. Event-gated multimodal system

Running a vision-language model on every bar is often wasteful.

A more practical architecture is:

```text
all bars
   -> cheap deterministic scanner
        -> nothing interesting: skip
        -> candidate / ambiguity: render chart
                                 -> multimodal model
                                 -> structured state
                                 -> decision layer
```

The scanner should optimize for **high recall**, not for being the final trading model. It is a radar, not the trader.

This pattern can make expensive multimodal inference practical over long histories.

## 8. Asymmetric payoff system

A system does not need a high win rate to have positive expectancy.

If average losses are `-1R` and average wins are larger, even a win rate below 50% can be economically useful.

Example:

```text
49 winners at +2R = +98R
51 losers  at -1R = -51R
------------------------
net                 +47R
profit factor       98 / 51 = 1.92
expectancy          +0.47R per trade
```

Therefore:

- do not optimize only for classification accuracy;
- do not treat every losing trade as a model error;
- report the whole R-multiple distribution;
- inspect the positive tail (`+2R`, `+3R`, `+4R`, ...);
- report expectancy, profit factor and drawdown alongside win rate.

This is a core design principle of the evaluation module.

## 9. Learned state + lightweight decision head

A powerful general pattern is to separate perception from decision-making:

```text
raw data / charts
       -> numerical + visual encoders
       -> typed MarketState
       -> small decision model
```

The decision head can be deliberately simple:

- logistic regression;
- gradient boosting;
- a small MLP;
- a small sequence model;
- a compact language model consuming typed state.

Benefits:

- cheaper retraining;
- easier comparison between visual backends;
- better auditability;
- easier caching;
- easier deployment on ordinary hardware.

## 10. How to compare systems fairly

For any strategy family, keep the comparison protocol fixed:

1. define timestamp semantics;
2. freeze train/validation/test periods;
3. forbid future/post information in inputs;
4. use the same transaction-cost assumptions;
5. report both predictive and economic metrics;
6. preserve outputs so a new economic policy can be evaluated without retraining the model;
7. compare against simple deterministic and statistical baselines.

A complex AI model is useful only if it adds something measurable beyond a simpler alternative.

## Suggested first community experiments

Good starter contributions would be:

- implement one deterministic baseline from this page;
- add a public-data example for Forex, equities or crypto;
- connect an existing EA/Python bot through the public integration adapter;
- compare CPU-only vs GPU models on the same state representation;
- test whether visual context improves a numerical baseline;
- benchmark event gating and cache hit rates;
- submit a different exit/R policy while reusing frozen model outputs.

The project welcomes systems that are very different from one another. The goal is to make the **research infrastructure reusable**, not to force every contributor into one trading philosophy.
