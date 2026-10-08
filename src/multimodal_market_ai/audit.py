"""Causality checks used across the project."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import pandas as pd


class CausalityError(ValueError):
    """Raised when an input contains information unavailable at decision time."""


@dataclass(frozen=True)
class CausalAuditReport:
    """Summary of the declared feature inputs checked for causal availability."""

    checked_features: tuple[str, ...]
    rows_checked: int


def assert_causal_alignment(decision_ts: pd.Series, context_ts: pd.Series) -> None:
    """Ensure every non-null context timestamp is <= its decision timestamp."""
    decision = pd.to_datetime(decision_ts, utc=True)
    context = pd.to_datetime(context_ts, utc=True)
    invalid = context.notna() & (context > decision)
    if invalid.any():
        first = int(invalid.to_numpy().nonzero()[0][0])
        raise CausalityError(
            f"future context detected at row {first}: "
            f"context={context.iloc[first]!s} decision={decision.iloc[first]!s}"
        )


def audit_causal_features(
    frame: pd.DataFrame,
    *,
    decision_ts_column: str,
    feature_columns: Sequence[str],
    allowed_features: Sequence[str],
    availability_columns: Mapping[str, str],
    forbidden_columns: Sequence[str] = (),
) -> CausalAuditReport:
    """Fail closed unless every selected feature is allowlisted and available by decision time."""
    if not isinstance(frame, pd.DataFrame):
        raise CausalityError("feature input must be a pandas DataFrame")
    if not feature_columns:
        raise CausalityError("feature allowlist selection must not be empty")

    selected = tuple(feature_columns)
    allowed = set(allowed_features)
    forbidden = set(forbidden_columns)
    if len(selected) != len(set(selected)):
        raise CausalityError("feature selection contains duplicate columns")
    if not allowed:
        raise CausalityError("an explicit feature allowlist is required")

    missing_features = [name for name in selected if name not in frame.columns]
    if missing_features:
        raise CausalityError(f"selected feature columns are missing: {missing_features}")
    outside_allowlist = [name for name in selected if name not in allowed]
    if outside_allowlist:
        raise CausalityError(f"selected features are outside the allowlist: {outside_allowlist}")
    forbidden_selected = [name for name in selected if name in forbidden]
    if forbidden_selected:
        raise CausalityError(f"forbidden columns cannot be selected as features: {forbidden_selected}")
    if decision_ts_column not in frame.columns:
        raise CausalityError(f"decision timestamp column is missing: {decision_ts_column}")

    missing_availability = [name for name in selected if name not in availability_columns]
    if missing_availability:
        raise CausalityError(
            f"availability timestamps are not declared for features: {missing_availability}"
        )
    unavailable_columns = [
        availability_columns[name]
        for name in selected
        if availability_columns[name] not in frame.columns
    ]
    if unavailable_columns:
        raise CausalityError(f"availability timestamp columns are missing: {unavailable_columns}")

    decision = pd.to_datetime(frame[decision_ts_column], utc=True, errors="coerce")
    if decision.isna().any():
        raise CausalityError("decision timestamps contain missing or invalid values")

    for feature in selected:
        available = pd.to_datetime(frame[availability_columns[feature]], utc=True, errors="coerce")
        invalid = available.isna() | (available > decision)
        if invalid.any():
            first = int(invalid.to_numpy().nonzero()[0][0])
            raise CausalityError(
                f"feature {feature!r} is unavailable at row {first}: "
                f"available={available.iloc[first]!s} decision={decision.iloc[first]!s}"
            )

    return CausalAuditReport(checked_features=selected, rows_checked=len(frame))
