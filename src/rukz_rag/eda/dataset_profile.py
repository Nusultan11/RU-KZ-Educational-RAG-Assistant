"""Dataset split profiling without preprocessing or data mutation."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from .text_stats import compute_text_statistics


class DatasetLike(Protocol):
    """Minimal Hugging Face Dataset interface required by the profiler."""

    column_names: Sequence[str]

    def __len__(self) -> int: ...

    def __getitem__(self, index: int) -> Mapping[str, Any]: ...


def profile_dataset_split(
    dataset: DatasetLike,
    split_name: str,
    sample_size: int,
    text_length_percentiles: Sequence[float],
    example_count: int = 3,
) -> dict[str, Any]:
    """Profile one dataset split using a deterministic head sample."""
    if sample_size <= 0:
        raise ValueError("sample_size must be positive.")
    if example_count < 0:
        raise ValueError("example_count must not be negative.")

    total_rows = len(dataset)
    analyzed_rows = min(total_rows, sample_size)
    records = [dict(dataset[index]) for index in range(analyzed_rows)]
    columns = list(dataset.column_names) if dataset.column_names else _record_columns(records)

    return {
        "split": split_name,
        "columns": columns,
        "total_rows": total_rows,
        "analyzed_rows": analyzed_rows,
        "sample_strategy": "head",
        "empty_values": _empty_value_counts(records, columns),
        "duplicate_rows": _duplicate_row_count(records),
        "duplicate_scope": "analyzed_rows",
        "examples": records[:example_count],
        "text_statistics": compute_text_statistics(records, text_length_percentiles),
    }


def _record_columns(records: Sequence[Mapping[str, Any]]) -> list[str]:
    return sorted({column for record in records for column in record})


def _empty_value_counts(
    records: Sequence[Mapping[str, Any]],
    columns: Sequence[str],
) -> dict[str, int]:
    return {
        column: sum(1 for record in records if _is_empty(record.get(column))) for column in columns
    }


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def _duplicate_row_count(records: Sequence[Mapping[str, Any]]) -> int:
    canonical_rows = [
        json.dumps(record, ensure_ascii=False, sort_keys=True, default=str) for record in records
    ]
    return len(canonical_rows) - len(set(canonical_rows))
