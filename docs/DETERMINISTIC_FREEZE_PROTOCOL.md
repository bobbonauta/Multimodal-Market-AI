# Deterministic freeze protocol

A deterministic system is not ready just because it runs once.

Before treating a deterministic core as stable, prove that it gives the same historical facts when the same facts are replayed.

This page describes a public, strategy-agnostic freeze protocol.

## 1. Freeze the contract first

Record the things that define the deterministic run:

- input dataset or source manifest;
- code revision;
- configuration revision;
- record-ID rule;
- timestamp semantics;
- required columns/schema;
- any provider/session rules that affect aggregation.

If one of these changes, you are testing a new version.

## 2. Test prefix invariance

This is one of the strongest causal checks.

Imagine running the system with data up to Friday:

```text
Monday -> Tuesday -> Wednesday -> Thursday -> Friday
```

Save the records produced for that history.

Then run the same system again with more future data:

```text
Monday -> ... -> Friday -> Saturday -> Sunday -> Monday
```

The records that already existed in the first run must not change just because later data was added.

In simple words:

> Adding the future must not rewrite the past.

Check at least:

- old record IDs are still present;
- no new record is inserted into the old historical prefix unexpectedly;
- canonical values for old IDs are unchanged;
- timestamps are unchanged;
- the required schema remains compatible.

A failure here is a causality/reproducibility problem until explained.

## 3. Test isolated execution

Hidden program state can create false reproducibility.

Example:

```text
configuration A
configuration B
configuration C
```

Run them once in the same long process.

Then run each one again in a fresh process with no shared memory or cache.

The results should match.

If they do not, look for:

- global variables;
- mutable caches;
- random state;
- environment-dependent defaults;
- files left by earlier runs.

## 4. Compare the inputs before comparing the outputs

Two outputs should not be called inconsistent if the inputs were different.

Before comparing two runs, verify the source fingerprint/hash.

```text
same input hash -> output comparison is meaningful

different input hash -> INPUT_NOT_COMPARABLE
```

The second case is not automatically a model failure.

Even two datasets with the same number of rows and the same start/end times can contain different values.

## 5. Separate value differences from representation differences

A strict table comparison can fail even when the actual values are the same.

Examples:

- integer vs floating dtype;
- timestamp resolution differences;
- timezone-aware vs differently encoded timestamp metadata.

An audit should report separately:

```text
VALUE DIFFERENCE
SCHEMA DIFFERENCE
DTYPE / REPRESENTATION DIFFERENCE
```

Do not ignore representation differences, but do not automatically call them changed trading logic either.

## 6. Keep the schema stable

If a field belongs to the contract but is temporarily unavailable, a stable schema will often keep the field and mark its value as missing/unavailable.

That is usually easier to audit than making columns appear and disappear depending on the current row.

Unknown fields outside the agreed schema should fail closed or be explicitly versioned.

## 7. Missing optional information must stay missing

A deterministic or bridge layer must not invent information to make a record complete.

If a value is not yet available:

```text
available value   -> transport it with its availability time
unavailable value -> keep it unavailable
future value      -> reject it
```

This is different from guessing a default value.

## 8. Freeze the core after the checks pass

When the deterministic core passes its agreed replay, causality and reproducibility checks, mark that version as frozen for the next experiment.

From that point:

- model comparison should use the same frozen deterministic core;
- a bridge should transport its output instead of rebuilding the rules independently;
- changes are allowed only as a new explicit version;
- a real correctness bug can reopen the core, but that invalidates or revalidates dependent results as needed.

## 9. Then compare models fairly

Only after the input/data path and deterministic core are stable should candidate models be compared.

Use the same:

- rows;
- split;
- target;
- allowed inputs;
- deterministic core;
- evaluation metrics.

This keeps a model from winning simply because it received easier data or a different pipeline.

## 10. Read-only bridge before execution

The next engineering step is normally a read-only bridge:

```text
frozen core
 -> small transport record
 -> external consumer / EA / service
 -> log or display only
```

The bridge should verify identity, timestamps and availability, but should not create a second independent implementation of the deterministic strategy.

## Freeze checklist

Before calling a deterministic version frozen, ask:

- Is the input fingerprint recorded?
- Are record IDs stable and unique?
- Does future-appended data leave the old prefix unchanged?
- Does isolated execution match sequential execution?
- Are value changes separated from dtype/schema changes?
- Are required fields/schema explicit?
- Are unavailable values kept unavailable rather than invented?
- Is the code/config version recorded?
- Is the next model comparison using the same frozen core?

If the answer is yes, the deterministic system is much more than "code that happens to run": it is a reproducible baseline that can be trusted enough for controlled research.
