"""Build the static (HTML-only) Hugging Face Space from the synthetic demo output.

This module deliberately does not import ``huggingface_hub`` so it can be tested in CI
without the optional ``hf`` extra.
"""

from __future__ import annotations

import html
import shutil
from pathlib import Path

import pandas as pd

TEMPLATE_DIR = Path(__file__).resolve().parent / "space_static"
TABLE_PLACEHOLDER = "<!--FUSION_TABLE-->"
DATASET_URL_PLACEHOLDER = "{{DATASET_URL}}"


def _signed(value: float, digits: int = 0) -> str:
    """Format a signal with an explicit sign so +1 / 0 / -1 line up."""
    number = float(value)
    if digits == 0:
        whole = round(number)
        return f"{whole:+d}" if whole else "0"
    return f"{number:+.{digits}f}"


def _signal_class(value: float) -> str:
    number = float(value)
    if number > 0:
        return "up"
    if number < 0:
        return "down"
    return "flat"


def _signal_cell(value: float, digits: int = 0) -> str:
    return f'<td class="sig {_signal_class(value)}">{_signed(value, digits)}</td>'


def render_fusion_rows(fusion: pd.DataFrame) -> str:
    """Render the fusion table as ``<tr>`` rows, one per decision/event."""
    rows: list[str] = []
    for record in fusion.to_dict(orient="records"):
        decision = str(record["decision"])
        decision_time = pd.Timestamp(record["decision_ts"]).strftime("%Y-%m-%d %H:%M")
        cells = [
            f"<td>{html.escape(str(record['case_id']))}</td>",
            f"<td>{html.escape(decision_time)}</td>",
            _signal_cell(record["trend_signal"]),
            _signal_cell(record["momentum_signal"]),
            _signal_cell(record["structure_signal"]),
            _signal_cell(record["mock_visual_score"], digits=4),
            _signal_cell(record["visual_signal"]),
            _signal_cell(record["det_signal"]),
            (
                f'<td><span class="badge {html.escape(decision.lower())}">'
                f"{html.escape(decision)}</span></td>"
            ),
        ]
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "\n".join(rows)


def build_static_space(demo_dir: Path, destination: Path, dataset_url: str) -> None:
    """Assemble the static Space from a ``write_demo`` output folder.

    ``demo_dir`` must contain ``fusion_table.csv``, ``market.csv`` and ``images/``.
    The page needs no JavaScript and no server: the table is rendered here, once.
    """
    destination.mkdir(parents=True, exist_ok=True)
    fusion = pd.read_csv(demo_dir / "fusion_table.csv")

    page = (TEMPLATE_DIR / "index.template.html").read_text(encoding="utf-8")
    page = page.replace(TABLE_PLACEHOLDER, render_fusion_rows(fusion))
    page = page.replace(DATASET_URL_PLACEHOLDER, html.escape(dataset_url, quote=True))
    (destination / "index.html").write_text(page, encoding="utf-8", newline="\n")

    shutil.copy2(TEMPLATE_DIR / "README.md", destination / "README.md")
    shutil.copy2(demo_dir / "fusion_table.csv", destination / "fusion_table.csv")
    shutil.copy2(demo_dir / "market.csv", destination / "market.csv")
    shutil.copytree(demo_dir / "images", destination / "images", dirs_exist_ok=True)
