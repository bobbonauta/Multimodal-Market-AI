from pathlib import Path

import pandas as pd

from multimodal_market_ai.synthetic_demo import (
    build_fusion_table,
    generate_synthetic_market,
    write_demo,
)


def test_synthetic_demo_has_three_teaching_decisions(tmp_path: Path) -> None:
    fusion = write_demo(tmp_path)

    assert fusion["decision"].tolist() == ["LONG", "WAIT", "SHORT"]
    assert fusion["case_id"].tolist() == ["case_001", "case_002", "case_003"]

    for case_id in fusion["case_id"]:
        assert (tmp_path / "images" / f"{case_id}.svg").is_file()

    assert (tmp_path / "market.csv").is_file()
    assert (tmp_path / "fusion_table.csv").is_file()


def test_synthetic_cases_never_use_rows_after_decision_time() -> None:
    fusion = build_fusion_table(generate_synthetic_market())

    decision_ts = pd.to_datetime(fusion["decision_ts"], utc=True)
    source_end_ts = pd.to_datetime(fusion["source_end_ts"], utc=True)

    assert source_end_ts.le(decision_ts).all()


def test_synthetic_demo_is_reproducible(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    write_demo(first)
    write_demo(second)

    assert (first / "market.csv").read_bytes() == (second / "market.csv").read_bytes()
    assert (first / "fusion_table.csv").read_bytes() == (
        second / "fusion_table.csv"
    ).read_bytes()

    for case_id in ("case_001", "case_002", "case_003"):
        assert (first / "images" / f"{case_id}.svg").read_bytes() == (
            second / "images" / f"{case_id}.svg"
        ).read_bytes()
