# Model adapters: how to plug multimodal models into the framework

Multimodal Market AI should support different model families without coupling the rest of the project to one vendor or architecture.

The adapter layer exists so that InternVL, Qwen-VL-family models, Gemma-family multimodal models and future backends can expose a **common research interface** while keeping model-specific loading, prompting and generation logic isolated.

## What an adapter is

An adapter is a small integration layer between the framework and a base model.

Conceptually:

```text
MarketSample
  - chart image(s)
  - numerical/context fields
  - prompt/task schema
        |
        v
ModelAdapter
  - load base model
  - preprocess image/text
  - run inference
  - parse structured output
  - report runtime/memory metadata
        |
        v
ModelReading / MarketState contribution
```

The rest of the project should not need to know whether the backend is InternVL, Qwen, Gemma or another multimodal model.

## Why adapters matter

Different VLM families differ in:

- image preprocessing;
- number and ordering of images;
- chat templates;
- special tokens;
- dynamic tiling / image patches;
- precision and quantization support;
- generation APIs;
- LoRA target module names;
- checkpoint format;
- model-specific structured-output behavior.

Keeping these differences behind an adapter makes experiments easier to compare fairly.

## Suggested public interface

A future adapter interface may look approximately like this:

```python
class MultimodalAdapter:
    model_id: str
    revision: str

    def load(self, device: str): ...

    def prepare(self, sample): ...

    def infer(self, sample, generation_config): ...

    def parse(self, raw_output): ...

    def runtime_info(self) -> dict: ...
```

This is an architectural guide, not yet a frozen API.

## Minimum metadata every adapter should expose

Every adapter contribution should record:

```text
model family:
model id:
exact revision / commit:
upstream license:
transformers/model-library version:
torch version:
CUDA / ROCm / CPU backend:
precision:
quantization:
attention backend:
image resolution / tiling:
number of images per sample:
max generation tokens:
generation mode:
VRAM / RAM observed:
latency / throughput:
```

This matters because two experiments that both say "Qwen" or "InternVL" may actually be running very different revisions and inference paths.

## Base-model weights vs training adapters

The word *adapter* is used in two related but different ways:

1. **framework adapter** — Python integration code that lets the project talk to a model family;
2. **training adapter** — learned PEFT/LoRA weights attached to a specific base model.

They should not be confused.

A framework adapter can support many checkpoints in one model family. A LoRA adapter is learned data and is tied to the architecture it was trained against.

## Important: LoRA adapters are architecture-specific

A LoRA adapter trained for InternVL cannot normally be attached directly to Qwen or Gemma.

Even models with similar parameter counts can use different:

- layer names;
- tensor shapes;
- attention modules;
- projector architecture;
- tokenizer/chat templates.

What **can** be reused across model families is the research protocol:

```text
same dataset
same images
same temporal split
same targets
same evaluation set
same output schema
same leakage rules
same economic evaluation
```

Each base-model family then receives its own fine-tuning run and its own learned adapter.

## Recommended directory structure

A future implementation can keep integrations clean with a layout such as:

```text
src/multimodal_market_ai/models/
  base.py
  internvl.py
  qwen_vl.py
  gemma.py

configs/models/
  internvl35_2b.yaml
  qwen_vl_example.yaml

runs/
  experiment_name/
    config.yaml
    checkpoints/
    adapter_final/
    metrics.json
```

Large model weights and training outputs should normally remain outside Git.

## Loading strategy

The normal loading sequence should be:

1. resolve an exact upstream model revision;
2. check the upstream license;
3. load processor/tokenizer and model from the same revision;
4. select precision/quantization appropriate for available hardware;
5. run a tiny inference smoke test;
6. record VRAM/RAM and output validity;
7. only then start a large benchmark or fine-tuning job.

Do not discover basic incompatibilities after several hours of training.

## Structured outputs

Free-form prose is difficult to evaluate automatically. Adapters should support structured tasks where practical.

Example:

```json
{
  "regime": "trend",
  "direction": "long",
  "confidence": 0.64,
  "ambiguity": true
}
```

The public framework should validate output syntax separately from whether the prediction is correct.

Useful metrics include:

- valid structured output rate;
- task F1 / accuracy where appropriate;
- latency;
- tokens generated;
- VRAM/RAM;
- agreement with serial/reference inference;
- economic metrics only when the task legitimately supports them.

## Multiple images / multiple timeframes

A multimodal adapter should not assume that every experiment uses one image.

Typical market samples may contain:

```text
image 1 -> lower timeframe
image 2 -> middle timeframe
image 3 -> higher timeframe
```

The adapter must document image order because swapping timeframes can silently change model behavior.

A good dataset record should carry explicit labels such as:

```json
{
  "images": {
    "fast": "...png",
    "middle": "...png",
    "slow": "...png"
  }
}
```

rather than relying only on positional filenames.

## Creating a new model-family adapter

Recommended sequence for contributors:

1. choose an openly usable upstream model and lock the exact revision;
2. implement model loading only;
3. add a five-sample or synthetic smoke test;
4. implement deterministic preprocessing;
5. add one structured inference task;
6. measure CPU RAM / GPU VRAM and latency;
7. make repeated inference reproducible where the model/library allows it;
8. document batch behavior separately from serial behavior;
9. add optional fine-tuning support only after inference is stable;
10. submit benchmark results with the pull request.

## Serial vs batch inference

Do not assume batched autoregressive VLM inference produces exactly the same token sequence as serial inference.

Prior research found cases where batching was substantially faster but tiny numerical differences inside the visual/prefill path changed near-tied token decisions. This is hardware/model dependent, but it is important enough to test explicitly.

For any claimed fast path, report:

- serial outputs;
- batched outputs;
- exact agreement rate;
- speedup;
- batch size;
- precision;
- deterministic settings;
- any known divergence cases.

A fast path is not automatically a replacement for a reference path if it changes decisions.

## Adapter contribution checklist

Before opening a PR for a model adapter, confirm:

- [ ] no proprietary strategy logic is embedded;
- [ ] exact upstream model and revision are documented;
- [ ] upstream license is documented;
- [ ] no model weights are committed unless redistribution is explicitly allowed;
- [ ] smoke inference works from a clean environment;
- [ ] structured output example is included;
- [ ] hardware/runtime information is included;
- [ ] no future market information is used in the example input;
- [ ] batch/serial behavior is documented if batching is supported;
- [ ] large downloads are not required in normal CI.

See also [Fine-tuning guide](FINETUNING_GUIDE.md) and [Benchmarking](BENCHMARKING.md).