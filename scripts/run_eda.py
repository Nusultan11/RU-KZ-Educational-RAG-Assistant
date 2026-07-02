"""Run reproducible Stage 2 EDA for configured Hugging Face datasets."""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from datasets import Dataset, DatasetDict, get_dataset_config_names, load_dataset  # type: ignore[import-untyped]
from tqdm import tqdm  # type: ignore[import-untyped]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from rukz_rag.eda import (  # type: ignore[import-untyped]  # noqa: E402
    profile_dataset_split,
    write_dataset_report,
    write_summary,
)

LOGGER = logging.getLogger("rukz_rag.eda")


@dataclass(frozen=True)
class DatasetLoadConfiguration:
    """Explicit loader for repositories containing incompatible file schemas."""

    name: str
    builder: str
    data_files: dict[str, str]


@dataclass(frozen=True)
class DatasetSpec:
    """One configured dataset and its project role."""

    name: str
    role: str
    load_configurations: tuple[DatasetLoadConfiguration, ...] = ()


@dataclass(frozen=True)
class EDASettings:
    """Validated Stage 2 EDA settings."""

    sample_size: int
    text_length_percentiles: tuple[float, ...]
    output_dir: Path
    language_detection_enabled: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile configured Hugging Face datasets and write Stage 2 EDA reports.",
    )
    parser.add_argument(
        "--datasets-config",
        type=Path,
        default=Path("configs/datasets.yaml"),
        help="Path to the dataset inventory YAML file.",
    )
    parser.add_argument(
        "--eda-config",
        type=Path,
        default=Path("configs/eda.yaml"),
        help="Path to the EDA settings YAML file.",
    )
    return parser.parse_args()


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file does not exist: {path}")

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Config must contain a YAML mapping: {path}")
    return loaded


def read_dataset_specs(path: Path) -> list[DatasetSpec]:
    config = load_yaml_mapping(path)
    datasets = config.get("datasets")
    if not isinstance(datasets, dict):
        raise ValueError("datasets config must contain a 'datasets' mapping.")

    specs: list[DatasetSpec] = []
    _collect_dataset_specs(datasets, specs)
    if not specs:
        raise ValueError(f"No dataset entries found in config: {path}")
    return specs


def _collect_dataset_specs(node: Any, specs: list[DatasetSpec]) -> None:
    if not isinstance(node, dict):
        return

    name = node.get("name")
    if isinstance(name, str) and name.strip():
        role = node.get("role", "unspecified")
        specs.append(
            DatasetSpec(
                name=name.strip(),
                role=str(role),
                load_configurations=_parse_load_configurations(
                    node.get("load_configurations", []),
                ),
            ),
        )
        return

    for value in node.values():
        _collect_dataset_specs(value, specs)


def _parse_load_configurations(value: Any) -> tuple[DatasetLoadConfiguration, ...]:
    if value in (None, []):
        return ()
    if not isinstance(value, list):
        raise ValueError("load_configurations must be a list.")

    configurations: list[DatasetLoadConfiguration] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Each load configuration must be a mapping.")
        name = str(item.get("name", "")).strip()
        builder = str(item.get("builder", "")).strip()
        raw_data_files = item.get("data_files")
        if not name or not builder or not isinstance(raw_data_files, dict):
            raise ValueError(
                "Each load configuration requires name, builder, and data_files mapping.",
            )
        data_files = {
            str(split): str(file_name)
            for split, file_name in raw_data_files.items()
            if str(split).strip() and str(file_name).strip()
        }
        if not data_files:
            raise ValueError(f"Load configuration '{name}' has no data files.")
        configurations.append(
            DatasetLoadConfiguration(name=name, builder=builder, data_files=data_files),
        )

    return tuple(configurations)


def read_eda_settings(path: Path) -> EDASettings:
    config = load_yaml_mapping(path)
    eda = config.get("eda")
    if not isinstance(eda, dict):
        raise ValueError("EDA config must contain an 'eda' mapping.")

    sample_size = int(eda.get("sample_size", 0))
    if sample_size <= 0:
        raise ValueError("eda.sample_size must be positive.")

    raw_percentiles = eda.get("text_length_percentiles")
    if not isinstance(raw_percentiles, list) or not raw_percentiles:
        raise ValueError("eda.text_length_percentiles must be a non-empty list.")
    percentiles = tuple(float(value) for value in raw_percentiles)

    output_dir = Path(str(eda.get("output_dir", "reports/eda")))
    language_detection = eda.get("language_detection", {})
    if not isinstance(language_detection, dict):
        raise ValueError("eda.language_detection must be a mapping.")

    return EDASettings(
        sample_size=sample_size,
        text_length_percentiles=percentiles,
        output_dir=output_dir,
        language_detection_enabled=bool(language_detection.get("enabled", False)),
    )


def profile_dataset(spec: DatasetSpec, settings: EDASettings) -> dict[str, Any]:
    """Load and profile all configurations and splits for one dataset repository."""
    report: dict[str, Any] = {
        "dataset": spec.name,
        "role": spec.role,
        "status": "success",
        "sample_size": settings.sample_size,
        "text_length_percentiles": list(settings.text_length_percentiles),
        "language_detection": {
            "enabled": settings.language_detection_enabled,
            "status": "disabled" if not settings.language_detection_enabled else "not_implemented",
        },
        "configurations": [],
    }

    configurations = _dataset_configurations(spec)
    successful_configurations = 0
    for configuration in configurations:
        config_report: dict[str, Any] = {
            "name": configuration.name,
            "status": "success",
            "splits": [],
        }
        try:
            loaded = _load_dataset_configuration(spec, configuration)
            splits = _profile_loaded_dataset(loaded, settings)
            config_report["splits"] = splits
            successful_configurations += 1
        except Exception as exc:  # Dataset repositories expose heterogeneous loaders.
            LOGGER.exception(
                "EDA failed for dataset=%s configuration=%s",
                spec.name,
                configuration.name,
            )
            config_report["status"] = "error"
            config_report["error"] = f"{type(exc).__name__}: {exc}"
        report["configurations"].append(config_report)

    if successful_configurations == 0:
        report["status"] = "failed"
    elif successful_configurations < len(configurations):
        report["status"] = "partial"

    return report


def _dataset_configurations(spec: DatasetSpec) -> tuple[DatasetLoadConfiguration, ...]:
    if spec.load_configurations:
        return spec.load_configurations

    config_names = get_dataset_config_names(spec.name)
    if not config_names:
        config_names = ["default"]
    return tuple(
        DatasetLoadConfiguration(name=config_name, builder="", data_files={})
        for config_name in config_names
    )


def _load_dataset_configuration(
    spec: DatasetSpec,
    configuration: DatasetLoadConfiguration,
) -> Dataset | DatasetDict:
    if configuration.data_files:
        remote_files = {
            split: f"hf://datasets/{spec.name}/{file_name}"
            for split, file_name in configuration.data_files.items()
        }
        return load_dataset(configuration.builder, data_files=remote_files)

    if configuration.name == "default":
        return load_dataset(spec.name)
    return load_dataset(spec.name, configuration.name)


def _profile_loaded_dataset(
    loaded: Dataset | DatasetDict,
    settings: EDASettings,
) -> list[dict[str, Any]]:
    if isinstance(loaded, Dataset):
        split_name = str(loaded.split) if loaded.split is not None else "unspecified"
        return [
            profile_dataset_split(
                dataset=loaded,
                split_name=split_name,
                sample_size=settings.sample_size,
                text_length_percentiles=settings.text_length_percentiles,
            ),
        ]

    return [
        profile_dataset_split(
            dataset=dataset,
            split_name=str(split_name),
            sample_size=settings.sample_size,
            text_length_percentiles=settings.text_length_percentiles,
        )
        for split_name, dataset in loaded.items()
    ]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def main() -> int:
    configure_logging()
    args = parse_args()
    specs = read_dataset_specs(args.datasets_config)
    settings = read_eda_settings(args.eda_config)

    LOGGER.info("Starting EDA for %d configured datasets", len(specs))
    reports: list[dict[str, Any]] = []
    for spec in tqdm(specs, desc="Datasets", unit="dataset"):
        LOGGER.info("Profiling dataset=%s role=%s", spec.name, spec.role)
        report = profile_dataset(spec, settings)
        report_path = write_dataset_report(settings.output_dir, spec.name, report)
        LOGGER.info("Saved report=%s status=%s", report_path, report["status"])
        reports.append(report)

    summary_path = write_summary(settings.output_dir, reports)
    LOGGER.info("Saved summary=%s", summary_path)

    failed = [report["dataset"] for report in reports if report["status"] != "success"]
    if failed:
        LOGGER.error("EDA completed with failed datasets: %s", ", ".join(failed))
        return 1

    LOGGER.info("EDA completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
