"""Run the baseline end-to-end RAG pipeline locally."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from rag.context_builder import ContextBuilder, RetrievedDocument
from rag.generator import TransformersGenerator
from rag.prompt_builder import PromptBuilder


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run query -> retrieval -> context -> prompt -> generation.",
    )
    parser.add_argument("--query", required=True, help="User question.")
    parser.add_argument(
        "--lang",
        choices=("ru", "kk"),
        required=True,
        help="Language index to search.",
    )
    parser.add_argument(
        "--index-dir",
        type=Path,
        default=Path("indexes/baseline"),
        help="Directory with FAISS index and metadata files.",
    )
    parser.add_argument(
        "--retriever-config",
        type=Path,
        default=Path("configs/retriever_baseline.yaml"),
        help="Path to retriever YAML config.",
    )
    parser.add_argument(
        "--context-config",
        type=Path,
        default=Path("configs/rag_context.yaml"),
        help="Path to context builder YAML config.",
    )
    parser.add_argument(
        "--prompt-config",
        type=Path,
        default=Path("configs/rag_prompt.yaml"),
        help="Path to prompt builder YAML config.",
    )
    parser.add_argument(
        "--generator-config",
        type=Path,
        default=Path("configs/rag_generator.yaml"),
        help="Path to generator YAML config.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of documents to retrieve. Defaults to retriever config.",
    )
    parser.add_argument(
        "--deduplicate-results",
        choices=("true", "false"),
        default="true",
        help="Deduplicate retrieved documents by text. Defaults to true.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML mapping: {config_path}")

    return config


def require_faiss_backend(config: dict[str, Any]) -> None:
    backend = config["retriever"]["vector_backend"]
    if backend != "faiss":
        raise ValueError(f"Only FAISS vector backend is supported, got: {backend}")


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
        raise RuntimeError("Running RAG over FAISS indexes requires faiss.") from exc

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


def normalize_text_for_deduplication(text: str) -> str:
    return " ".join(text.split()).casefold()


def deduplicate_results(
    results: list[tuple[int, float]],
    metadata: list[dict[str, Any]],
) -> list[tuple[int, float]]:
    seen_texts: set[str] = set()
    deduplicated: list[tuple[int, float]] = []

    for position, score in results:
        if position >= len(metadata):
            raise IndexError(
                f"Index returned position={position}, but metadata has {len(metadata)} records.",
            )

        text = str(metadata[position].get("text", "")).strip()
        dedup_key = normalize_text_for_deduplication(text)
        if dedup_key in seen_texts:
            continue

        seen_texts.add(dedup_key)
        deduplicated.append((position, score))

    return deduplicated


def build_retrieved_documents(
    language: str,
    results: list[tuple[int, float]],
    metadata: list[dict[str, Any]],
) -> list[RetrievedDocument]:
    documents: list[RetrievedDocument] = []
    for position, score in results:
        if position >= len(metadata):
            raise IndexError(
                f"Index returned position={position}, but metadata has {len(metadata)} records.",
            )

        record = metadata[position]
        text = str(record.get("text", "")).strip()
        if not text:
            continue

        documents.append(
            RetrievedDocument(
                doc_id=str(record.get("doc_id", position)),
                text=text,
                score=score,
                source=str(record.get("source", "unknown")),
                language=str(record.get("language", language)),
                metadata={key: value for key, value in record.items() if key != "text"},
            ),
        )

    if not documents:
        raise ValueError("Retrieval returned no usable documents.")

    return documents


def create_context_builder(config: dict[str, Any]) -> ContextBuilder:
    context_config = config["context_builder"]
    return ContextBuilder(max_context_chars=int(context_config["max_context_chars"]))


def create_prompt_builder(config: dict[str, Any]) -> PromptBuilder:
    prompt_config = config["prompt_builder"]
    return PromptBuilder(
        instruction=str(prompt_config["instruction"]),
        answer_language_policy=str(prompt_config["answer_language_policy"]),
        require_sources=bool(prompt_config["require_sources"]),
    )


def create_generator(config: dict[str, Any]) -> TransformersGenerator:
    generator_config = config["generator"]
    backend = generator_config["backend"]
    if backend != "transformers_pipeline":
        raise ValueError(f"Only transformers_pipeline backend is supported, got: {backend}")

    return TransformersGenerator(
        model_name=str(generator_config["model_name"]),
        max_new_tokens=int(generator_config["max_new_tokens"]),
        temperature=float(generator_config["temperature"]),
        do_sample=bool(generator_config["do_sample"]),
        device_map=generator_config.get("device_map"),
        torch_dtype=generator_config.get("torch_dtype"),
    )


def print_run_summary(
    language: str,
    query: str,
    documents: list[RetrievedDocument],
    answer_text: str,
) -> None:
    print(f"[QUERY] lang={language} text={query}")
    print(f"[RETRIEVED] count={len(documents)}")
    for rank, document in enumerate(documents, start=1):
        preview = " ".join(document.text.split())[:180]
        print(
            f"[SOURCE {rank}] score={document.score:.6f} "
            f"doc_id={document.doc_id} source={document.source}",
        )
        print(preview)

    print("\n[ANSWER]")
    print(answer_text)


def main() -> int:
    configure_stdout()
    args = parse_args()

    retriever_config = load_config(args.retriever_config)
    context_config = load_config(args.context_config)
    prompt_config = load_config(args.prompt_config)
    generator_config = load_config(args.generator_config)
    require_faiss_backend(retriever_config)

    top_k = args.top_k if args.top_k is not None else int(retriever_config["retriever"]["top_k"])
    if top_k <= 0:
        raise ValueError("top-k must be positive.")

    index_path = args.index_dir / f"{args.lang}.index"
    metadata_path = args.index_dir / f"{args.lang}_metadata.jsonl"
    index = load_index(index_path)
    metadata = load_metadata(metadata_path)

    query_embedding = encode_query(
        query=args.query,
        model_name=str(retriever_config["retriever"]["embedding_model"]),
        normalize_embeddings=bool(retriever_config["retriever"]["normalize_embeddings"]),
    )

    deduplicate_results_enabled = args.deduplicate_results == "true"
    search_k = top_k * 3 if deduplicate_results_enabled else top_k
    raw_results = search(index=index, query_embedding=query_embedding, top_k=search_k)
    if deduplicate_results_enabled:
        raw_results = deduplicate_results(raw_results, metadata)

    documents = build_retrieved_documents(
        language=args.lang,
        results=raw_results[:top_k],
        metadata=metadata,
    )

    context = create_context_builder(context_config).build(
        question=args.query,
        documents=documents,
    )
    prompt = create_prompt_builder(prompt_config).build(context=context)
    answer = create_generator(generator_config).generate(prompt)

    print_run_summary(
        language=args.lang,
        query=args.query,
        documents=documents,
        answer_text=answer.answer_text,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
