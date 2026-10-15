---
title: Multimodal Market AI Demo
emoji: 📈
colorFrom: blue
colorTo: gray
sdk: static
app_file: index.html
pinned: false
license: apache-2.0
short_description: Synthetic multimodal fusion demo. Not a trading bot.
---

# Multimodal Market AI — static demo

A static page that shows the output of the public synthetic pipeline:

```text
fake OHLCV
  -> deterministic signals
  -> chart images
  -> mock visual signal
  -> fusion table
  -> LONG / WAIT / SHORT
```

Everything is fake and precomputed from the open-source code. It is an engineering/research
demonstration, not a trading bot or signal service.

## Latest public research snapshot

The project now also publishes a larger October 2026 visual-model arena: **5 open VLM
configurations × 1,000 frozen cases**, with **5,000/5,000 valid outputs** across two independent
500-case tranches per model.

The published metrics are aggregate agreement/stability measurements only. The deterministic
comparison reference is not ground truth, and private strategy rules, task meanings, cases and
adapter weights remain closed.

Full public-safe results:
`https://github.com/bobbonauta/Multimodal-Market-AI/blob/main/docs/LARGE_SAMPLE_VISUAL_ARENA_2026_10.md`

Canonical source:
`https://github.com/bobbonauta/Multimodal-Market-AI`
