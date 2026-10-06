# Historical market data: sources, download workflow and causal preparation

This project intentionally does **not** bundle large historical datasets. Market data licensing, broker terms and redistribution rights vary by provider, so users should obtain data from a source they are legally allowed to use.

The important part for Multimodal Market AI is not the provider name. It is the **timestamp semantics, completeness, provenance and causal transformation pipeline**.

## What the research used

Prior research behind this project used more than one source, including:

- **Dukascopy historical market data tooling** for long OHLC histories;
- **broker / MetaTrader 5 exports and caches** for comparison and broker-specific histories;
- locally preserved raw files before any resampling or feature construction.

Using multiple sources was useful because market-history details can differ between providers: session boundaries, weekend bars, flat candles, missing intervals, spread representation and timezone conventions may all change a backtest.

## Recommended data workflow

```text
source download / broker export
        -> immutable RAW copy
        -> normalize symbol + timezone + timestamp meaning
        -> validate duplicates, gaps and abnormal bars
        -> choose the base timeframe
        -> build higher timeframes causally
        -> freeze train / validation / test periods
        -> deterministic features / rendering / model input
```

Do not overwrite the raw source when cleaning data. Keep the source copy immutable so every derived dataset can be traced back to it.

## Canonical OHLCV schema

A simple interoperable format is CSV or Parquet with at least:

```text
timestamp,open,high,low,close,volume
2026-01-02T10:05:00Z,1.0350,1.0354,1.0348,1.0352,1234
```

Requirements:

- timestamp must be timezone-aware;
- UTC is strongly recommended internally;
- document whether the timestamp means **bar open** or **bar close**;
- the current public API assumes **close-indexed bars**;
- OHLC must describe only information available inside that completed bar;
- keep volume semantics documented: real volume, tick volume or unavailable.

If your provider uses bar-open timestamps, convert them consistently before causal alignment.

## Suggested folder layout

```text
data/
  raw/
    provider_name/
      EURUSD/
        M5.parquet
  normalized/
    EURUSD/
      M5.parquet
  derived/
    EURUSD/
      M15.parquet
      H1.parquet
      H4.parquet
```

`raw/` should be treated as immutable.

## Starting from one base timeframe

You usually do **not** need to download every higher timeframe separately.

If a trustworthy base timeframe is available, higher timeframes can be built from it:

```text
M5 -> M15 -> H1 -> H4
```

or directly from M5 according to the target boundaries.

The critical rule is that the higher-timeframe bar must become visible only after it has closed.

For example, a completed H1 bar ending at 11:00 UTC may be used by an M5 decision at 11:00 or later, but not by a decision at 10:55.

The package functions `resample_ohlcv_close_indexed` and `align_closed_higher_timeframe` are designed around this principle.

## Data validation before training

Before using a history for training or backtesting, check at least:

- monotonic timestamps;
- duplicate timestamps;
- timezone consistency;
- missing expected intervals;
- `high >= max(open, close)`;
- `low <= min(open, close)`;
- `high >= low`;
- impossible or zero prices;
- long runs of flat candles;
- unexpected weekend/session bars;
- sudden symbol precision changes;
- unusually large gaps that may represent bad data rather than market movement.

Do not silently delete anomalies. Record what was removed or transformed and why.

## Forex-specific considerations

Forex is decentralized. There is no single universal candle history shared by every broker.

Possible differences include:

- server timezone;
- daily candle boundary;
- Sunday / weekend candles;
- bid-only vs ask/mid data;
- spread and rollover handling;
- holidays and partial sessions;
- broker-specific missing or synthetic bars.

For research intended to transfer between brokers, treat provider identity as part of the dataset provenance.

## Dukascopy-style histories

Dukascopy is useful for long historical coverage and is commonly used in quantitative research. The prior research used Dukascopy-based tooling as one source of historical FX data.

Because third-party downloader packages can change, this repository avoids freezing one unofficial download command until the public connector is implemented and tested. Contributors are encouraged to add a connector that:

1. records the source and downloader version;
2. downloads a clearly specified symbol/time range;
3. converts timestamps to the canonical schema;
4. preserves a raw copy;
5. emits a manifest with row count, first/last timestamp and data hash;
6. documents the provider's applicable terms.

See GitHub issue **#1** for the first public connector task.

## MetaTrader / broker data

Broker or MetaTrader histories are useful when the final system will operate on that broker's feed.

Recommended procedure:

1. export OHLC data from the platform or documented local cache;
2. preserve the original export unchanged;
3. record broker/server and timezone;
4. normalize to UTC close timestamps;
5. compare a small overlapping period against an independent source;
6. document material differences rather than forcing both feeds to look identical.

## Train / validation / test

Financial time series should normally be split **chronologically**, not randomly.

Example:

```text
TRAIN       2015-2020
VALIDATION  2021-2022
TEST        2023-2024
```

The exact dates depend on the experiment. The principle is what matters:

- fit on the past;
- tune on later but still development-only data;
- keep final test data unopened until the model and evaluation policy are frozen.

For multi-timeframe systems, all derived timeframes must obey the same temporal boundary.

## Rendering and model input

When rendering charts for VLMs:

- render only bars available at the decision timestamp;
- never include a future candle at the right edge;
- keep image dimensions and layout versioned;
- record symbol, timeframe, decision timestamp and renderer version outside the image as metadata;
- do not draw labels or outcomes that reveal the target.

## Minimum provenance record

Every serious experiment should be able to answer:

```text
source/provider:
symbol:
base timeframe:
raw first timestamp:
raw last timestamp:
timezone:
bar timestamp semantics:
downloader/export version:
normalization script version:
raw hash or manifest:
derived dataset version:
train/validation/test boundaries:
```

Without this information, a strong model metric can be impossible to reproduce or audit.

## Contribution opportunity

A good community contribution is a data adapter that converts a legal public or user-supplied source into the canonical close-indexed OHLCV representation while preserving provenance and causality.

The first connector does not need to support every market. One well-tested FX, equity or crypto source is more useful than many fragile downloaders.