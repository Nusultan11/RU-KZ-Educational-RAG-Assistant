"""Evaluate KZ baseline retrieval with anchor-positive pairs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import yaml


@dataclass(frozen=True)
class EvaluationRecord:
    """A single KZ retrieval evaluation example."""

    query: str
    positive: str
    expected_position: int


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate KZ retrieval with anchor-positive pairs.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/retriever_baseline.yaml"),
        help="Path to retriever baseline YAML config.",
    )
    parser.add_argument(
        "--index-dir",
        type=Path,
        default=Path("indexes/baseline"),
        help="Directory with kk.index and kk_metadata.jsonl.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw/hf"),
        help="Directory with local Hugging Face dataset snapshots.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Maximum k for Recall@k and MRR@k.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Query embedding batch size.",
    )
    parser.add_argument(
        "--max-queries",
        type=int,
        default=None,
        help="Optional cap for smoke-testing before full evaluation.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML mapping: {config_path}")

    return config


def local_dataset_dir(data_dir: Path, dataset_name: str) -> Path:
    return data_dir / dataset_name.replace("/", "__")


def find_required_file(dataset_dir: Path, file_name: str) -> Path:
    matches = sorted(dataset_dir.rglob(file_name))
    if not matches:
        raise FileNotFoundError(f"File {file_name} was not found under {dataset_dir}")
    return matches[0]


def require_text(record: dict[str, Any], column: str, source_path: Path) -> str:
    value = record.get(column)
    if value is None:
        raise ValueError(f"Missing required column {column!r} in {source_path}")

    text = str(value).strip()
    if not text:
        raise ValueError(f"Empty text in column {column!r} from {source_path}")

    return text


def read_csv_records(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def load_kz_evaluation_records(
    config: dict[str, Any],
    data_dir: Path,
    max_queries: int | None,
) -> list[EvaluationRecord]:
    dataset_dir = local_dataset_dir(data_dir, config["source"])
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Local dataset snapshot does not exist: {dataset_dir}")

    path = find_required_file(dataset_dir, config["file"])
    records: list[EvaluationRecord] = []

    for row_number, row in enumerate(read_csv_records(path)):
        query = require_text(row, config["query_column"], path)
        positive = require_text(row, config["text_column"], path)
        records.append(
            EvaluationRecord(
                query=query,
                positive=positive,
                expected_position=row_number,
            ),
        )
        if max_queries is not None and len(records) >= max_queries:
            break

    if not records:
        raise ValueError(f"No KZ evaluation records loaded from {path}")

    return records


def load_metadata(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Metadata file does not exist: {path}")

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"Metadata record is not an object: {path}:{line_number}")
            records.append(record)

    if not records:
        raise ValueError(f"Metadata file is empty: {path}")

    return records


def validate_metadata_alignment(
    records: list[EvaluationRecord],
    metadata: list[dict[str, Any]],
) -> None:
    if len(records) > len(metadata):
        raise ValueError(
            f"Evaluation records exceed metadata size: records={len(records)} metadata={len(metadata)}",
        )

    for record in records:
        metadata_record = metadata[record.expected_position]
        metadata_text = str(metadata_record.get("text", "")).strip()
        if metadata_text != record.positive:
            raise ValueError(
                "KZ metadata is not aligned with evaluation records at "
                f"position={record.expected_position}",
            )


def load_index(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"FAISS index file does not exist: {path}")

    try:
        import faiss
    except ImportError as exc:
        raise RuntimeError("Evaluating retrieval requires faiss.") from exc

    return faiss.read_index(str(path))


def load_embedding_model(model_name: str) -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("Evaluating retrieval requires sentence-transformers.") from exc

    return SentenceTransformer(model_name)


def encode_queries(
    model: Any,
    queries: list[str],
    batch_size: int,
    normalize_embeddings: bool,
) -> Any:
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("Evaluating retrieval requires numpy.") from exc

    formatted_queries = [f"query: {query}" for query in queries]
    embeddings = model.encode(
        formatted_queries,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=normalize_embeddings,
        show_progress_bar=True,
    )
    return np.asarray(embeddings, dtype="float32")


def reciprocal_rank(positions: list[int], expected_position: int, top_k: int) -> float:
    for rank, position in enumerate(positions[:top_k], start=1):
        if position == expected_position:
            return 1.0 / rank
    return 0.0


def compute_metrics(
    records: list[EvaluationRecord],
    retrieved_positions: list[list[int]],
) -> dict[str, float]:
    if len(records) != len(retrieved_positions):
        raise ValueError("Record count and retrieval result count do not match.")

    total = len(records)
    recall_at_1 = 0
    recall_at_5 = 0
    reciprocal_ranks_at_5: list[float] = []

    for record, positions in zip(records, retrieved_positions):
        if record.expected_position in positions[:1]:
            recall_at_1 += 1
        if record.expected_position in positions[:5]:
            recall_at_5 += 1
        reciprocal_ranks_at_5.append(
            reciprocal_rank(positions, record.expected_position, top_k=5),
        )

    return {
        "queries": float(total),
        "recall@1": recall_at_1 / total,
        "recall@5": recall_at_5 / total,
        "mrr@5": sum(reciprocal_ranks_at_5) / total,
    }


def evaluate(
    index: Any,
    records: list[EvaluationRecord],
    embeddings: Any,
    top_k: int,
) -> dict[str, float]:
    _, positions = index.search(embeddings, top_k)
    retrieved_positions = [
        [int(position) for position in row.tolist() if position >= 0]
        for row in positions
    ]
    return compute_metrics(records, retrieved_positions)


def print_metrics(metrics: dict[str, float]) -> None:
    print("[KZ RETRIEVAL EVALUATION]")
    print(f"queries={int(metrics['queries'])}")
    print(f"recall@1={metrics['recall@1']:.6f}")
    print(f"recall@5={metrics['recall@5']:.6f}")
    print(f"mrr@5={metrics['mrr@5']:.6f}")


def main() -> int:
    configure_stdout()
    args = parse_args()
    if args.top_k < 5:
        raise ValueError("--top-k must be at least 5 for Recall@5 and MRR@5.")
    if args.batch_size <= 0:
        raise ValueError("--batch-size must be positive.")
    if args.max_queries is not None and args.max_queries <= 0:
        raise ValueError("--max-queries must be positive when provided.")

    config = load_config(args.config)
    if config["retriever"]["vector_backend"] != "faiss":
        raise ValueError("Only FAISS vector backend is supported.")

    records = load_kz_evaluation_records(
        config=config["data"]["kazakh"],
        data_dir=args.data_dir,
        max_queries=args.max_queries,
    )
    metadata = load_metadata(args.index_dir / "kk_metadata.jsonl")
    validate_metadata_alignment(records, metadata)

    index = load_index(args.index_dir / "kk.index")
    model = load_embedding_model(config["retriever"]["embedding_model"])
    embeddings = encode_queries(
        model=model,
        queries=[record.query for record in records],
        batch_size=args.batch_size,
        normalize_embeddings=bool(config["retriever"]["normalize_embeddings"]),
    )
    metrics = evaluate(index, records, embeddings, top_k=args.top_k)
    print_metrics(metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
