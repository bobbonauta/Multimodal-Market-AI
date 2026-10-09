from __future__ import annotations

import pandas as pd
import pytest

from multimodal_market_ai.deterministic import (
    DeterministicModelError,
    combine_directional_signals,
)


def test_majority_policy_uses_more_votes() -> None:
    frame = pd.DataFrame(
        {
            "a": [1, -1, 1],
            "b": [1, -1, -1],
            "c": [-1, 1, 0],
        }
    )

    out = combine_directional_signals(frame, ["a", "b", "c"], policy="majority")

    assert out["det_signal"].tolist() == [1, -1, 0]
    assert out["det_active_signals"].tolist() == [3, 3, 2]


def test_unanimous_policy_requires_active_votes_to_agree() -> None:
    frame = pd.DataFrame(
        {
            "a": [1, 1, -1],
            "b": [1, -1, -1],
            "c": [0, 0, -1],
        }
    )

    out = combine_directional_signals(
        frame,
        ["a", "b", "c"],
        policy="unanimous",
        minimum_active=2,
    )

    assert out["det_signal"].tolist() == [1, 0, -1]


def test_weighted_policy_can_give_more_importance_to_one_rule() -> None:
    frame = pd.DataFrame({"a": [1], "b": [-1], "c": [-1]})

    out = combine_directional_signals(
        frame,
        ["a", "b", "c"],
        policy="weighted",
        weights={"a": 0.8, "b": 0.1, "c": 0.1},
        weighted_threshold=0.5,
    )

    assert out.loc[0, "det_signal"] == 1
    assert out.loc[0, "det_score"] == pytest.approx(0.6)


def test_minimum_active_can_block_a_weak_row() -> None:
    frame = pd.DataFrame({"a": [1], "b": [0], "c": [0]})

    out = combine_directional_signals(
        frame,
        ["a", "b", "c"],
        policy="majority",
        minimum_active=2,
    )

    assert out.loc[0, "det_signal"] == 0


def test_invalid_signal_values_are_rejected() -> None:
    frame = pd.DataFrame({"a": [1], "b": [2]})

    with pytest.raises(DeterministicModelError, match=r"-1, 0 or \+1"):
        combine_directional_signals(frame, ["a", "b"])


def test_original_frame_is_not_changed() -> None:
    frame = pd.DataFrame({"a": [1], "b": [-1]})
    original_columns = frame.columns.tolist()

    combine_directional_signals(frame, ["a", "b"])

    assert frame.columns.tolist() == original_columns
