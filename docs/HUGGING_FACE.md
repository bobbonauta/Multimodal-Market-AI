# Hugging Face export

GitHub is the canonical source for Multimodal Market AI.

Hugging Face is used as a discovery and demo surface for:

1. the small synthetic multimodal dataset;
2. a static Space showing the demo output at a glance;
3. future public adapters or model cards when there is something safe and useful to publish.

This avoids maintaining two independent versions of the project.

## What is prepared

```text
huggingface/
    dataset/
        README.md           dataset card
    space/              Gradio Space (interactive)
        README.md
        app.py
        requirements.txt
    space_static/       static Space (plain HTML, default)
        README.md
        index.template.html
    static_page.py      builds the static Space from the synthetic demo output
    export_to_hub.py
```

The export script assembles the Hugging Face repositories from the current GitHub checkout.

## Three pages, three jobs

The pages do not copy each other, and none of them copies the root `README.md`.

| Page | Job |
|---|---|
| GitHub `README.md` | explains the whole project |
| Hugging Face dataset card (`dataset/README.md`) | describes the data only: what is in it, the schema, how it is generated, its limits, its license |
| Hugging Face static Space (`space_static/`) | shows the demo at a glance: the pipeline, the fusion table, the three charts, the mock visual adapter and `LONG` / `WAIT` / `SHORT` |

Each Hugging Face page links back to the canonical GitHub repository, and the Space links to the
dataset.

## Publishing order

Hugging Face is exported from `main`, after the change is merged and CI is green on `main`:

1. work on a branch;
2. test and review it;
3. merge it into `main`;
4. check that CI on `main` is green;
5. export to Hugging Face from `main`.

Never export from a branch that has not been merged. `export_to_hub.py` enforces this with one
check: a real export refuses to run when the checked-out Git branch is not `main`.

## Requirements

The Hugging Face account/token must have **write** permission.

Install the optional dependency:

```bash
pip install -e ".[hf]"
```

Authenticate in one of the standard Hugging Face ways, for example by setting `HF_TOKEN` in the
environment. Never commit the token.

## Preview without uploading

```bash
python huggingface/export_to_hub.py --dry-run
```

`--dry-run` builds the export folders and uploads nothing, so it works on any branch.

The default repository names are:

```text
<your-user>/multimodal-market-ai-synthetic
<your-user>/multimodal-market-ai-demo
```

You can override them:

```bash
python huggingface/export_to_hub.py \
  --dataset-name my-dataset-name \
  --space-name my-space-name
```

## Upload

From a clean checkout of `main`:

```bash
python huggingface/export_to_hub.py
```

On any other branch the script stops before it contacts Hugging Face:

```text
Refusing Hugging Face publish: current Git branch is not main (...). Merge and verify main before publishing.
```

The script:

1. regenerates the synthetic demo;
2. creates a temporary dataset export directory;
3. creates a temporary Space export directory;
4. copies only public-safe files;
5. creates the Hub repositories if needed;
6. uploads the folders.

It does **not** upload:

- private datasets;
- private strategy rules;
- private feature names;
- private adapters;
- broker/account information;
- local secrets.

## Dataset contents

The synthetic dataset contains:

- `market.csv`;
- `fusion_table.csv`;
- three generated SVG chart images;
- a dataset card (`dataset/README.md`).

Everything is synthetic and reproducible from the GitHub code.

## Static or Gradio Space

`export_to_hub.py` can create two kinds of Space, chosen with `--space-type`:

| Type | Command | Needs |
|---|---|---|
| `static` (default) | `python huggingface/export_to_hub.py` | nothing extra, free on every account |
| `gradio` | `python huggingface/export_to_hub.py --space-type gradio` | compute; Gradio Spaces normally need a paid plan (a free account may only have limited options such as ZeroGPU) |

The static Space is a single HTML page with the fusion table, the three chart images and the raw
CSV files. It needs no server: the demo is deterministic, so its output is computed once, at export
time, and written into the page. The only thing it cannot do is the "Regenerate" button of the
Gradio version, which always produced the same result anyway.

The static export removes the `style.css` that Hugging Face puts in every new static Space, because
the page carries its own styles.

## Space contents (Gradio, `--space-type gradio`)

The Gradio Space contains:

- a tiny Gradio UI;
- the public synthetic demo generator;
- the public deterministic combiner;
- generated charts and fusion-table output.

The Space runs on CPU and is educational. It is not a trading service.
