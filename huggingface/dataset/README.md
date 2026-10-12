---
license: apache-2.0
pretty_name: Multimodal Market AI Synthetic Demo
size_categories:
- n<1K
tags:
- finance
- synthetic
- multimodal
- time-series
- causal-inference
---

# Multimodal Market AI — synthetic demo dataset

A tiny, fully synthetic dataset for demonstrating the public Multimodal Market AI workflow.

It contains:

- 90 fake OHLCV bars;
- three decision/event rows;
- three SVG chart images;
- deterministic teaching signals;
- a mock visual feature;
- a fusion table with `LONG`, `WAIT` and `SHORT` example decisions.

No real market record, proprietary strategy rule or private feature is included.

## Purpose

The dataset exists so a new user can understand and test the data contract before connecting a
real bot, real market feed or real VLM.

## Important

This is an educational engineering dataset, not a trading dataset and not evidence of
profitability.

Canonical source:
`https://github.com/bobbonauta/Multimodal-Market-AI`
