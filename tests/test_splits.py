import pandas as pd
import pytest

from multimodal_market_ai.splits import (
    TemporalSplitError,
    apply_numeric_statistics,
    fit_numeric_statistics,
    purged_temporal_split,
)


def _frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "decision_ts": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05", "2026-01-06"],
                utc=True,
            ),
            "outcome_end_ts": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-04", "2026-01-04", "2026-01-06", "2026-01-07"],
                utc=True,
            ),
            "group": ["a", "b", "c", "d", "e", "f"],
            "feature": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        }
    )


def test_purged_temporal_split_respects_outcome_boundaries() -> None:
    split = purged_temporal_split(
        _frame(), train_end="2026-01-03", validation_end="2026-01-05"
    )

    assert split.train.index.tolist() == [0, 1]
    assert split.validation.index.tolist() == [3]
    assert split.test.index.tolist() == [5]
    assert split.excluded.index.tolist() == [2, 4]


def test_groups_crossing_periods_are_purged_from_each_period() -> None:
    frame = _frame()
    frame.loc[0, "group"] = "shared"
    frame.loc[3, "group"] = "shared"

    split = purged_temporal_split(
        frame,
        train_end="2026-01-03",
        validation_end="2026-01-05",
        group_id="group",
    )

    assert 0 not in split.train.index
    assert 3 not in split.validation.index
    assert split.statistics["group_purged_rows"] == 2


def test_validation_mutation_does_not_change_training_preprocessing() -> None:
    split = purged_temporal_split(
        _frame(), train_end="2026-01-03", validation_end="2026-01-05"
    )
    fitted = fit_numeric_statistics(split.train, ["feature"])
    changed_validation = split.validation.copy()
    changed_validation.loc[:, "feature"] = 1_000_000.0

    assert fit_numeric_statistics(split.train, ["feature"]) == fitted
    transformed = apply_numeric_statistics(changed_validation, fitted)
    assert transformed["feature"].iloc[0] > 100_000.0


def test_invalid_temporal_boundaries_fail_closed() -> None:
    with pytest.raises(TemporalSplitError):
        purged_temporal_split(_frame(), train_end="2026-01-05", validation_end="2026-01-03")
