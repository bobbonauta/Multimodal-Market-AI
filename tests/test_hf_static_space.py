import importlib.util
from pathlib import Path
from types import ModuleType

import pandas as pd

from multimodal_market_ai.synthetic_demo import write_demo

ROOT = Path(__file__).resolve().parents[1]
DATASET_URL = "https://huggingface.co/datasets/example/multimodal-market-ai-synthetic"


def _load_static_page() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "static_page",
        ROOT / "huggingface" / "static_page.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build(tmp_path: Path, name: str) -> Path:
    demo_dir = tmp_path / f"{name}_demo"
    space_dir = tmp_path / f"{name}_space"
    write_demo(demo_dir)
    _load_static_page().build_static_space(demo_dir, space_dir, DATASET_URL)
    return space_dir


def test_static_space_contains_page_data_and_images(tmp_path: Path) -> None:
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

    readme = (space / "README.md").read_text(encoding="utf-8")
    assert "sdk: static" in readme
    assert "app_file: index.html" in readme


def test_static_page_shows_all_teaching_decisions_and_no_leftover_placeholders(
    tmp_path: Path,
) -> None:
    page = (_build(tmp_path, "one") / "index.html").read_text(encoding="utf-8")

    for decision in ("LONG", "WAIT", "SHORT"):
        assert f'<span class="badge {decision.lower()}">{decision}</span>' in page

    assert "<!--FUSION_TABLE-->" not in page
    assert "{{DATASET_URL}}" not in page
    assert DATASET_URL in page


def test_static_page_is_reproducible(tmp_path: Path) -> None:
    first = _build(tmp_path, "first")
    second = _build(tmp_path, "second")

    assert (first / "index.html").read_bytes() == (second / "index.html").read_bytes()


def test_fusion_rows_escape_html() -> None:
    fusion = pd.DataFrame(
        [
            {
                "case_id": "<script>alert(1)</script>",
                "decision_ts": "2026-01-02 05:00:00+00:00",
                "trend_signal": 1,
                "momentum_signal": 0,
                "structure_signal": -1,
                "mock_visual_score": 0.0188,
                "visual_signal": 1,
                "det_signal": 1,
                "decision": "LONG",
            }
        ]
    )

    rows = _load_static_page().render_fusion_rows(fusion)

    assert "<script>" not in rows
    assert "&lt;script&gt;" in rows
    assert "+1" in rows
    assert "-1" in rows
