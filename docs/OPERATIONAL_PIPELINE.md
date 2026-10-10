# Operational pipeline — four simple steps

Multimodal Market AI uses one simple operational pipeline.

The exact strategy can change. The model can change. The data source can change.

The four jobs stay the same:

```text
1. ACQUIRE
   get the market case that really exists now
        |
        v
2. EXTRACT
   turn that case into causal, usable information
        |
        v
3. DECIDE
   compare the information and choose what to do now
        |
        v
4. APPLY
   pass that decision to a safe output or execution layer
```

This is the operational pipeline. Training, model comparison, caching, audits and visual AI are tools used to build or validate these four steps. They are not separate competing pipelines.

## 1. Acquire

**Question:** what information is actually available now?

Examples:

- closed market bars;
- an event exported by an existing bot;
- several synchronized timeframes;
- data from another market used as context.

The important rule is simple:

> Do not use information that did not exist yet.

If the decision time is 10:07, a bar that closes at 10:10 does not exist yet for that decision.

## 2. Extract

**Question:** what useful facts can we calculate from the available data?

This is where a deterministic system can work.

Examples of generic extracted information:

- trend clues;
- momentum clues;
- structural clues;
- volatility;
- relative-strength values;
- multi-timeframe context;
- outputs from an existing private bot.

The extractor can be completely replaced.

One user may use three simple public signals. Another user may connect a private EA with thousands of lines of code. Both can still use the same four-step pipeline.

The same input plus the same deterministic version should produce the same extracted result.

## 3. Decide

**Question:** given the information we have now, what should the system do now?

A trading example can use three decisions:

```text
LONG
SHORT
WAIT
```

Other projects can rename them, for example:

```text
ACTION_A
ACTION_B
WAIT
```

`WAIT` means **do not perform either action yet**. It can mean that more information is needed, that the rules disagree, or that the current case is not actionable under the user's system.

The public framework does not prescribe one private definition of `WAIT`.

### Three different ideas that must not be confused

They look similar, but they are not the same thing:

1. **A signal does not vote** — in the public multi-signal helper, one rule can output `0`.
2. **The final decision is WAIT** — the decision layer chooses not to act now.
3. **An internal state** — a private system may keep some longer-lived state of its own.

Do not automatically treat these three things as one variable.

The public deterministic combiner may produce `det_signal = 0` when it cannot choose a side. A caller may map that result to `WAIT`, but `0` is not automatically a third persistent market direction.

## 4. Apply

**Question:** where does the decision go?

At first, the safest answer is usually a read-only output:

```text
decision
 -> CSV / JSON / database / log / screen
```

For an existing EA:

```text
private bot or deterministic core
        |
        v
small bridge
        |
        v
read-only decision/output
```

The bridge should transport the result. It should not secretly rebuild a second copy of the strategy.

If an optional field is not available, keep it unavailable. Do not invent a value only to make the record look complete.

Execution-capable code is a separate safety decision. This public project treats read-only forward validation as the normal step before any execution integration.

# Where AI fits

AI is not automatically step 5.

It can help inside step 2 or step 3 if it proves useful.

Examples:

```text
ACQUIRE
 -> deterministic EXTRACT
 -> simple DECIDE
```

or:

```text
ACQUIRE
 -> deterministic + visual EXTRACT
 -> statistical/AI DECIDE
```

or:

```text
existing private bot
 -> exported state
 -> AI quality/risk estimate
 -> DECIDE or read-only report
```

The model family is replaceable. The operational pipeline is not redesigned every time a new model is tested.

# Build the pipeline before choosing the fanciest model

A sensible order is:

```text
complete the four operational steps
        |
        v
prove the deterministic/core data path is causal and reproducible
        |
        v
freeze the experiment contract
        |
        v
compare candidate models fairly
```

Candidate models should be compared using the same:

- dataset;
- time split;
- available inputs;
- target meaning;
- metrics;
- deterministic/core pipeline.

If a more complex model does not improve the result, it does not need to be used.

# Research workflow around the four steps

The repository contains many research tools. They support the pipeline like safety equipment around a machine:

```text
                    hashes / manifests
                           |
                           v
ACQUIRE -> EXTRACT -> DECIDE -> APPLY
   |          |          |        |
 causal    replay /    train-   read-only
 checks     freeze     val-test   forward
   |          |          |        |
   +----------+----------+--------+
              evaluation
```

These tools are important, but they should not make the basic pipeline harder to understand.

# Minimal rule

When considering a new component, ask:

> Which of the four jobs does this component improve or validate?

If the answer is "none", it probably does not belong in the operational pipeline yet.

See also:

- [Multi-signal and deterministic model](MULTI_SIGNAL_AND_DETERMINISTIC_MODEL.md)
- [Deterministic freeze protocol](DETERMINISTIC_FREEZE_PROTOCOL.md)
- [Integrating an existing bot or EA](INTEGRATING_EXISTING_BOTS.md)
- [Public research workflow](PUBLIC_WORKFLOW_SYNC.md)
