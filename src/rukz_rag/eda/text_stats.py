"""Text-length statistics for sampled dataset records."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import pandas as pd  # type: ignore[import-untyped]


def compute_text_statistics(
    records: Sequence[Mapping[str, Any]],
    percentiles: Sequence[float],
) -> dict[str, dict[str, Any]]:
    """Compute character-length statistics for columns containing strings."""
    _validate_percentiles(percentiles)
    text_columns = sorted(
        {
            column
            for record in records
            for column, value in record.items()
            if isinstance(value, str)
        },
    )

    statistics: dict[str, dict[str, Any]] = {}
    for column in text_columns:
        lengths = [
            len(value) for record in records if isinstance((value := record.get(column)), str)
        ]
        if not lengths:
            continue

        series = pd.Series(lengths, dtype="int64")
        statistics[column] = {
            "count": int(series.count()),
            "min": int(series.min()),
            "max": int(series.max()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "percentiles": {
                f"p{_percentile_label(percentile)}": float(series.quantile(percentile / 100))
                for percentile in percentiles
            },
        }

    return statistics


def _validate_percentiles(percentiles: Sequence[float]) -> None:
    if not percentiles:
        raise ValueError("At least one text-length percentile is required.")
    invalid = [value for value in percentiles if value < 0 or value > 100]
    if invalid:
        raise ValueError(f"Percentiles must be between 0 and 100: {invalid}")


def _percentile_label(percentile: float) -> str:
    numeric_percentile = float(percentile)
    if numeric_percentile.is_integer():
        return str(int(numeric_percentile))
    return str(numeric_percentile).replace(".", "_")
