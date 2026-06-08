"""Download configured Hugging Face datasets into a local raw data directory."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from huggingface_hub import snapshot_download


DATASET_NAME_PATTERN = re.compile(r'^\s*name:\s*["\']?([^"\']+)["\']?\s*$')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Hugging Face datasets listed in configs/datasets.yaml.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/datasets.yaml"),
        help="Path to datasets YAML config.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/hf"),
        help="Directory where dataset snapshots will be stored.",
    )
    return parser.parse_args()


def read_dataset_names(config_path: Path) -> list[str]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    dataset_names: list[str] = []
    for line in config_path.read_text(encoding="utf-8").splitlines():
        match = DATASET_NAME_PATTERN.match(line)
        if match:
            dataset_names.append(match.group(1))

    if not dataset_names:
        raise ValueError(f"No dataset names found in config: {config_path}")

    return dataset_names


def local_dataset_dir(output_dir: Path, dataset_name: str) -> Path:
    return output_dir / dataset_name.replace("/", "__")


def download_dataset(dataset_name: str, output_dir: Path) -> Path:
    target_dir = local_dataset_dir(output_dir, dataset_name)
    print(f"[START] dataset={dataset_name}")
    print(f"[PATH]  local_dir={target_dir}")

    snapshot_download(
        repo_id=dataset_name,
        repo_type="dataset",
        local_dir=target_dir,
        local_dir_use_symlinks=False,
    )

    print(f"[DONE]  dataset={dataset_name}")
    return target_dir


def main() -> int:
    args = parse_args()
    dataset_names = read_dataset_names(args.config)

    print(f"[CONFIG] {args.config}")
    print(f"[OUTPUT] {args.output_dir}")
    print(f"[COUNT]  datasets={len(dataset_names)}")

    for dataset_name in dataset_names:
        download_dataset(dataset_name, args.output_dir)

    print("[SUCCESS] all datasets downloaded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
