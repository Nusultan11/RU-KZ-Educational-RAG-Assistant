"""Build baseline RU/KZ FAISS retrieval indexes from local dataset snapshots."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

import yaml


LOGGER = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = {".csv", ".json", ".jsonl", ".parquet"}


@dataclass(frozen=True)
class Document:
    """A text document that will be embedded and stored in metadata."""

    doc_id: str
    language: str
    text: str
    source: str
    extra: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build baseline RU/KZ FAISS retrieval indexes.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/retriever_baseline.yaml"),
        help="Path to retriever baseline YAML config.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("indexes/baseline"),
        help="Directory where FAISS indexes and metadata files will be saved.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw/hf"),
        help="Directory with local Hugging Face dataset snapshots.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Embedding batch size.",
    )
    return parser.parse_args()


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML mapping: {config_path}")

    return config


def local_dataset_dir(data_dir: Path, dataset_name: str) -> Path:
    return data_dir / dataset_name.replace("/", "__")


def require_dataset_dir(data_dir: Path, dataset_name: str) -> Path:
    dataset_dir = local_dataset_dir(data_dir, dataset_name)
    if not dataset_dir.exists():
        raise FileNotFoundError(
            f"Local dataset snapshot does not exist: {dataset_dir}. "
            "Download datasets before building indexes.",
        )
    return dataset_dir


def read_csv_records(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def read_jsonl_records(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"JSONL record is not an object: {path}:{line_number}")
            yield record


def read_json_records(path: Path) -> Iterator[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        for record in payload:
            if not isinstance(record, dict):
                raise ValueError(f"JSON list item is not an object: {path}")
            yield record
        return

    if isinstance(payload, dict):
        rows = payload.get("data")
        if isinstance(rows, list):
            for record in rows:
                if not isinstance(record, dict):
                    raise ValueError(f"JSON data item is not an object: {path}")
                yield record
            return
        yield payload
        return

    raise ValueError(f"Unsupported JSON payload: {path}")


def read_parquet_records(path: Path) -> Iterator[dict[str, Any]]:
    try:
        import pyarrow.parquet as parquet
    except ImportError as exc:
        raise RuntimeError("Reading parquet files requires pyarrow.") from exc

    table = parquet.read_table(path)
    for record in table.to_pylist():
        if not isinstance(record, dict):
            raise ValueError(f"Parquet row is not an object: {path}")
        yield record


def read_records(path: Path) -> Iterator[dict[str, Any]]:
    readers = {
        ".csv": read_csv_records,
        ".jsonl": read_jsonl_records,
        ".json": read_json_records,
        ".parquet": read_parquet_records,
    }
    reader = readers.get(path.suffix.lower())
    if reader is None:
        raise ValueError(f"Unsupported dataset file extension: {path}")
    yield from reader(path)


def find_required_file(dataset_dir: Path, file_name: str) -> Path:
    matches = sorted(dataset_dir.rglob(file_name))
    if not matches:
        raise FileNotFoundError(f"File {file_name} was not found under {dataset_dir}")
    if len(matches) > 1:
        LOGGER.warning("Multiple matches for %s, using %s", file_name, matches[0])
    return matches[0]


def find_split_files(dataset_dir: Path, config_name: str, split_name: str) -> list[Path]:
    candidates = [
        path
        for path in dataset_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if not candidates:
        raise FileNotFoundError(f"No supported dataset files found under {dataset_dir}")

    config_lower = config_name.lower()
    split_lower = split_name.lower()

    matched = [
        path
        for path in candidates
        if config_lower in str(path).lower() and split_lower in path.name.lower()
    ]
    if matched:
        return sorted(matched)

    config_matched = [
        path for path in candidates if config_lower in str(path).lower()
    ]
    if config_matched:
        LOGGER.warning(
            "No split-specific files found for config=%s split=%s; using config files.",
            config_name,
            split_name,
        )
        return sorted(config_matched)

    raise FileNotFoundError(
        f"No files matched config={config_name!r} split={split_name!r} under {dataset_dir}",
    )


def require_text(record: dict[str, Any], column: str, source_path: Path) -> str:
    value = record.get(column)
    if value is None:
        raise ValueError(f"Missing required column {column!r} in {source_path}")

    text = str(value).strip()
    if not text:
        raise ValueError(f"Empty text in column {column!r} from {source_path}")

    return text


def load_russian_documents(config: dict[str, Any], data_dir: Path) -> list[Document]:
    dataset_dir = require_dataset_dir(data_dir, config["source"])
    files = find_split_files(dataset_dir, config["config"], config["split"])
    documents: list[Document] = []

    for path in files:
        for row_number, record in enumerate(read_records(path)):
            text = require_text(record, config["text_column"], path)
            raw_id = record.get(config["id_column"], row_number)
            documents.append(
                Document(
                    doc_id=str(raw_id),
                    language="ru",
                    text=text,
                    source=config["source"],
                    extra={"file": str(path), "row": row_number},
                ),
            )

    return documents


def load_kazakh_documents(config: dict[str, Any], data_dir: Path) -> list[Document]:
    dataset_dir = require_dataset_dir(data_dir, config["source"])
    path = find_required_file(dataset_dir, config["file"])
    documents: list[Document] = []

    for row_number, record in enumerate(read_records(path)):
        text = require_text(record, config["text_column"], path)
        extra = {
            "query": record.get(config["query_column"]),
            "negative": record.get(config["negative_column"]),
            "source_column": record.get(config["source_column"]),
            "file": str(path),
            "row": row_number,
        }
        documents.append(
            Document(
                doc_id=f"kk-{row_number}",
                language="kk",
                text=text,
                source=config["source"],
                extra=extra,
            ),
        )

    return documents


def format_passages(documents: Iterable[Document]) -> list[str]:
    return [f"passage: {document.text}" for document in documents]


def build_faiss_index(
    documents: list[Document],
    model_name: str,
    normalize_embeddings: bool,
    batch_size: int,
) -> Any:
    if not documents:
        raise ValueError("Cannot build FAISS index from zero documents.")

    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Building indexes requires faiss, numpy and sentence-transformers.",
        ) from exc

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        format_passages(documents),
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=normalize_embeddings,
        show_progress_bar=True,
    )
    embeddings = np.asarray(embeddings, dtype="float32")

    if embeddings.ndim != 2:
        raise ValueError(f"Expected 2D embeddings, got shape={embeddings.shape}")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) if normalize_embeddings else faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def write_metadata(path: Path, documents: list[Document]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for position, document in enumerate(documents):
            payload = {
                "position": position,
                "doc_id": document.doc_id,
                "language": document.language,
                "text": document.text,
                "source": document.source,
                "extra": document.extra,
            }
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def save_index(path: Path, index: Any) -> None:
    try:
        import faiss
    except ImportError as exc:
        raise RuntimeError("Saving FAISS indexes requires faiss.") from exc

    faiss.write_index(index, str(path))


def build_language_index(
    language: str,
    documents: list[Document],
    config: dict[str, Any],
    output_dir: Path,
    batch_size: int,
) -> None:
    LOGGER.info("Building %s index from %d documents", language, len(documents))
    index = build_faiss_index(
        documents=documents,
        model_name=config["retriever"]["embedding_model"],
        normalize_embeddings=bool(config["retriever"]["normalize_embeddings"]),
        batch_size=batch_size,
    )
    save_index(output_dir / f"{language}.index", index)
    write_metadata(output_dir / f"{language}_metadata.jsonl", documents)
    LOGGER.info("Saved %s index and metadata to %s", language, output_dir)


def main() -> int:
    setup_logging()
    args = parse_args()
    config = load_config(args.config)

    if config["retriever"]["vector_backend"] != "faiss":
        raise ValueError("Only FAISS vector backend is supported by this baseline script.")
    if config["chunking"]["enabled"]:
        raise ValueError("Chunking must be disabled for this baseline script.")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    ru_documents = load_russian_documents(config["data"]["russian"], args.data_dir)
    kk_documents = load_kazakh_documents(config["data"]["kazakh"], args.data_dir)

    build_language_index("ru", ru_documents, config, args.output_dir, args.batch_size)
    build_language_index("kk", kk_documents, config, args.output_dir, args.batch_size)

    LOGGER.info("Baseline retrieval indexes built successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
