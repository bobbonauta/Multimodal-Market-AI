# Hugging Face export

GitHub is the canonical source for Multimodal Market AI.

Hugging Face is used as a discovery and demo surface for:

1. the small synthetic multimodal dataset;
2. a CPU-only Space showing the same demo;
3. future public adapters or model cards when there is something safe and useful to publish.

This avoids maintaining two independent versions of the project.

## What is prepared

```text
huggingface/
    dataset/
        frontmatter.yml     dataset card metadata (license, tags, size)
    space/                  Gradio Space (interactive)
        README.md
        app.py
        requirements.txt
    space_static/           static Space (plain HTML, default)
        frontmatter.yml     Space card metadata (sdk: static, app_file)
        index.template.html page wrapper: styles and the mermaid script
    static_page.py          turns the root README.md into the Space page and the cards
    export_to_hub.py
```

The export script assembles the Hugging Face repositories from the current GitHub checkout.

## One README, three pages

The root `README.md` is the only place where the project text is written. The export builds from it:

| Hugging Face page | Built as |
|---|---|
| Dataset card | `dataset/frontmatter.yml` + the README text |
| Static Space card | `space_static/frontmatter.yml` + the README text |
| Static Space page (`index.html`) | the README rendered to HTML inside `index.template.html` |

So the Hugging Face pages say exactly what the GitHub page says. They differ only in two ways:

- **Look.** The Space page has its own light/dark styling. The cards use the Hub's own rendering.
- **Link targets.** A link such as `docs/ROADMAP.md` only works inside the GitHub repository, so on
  Hugging Face it points to the same file on GitHub. The three chart images are copied next to the
  page and linked from there.

Nothing else is rewritten: code blocks stay as written. To change what the Hugging Face pages say,
edit `README.md` and run the export again; there is no second copy to keep in sync.

The README's diagram is a `mermaid` block. GitHub draws it itself. The Space page draws it with
mermaid.js, which the visitor's browser loads from a CDN (jsDelivr, pinned to one version). If that
script cannot load, the diagram source stays on the page as text. The dataset card does not draw
it: the Hub's card renderer shows the same `mermaid` block as plain source code.

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

```bash
python huggingface/export_to_hub.py
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
- a dataset card (the project README, see above).

Everything is synthetic and reproducible from the GitHub code.

## Static or Gradio Space

`export_to_hub.py` can create two kinds of Space, chosen with `--space-type`:

| Type | Command | Needs |
|---|---|---|
| `static` (default) | `python huggingface/export_to_hub.py` | nothing extra, free on every account |
| `gradio` | `python huggingface/export_to_hub.py --space-type gradio` | a Hugging Face PRO subscription for CPU hosting |

The static Space is a single HTML page: the project README, with the three chart images and the raw
CSV files next to it. It needs no server: the demo is deterministic, so its output is computed once,
at export time, and written into the Space. The only thing it cannot do is the "Regenerate" button
of the Gradio version, which always produced the same result anyway.

The static export removes the `style.css` that Hugging Face puts in every new static Space, because
the page carries its own styles.

## Space contents (Gradio, `--space-type gradio`)

The Gradio Space contains:

- a tiny Gradio UI;
- the public synthetic demo generator;
- the public deterministic combiner;
- generated charts and fusion-table output.

The Space runs on CPU and is educational. It is not a trading service.
