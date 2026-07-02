"""Writers for machine-readable and human-readable EDA reports."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def dataset_report_slug(dataset_name: str) -> str:
    """Build a stable report filename from a Hugging Face dataset repository name."""
    repository_name = dataset_name.rsplit("/", maxsplit=1)[-1]
    slug = re.sub(r"[^a-z0-9]+", "_", repository_name.casefold()).strip("_")
    if not slug:
        raise ValueError(f"Cannot create report slug for dataset: {dataset_name}")
    return slug


def write_dataset_report(
    output_dir: Path,
    dataset_name: str,
    report: dict[str, Any],
) -> Path:
    """Write one UTF-8 JSON report and return its path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{dataset_report_slug(dataset_name)}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    return report_path


def write_summary(output_dir: Path, reports: list[dict[str, Any]]) -> Path:
    """Write a compact Markdown summary for all configured datasets."""
    output_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# EDA Summary",
        "",
        "| Dataset | Status | Configs | Splits | Rows |",
        "| --- | --- | ---: | ---: | ---: |",
    ]

    for report in reports:
        configurations = report.get("configurations", [])
        split_reports = [
            split for configuration in configurations for split in configuration.get("splits", [])
        ]
        total_rows = sum(int(split.get("total_rows", 0)) for split in split_reports)
        lines.append(
            "| {dataset} | {status} | {configs} | {splits} | {rows} |".format(
                dataset=report.get("dataset", "unknown"),
                status=report.get("status", "unknown"),
                configs=len(configurations),
                splits=len(split_reports),
                rows=total_rows,
            ),
        )

    summary_path = output_dir / "summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path
