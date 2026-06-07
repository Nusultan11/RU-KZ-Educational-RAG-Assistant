"""Smoke-level import checks for the architecture skeleton."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest import TestCase


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))


class SkeletonImportTests(TestCase):
    """Validate that package boundaries are importable."""

    def test_top_level_package_imports(self) -> None:
        module = importlib.import_module("rag_assistant")
        self.assertIsNotNone(module)

    def test_layer_packages_import(self) -> None:
        for package in (
            "rag_assistant.core",
            "rag_assistant.data",
            "rag_assistant.eda",
            "rag_assistant.preprocessing",
            "rag_assistant.indexing",
            "rag_assistant.retrieval",
            "rag_assistant.generation",
            "rag_assistant.evaluation",
            "rag_assistant.training",
            "rag_assistant.api",
            "rag_assistant.monitoring",
        ):
            with self.subTest(package=package):
                self.assertIsNotNone(importlib.import_module(package))

