"""Reproducible dataset profiling for the Stage 2 EDA foundation."""

from .dataset_profile import profile_dataset_split
from .report import dataset_report_slug, write_dataset_report, write_summary
from .text_stats import compute_text_statistics

__all__ = [
    "compute_text_statistics",
    "dataset_report_slug",
    "profile_dataset_split",
    "write_dataset_report",
    "write_summary",
]
