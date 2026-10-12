"""Build the Hugging Face dataset card and static Space from the repository README.

The README is the single source of truth: both Hugging Face surfaces are generated from it, so
they stay equal to GitHub apart from look and link targets. Relative links cannot work outside the
repository, so they are rewritten to GitHub (or to the copy of the chart images that ships next to
the page).

This module deliberately does not import ``huggingface_hub`` so it can be tested in CI without the
optional ``hf`` extra.
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML

REPO_URL = "https://github.com/bobbonauta/Multimodal-Market-AI"
TEMPLATE_DIR = Path(__file__).resolve().parent / "space_static"
BODY_PLACEHOLDER = "<!--README_BODY-->"
IMAGE_PREFIX = "examples/synthetic_multimodal/output/images/"

_ABSOLUTE = ("#", "http://", "https://", "mailto:")
_LINK_TARGET = re.compile(r"(\]\()([^)\s]+)(\))")
_FENCE = re.compile(r"^\s*(```|~~~)")


def rewrite_target(target: str) -> str:
    """Point a README link/image at something that exists outside the repository checkout."""
    if target.startswith(_ABSOLUTE):
        return target
    if target.startswith(IMAGE_PREFIX):
        return "images/" + target[len(IMAGE_PREFIX) :]
    return f"{REPO_URL}/blob/main/{target}"


def rewrite_markdown_links(markdown_text: str) -> str:
    """Rewrite link targets in Markdown source, line by line, leaving code fences alone."""
    lines: list[str] = []
    in_fence = False
    for line in markdown_text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            line = _LINK_TARGET.sub(
                lambda match: match[1] + rewrite_target(match[2]) + match[3],
                line,
            )
        lines.append(line)
    return "\n".join(lines)


def build_card(frontmatter_path: Path, readme_text: str) -> str:
    """Hub card = the repository's own YAML metadata + the README body."""
    header = frontmatter_path.read_text(encoding="utf-8").strip("\n")
    body = rewrite_markdown_links(readme_text).strip("\n")
    return f"---\n{header}\n---\n\n{body}\n"


def _slug(text: str) -> str:
    """GitHub-style heading anchor, so in-page links such as ``#project-status`` still work."""
    return re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")


def _render_fence(
    self: RendererHTML,
    tokens: list,
    idx: int,
    options: dict,
    env: dict,
) -> str:
    token = tokens[idx]
    if token.info.strip() == "mermaid":
        # mermaid.js turns this into a diagram, as GitHub does; without JavaScript the
        # source stays readable.
        return f'<pre class="mermaid">{html.escape(token.content)}</pre>\n'
    return RendererHTML.fence(self, tokens, idx, options, env)


def render_html(readme_text: str) -> str:
    """Render the README as an HTML fragment (raw HTML in the source is escaped, not passed)."""
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    md.add_render_rule("fence", _render_fence)
    tokens = md.parse(readme_text)

    seen: dict[str, int] = {}
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            inline = tokens[index + 1]
            text = "".join(
                child.content
                for child in inline.children or []
                if child.type in {"text", "code_inline"}
            )
            slug = _slug(text)
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            token.attrSet("id", slug if not count else f"{slug}-{count}")
        for child in token.children or []:
            if child.type == "link_open":
                child.attrSet("href", rewrite_target(str(child.attrGet("href"))))
            elif child.type == "image":
                child.attrSet("src", rewrite_target(str(child.attrGet("src"))))

    return md.renderer.render(tokens, md.options, {})


def build_static_space(demo_dir: Path, destination: Path, readme_text: str) -> None:
    """Assemble the static Space from the README and a ``write_demo`` output folder.

    ``demo_dir`` must contain ``fusion_table.csv``, ``market.csv`` and ``images/``. The page needs
    no server and no build step: the README is rendered here, once.
    """
    destination.mkdir(parents=True, exist_ok=True)

    template = (TEMPLATE_DIR / "index.template.html").read_text(encoding="utf-8")
    page = template.replace(BODY_PLACEHOLDER, render_html(readme_text))
    (destination / "index.html").write_text(page, encoding="utf-8", newline="\n")

    card = build_card(TEMPLATE_DIR / "frontmatter.yml", readme_text)
    (destination / "README.md").write_text(card, encoding="utf-8", newline="\n")

    shutil.copy2(demo_dir / "fusion_table.csv", destination / "fusion_table.csv")
    shutil.copy2(demo_dir / "market.csv", destination / "market.csv")
    shutil.copytree(demo_dir / "images", destination / "images", dirs_exist_ok=True)
