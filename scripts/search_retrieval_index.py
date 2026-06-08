"""Search baseline RU/KZ FAISS retrieval indexes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search a baseline RU/KZ FAISS retrieval index.",
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
        help="Directory with FAISS indexes and metadata files.",
    )
    parser.add_argument(
        "--lang",
        choices=("ru", "kk"),
        required=True,
        help="Language index to search.",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Query text.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of results to return. Defaults to config retriever.top_k.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML mapping: {config_path}")

    return config


def require_supported_backend(config: dict[str, Any]) -> None:
    if config["retriever"]["vector_backend"] != "faiss":
        raise ValueError("Only FAISS vector backend is supported by this script.")


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


def load_index(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"FAISS index file does not exist: {path}")

    try:
        import faiss
    except ImportError as exc:
        raise RuntimeError("Searching FAISS indexes requires faiss.") from exc

    return faiss.read_index(str(path))


def encode_query(query: str, model_name: str, normalize_embeddings: bool) -> Any:
    try:
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Encoding queries requires numpy and sentence-transformers.",
        ) from exc

    model = SentenceTransformer(model_name)
    embedding = model.encode(
        [f"query: {query}"],
        convert_to_numpy=True,
        normalize_embeddings=normalize_embeddings,
        show_progress_bar=False,
    )
    return np.asarray(embedding, dtype="float32")


def search(index: Any, query_embedding: Any, top_k: int) -> list[tuple[int, float]]:
    scores, positions = index.search(query_embedding, top_k)
    results: list[tuple[int, float]] = []
    for position, score in zip(positions[0].tolist(), scores[0].tolist()):
        if position < 0:
            continue
        results.append((int(position), float(score)))
    return results


def print_results(
    language: str,
    query: str,
    results: list[tuple[int, float]],
    metadata: list[dict[str, Any]],
) -> None:
    print(f"[QUERY] lang={language} text={query}")
    print(f"[RESULTS] count={len(results)}")

    for rank, (position, score) in enumerate(results, start=1):
        if position >= len(metadata):
            raise IndexError(
                f"Index returned position={position}, but metadata has {len(metadata)} records.",
            )

        record = metadata[position]
        text = str(record.get("text", "")).replace("\n", " ").strip()
        print(f"\n#{rank} score={score:.6f} doc_id={record.get('doc_id')}")
        print(f"language={record.get('language')} source={record.get('source')}")
        print(text)


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    require_supported_backend(config)

    top_k = args.top_k if args.top_k is not None else int(config["retriever"]["top_k"])
    if top_k <= 0:
        raise ValueError("top-k must be positive.")

    index_path = args.index_dir / f"{args.lang}.index"
    metadata_path = args.index_dir / f"{args.lang}_metadata.jsonl"

    index = load_index(index_path)
    metadata = load_metadata(metadata_path)
    query_embedding = encode_query(
        query=args.query,
        model_name=config["retriever"]["embedding_model"],
        normalize_embeddings=bool(config["retriever"]["normalize_embeddings"]),
    )
    results = search(index=index, query_embedding=query_embedding, top_k=top_k)
    print_results(args.lang, args.query, results, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
