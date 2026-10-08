"""Purged time-ordered splits and training-only numeric preprocessing helpers."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd


class TemporalSplitError(ValueError):
    """Raised when timestamp or grouping inputs cannot define a safe temporal split."""


@dataclass(frozen=True)
class TemporalSplit:
    """Rows assigned to each period, with purged rows kept separately."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame
    excluded: pd.DataFrame
    statistics: Mapping[str, int]


def _utc_timestamp(value: object, label: str) -> pd.Timestamp:
    try:
        parsed = pd.to_datetime(value, utc=True, errors="raise")
    except (TypeError, ValueError) as exc:
        raise TemporalSplitError(f"{label} must be a valid timestamp") from exc
    if not isinstance(parsed, pd.Timestamp) or pd.isna(parsed):
        raise TemporalSplitError(f"{label} must be a single valid timestamp")
    return parsed


def purged_temporal_split(
    frame: pd.DataFrame,
    *,
    decision_ts: str = "decision_ts",
    outcome_end_ts: str = "outcome_end_ts",
    train_end: object,
    validation_end: object,
    group_id: str | None = None,
) -> TemporalSplit:
    """Split rows by decision time and purge outcomes that cross a split boundary."""
    if not isinstance(frame, pd.DataFrame):
        raise TemporalSplitError("input must be a pandas DataFrame")
    required = [decision_ts, outcome_end_ts]
    if group_id is not None:
        required.append(group_id)
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise TemporalSplitError(f"required columns are missing: {missing}")

    train_cutoff = _utc_timestamp(train_end, "train_end")
    validation_cutoff = _utc_timestamp(validation_end, "validation_end")
    if train_cutoff >= validation_cutoff:
        raise TemporalSplitError("train_end must be earlier than validation_end")

    decisions = pd.to_datetime(frame[decision_ts], utc=True, errors="coerce")
    outcomes = pd.to_datetime(frame[outcome_end_ts], utc=True, errors="coerce")
    if decisions.isna().any() or outcomes.isna().any():
        raise TemporalSplitError("decision and outcome timestamps must be present and valid")
    if (outcomes < decisions).any():
        raise TemporalSplitError("outcome_end_ts cannot precede decision_ts")

    train_mask = (decisions <= train_cutoff) & (outcomes <= train_cutoff)
    validation_mask = (
        (decisions > train_cutoff)
        & (decisions <= validation_cutoff)
        & (outcomes <= validation_cutoff)
    )
    test_mask = decisions > validation_cutoff
    base_masks = {
        "train": train_mask.to_numpy(dtype=bool, copy=True),
        "validation": validation_mask.to_numpy(dtype=bool, copy=True),
        "test": test_mask.to_numpy(dtype=bool, copy=True),
    }

    group_purged = np.zeros(len(frame), dtype=bool)
    if group_id is not None:
        group_values = frame[group_id].tolist()
        partitions_by_group: dict[object, set[str]] = {}
        for position, value in enumerate(group_values):
            if not pd.api.types.is_scalar(value):
                raise TemporalSplitError("group_id values must be scalar and hashable")
            if pd.isna(value):
                continue
            try:
                hash(value)
            except TypeError as exc:
                raise TemporalSplitError("group_id values must be scalar and hashable") from exc
            assigned = [name for name, mask in base_masks.items() if mask[position]]
            if assigned:
                partitions_by_group.setdefault(value, set()).update(assigned)
        crossing_groups = {
            value for value, partitions in partitions_by_group.items() if len(partitions) > 1
        }
        if crossing_groups:
            for position, value in enumerate(group_values):
                if not pd.isna(value) and value in crossing_groups:
                    group_purged[position] = True
            for mask in base_masks.values():
                mask[group_purged] = False

    assigned_any = np.zeros(len(frame), dtype=bool)
    for mask in base_masks.values():
        assigned_any |= mask
    excluded_mask = ~assigned_any
    slices = {name: frame.iloc[mask].copy() for name, mask in base_masks.items()}
    excluded = frame.iloc[excluded_mask].copy()
    statistics = {
        "total_rows": len(frame),
        "train_rows": len(slices["train"]),
        "validation_rows": len(slices["validation"]),
        "test_rows": len(slices["test"]),
        "excluded_rows": len(excluded),
        "group_purged_rows": int(group_purged.sum()),
    }
    return TemporalSplit(
        train=slices["train"],
        validation=slices["validation"],
        test=slices["test"],
        excluded=excluded,
        statistics=statistics,
    )


def fit_numeric_statistics(
    training_frame: pd.DataFrame,
    feature_columns: Sequence[str],
) -> dict[str, dict[str, float]]:
    """Fit mean and scale values using only the provided training rows."""
    if not feature_columns:
        raise ValueError("feature_columns must not be empty")
    if len(feature_columns) != len(set(feature_columns)):
        raise ValueError("feature_columns must be unique")
    missing = [column for column in feature_columns if column not in training_frame.columns]
    if missing:
        raise ValueError(f"training feature columns are missing: {missing}")

    statistics: dict[str, dict[str, float]] = {}
    for column in feature_columns:
        numeric = pd.to_numeric(training_frame[column], errors="coerce").to_numpy(dtype=float)
        finite = numeric[np.isfinite(numeric)]
        if finite.size == 0:
            raise ValueError(f"training feature {column!r} has no finite values")
        mean = float(finite.mean())
        scale = float(finite.std(ddof=0))
        if not math.isfinite(scale) or scale == 0.0:
            scale = 1.0
        statistics[column] = {"mean": mean, "scale": scale}
    return statistics


def apply_numeric_statistics(
    frame: pd.DataFrame,
    statistics: Mapping[str, Mapping[str, float]],
) -> pd.DataFrame:
    """Transform numeric columns with fixed statistics previously fitted on training rows."""
    transformed = frame.copy()
    for column, values in statistics.items():
        if column not in transformed.columns:
            raise ValueError(f"feature column is missing: {column}")
        mean = float(values["mean"])
        scale = float(values["scale"])
        if not math.isfinite(mean) or not math.isfinite(scale) or scale <= 0.0:
            raise ValueError(f"invalid preprocessing statistics for feature {column!r}")
        transformed[column] = (pd.to_numeric(transformed[column], errors="coerce") - mean) / scale
    return transformed
