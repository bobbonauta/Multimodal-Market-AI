import importlib.util
import re
from pathlib import Path
from types import ModuleType

from multimodal_market_ai.synthetic_demo import write_demo

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def _load_static_page() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "static_page",
        ROOT / "huggingface" / "static_page.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build(tmp_path: Path, name: str, readme: str = README) -> Path:
    demo_dir = tmp_path / f"{name}_demo"
    space_dir = tmp_path / f"{name}_space"
    write_demo(demo_dir)
    _load_static_page().build_static_space(demo_dir, space_dir, readme)
    return space_dir


def _headings(markdown: str) -> list[str]:
    """Heading texts of a Markdown document, ignoring code fences."""
    found: list[str] = []
    in_fence = False
    for line in markdown.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and (match := re.match(r"#{1,6} (.+)", line)):
            found.append(match[1].strip())
    return found


def test_static_space_contains_page_card_data_and_images(tmp_path: Path) -> None:
    space = _build(tmp_path, "one")

    for relative in (
        "index.html",
        "README.md",
        "fusion_table.csv",
        "market.csv",
        "images/case_001.svg",
        "images/case_002.svg",
        "images/case_003.svg",
    ):
        assert (space / relative).is_file(), relative
    assert not (space / "style.css").exists()

    card = (space / "README.md").read_text(encoding="utf-8")
    assert card.startswith("---\n")
    assert "sdk: static" in card
    assert "app_file: index.html" in card


def test_page_and_card_carry_every_readme_heading(tmp_path: Path) -> None:
    space = _build(tmp_path, "one")
    page = (space / "index.html").read_text(encoding="utf-8")
    card = (space / "README.md").read_text(encoding="utf-8")
    module = _load_static_page()

    headings = _headings(README)
    assert len(headings) > 10  # the README really has its sections
    for heading in headings:
        assert f"{heading}</h" in page.replace("&amp;", "&"), heading
        assert heading in card, heading

    # In-page anchors keep working: [status badge](#project-status) needs this id.
    assert 'id="project-status"' in page
    assert module._slug("What is a fusion table?") == "what-is-a-fusion-table"


def test_readme_diagram_is_kept_for_mermaid(tmp_path: Path) -> None:
    page = (_build(tmp_path, "one") / "index.html").read_text(encoding="utf-8")

    assert '<pre class="mermaid">flowchart LR' in page
    assert "A[Market data] --&gt; B[Deterministic extractor]" in page


def test_no_relative_link_or_image_is_left_broken(tmp_path: Path) -> None:
    space = _build(tmp_path, "one")
    page = (space / "index.html").read_text(encoding="utf-8")
    card = (space / "README.md").read_text(encoding="utf-8")

    for target in re.findall(r'(?:href|src)="([^"]+)"', page):
        assert target.startswith(("https://", "#", "images/")), target
    for target in re.findall(r"\]\(([^)\s]+)\)", card):
        assert target.startswith(("https://", "#", "images/")), target

    for image in re.findall(r'src="(images/[^"]+)"', page):
        assert (space / image).is_file(), image
    assert "https://github.com/bobbonauta/Multimodal-Market-AI/blob/main/docs/ROADMAP.md" in page


def test_card_changes_nothing_but_link_targets() -> None:
    module = _load_static_page()
    card_body = module.rewrite_markdown_links(README)

    def blank_targets(text: str) -> str:
        return re.sub(r"\]\([^)\s]+\)", "](X)", text)

    assert card_body.count("\n") == README.count("\n")
    assert blank_targets(card_body) == blank_targets(README)
    # Code stays exactly as written: the install command contains "[dev]" but no link.
    assert 'pip install -e ".[dev]"' in card_body


def test_static_page_is_reproducible(tmp_path: Path) -> None:
    first = _build(tmp_path, "first")
    second = _build(tmp_path, "second")

    for name in ("index.html", "README.md"):
        assert (first / name).read_bytes() == (second / name).read_bytes()


def test_raw_html_in_the_readme_is_not_passed_through(tmp_path: Path) -> None:
    hostile = "# Title\n\n<script>alert(1)</script>\n\n[x](docs/A.md)\n"
    page = (_build(tmp_path, "one", readme=hostile) / "index.html").read_text(encoding="utf-8")

    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
