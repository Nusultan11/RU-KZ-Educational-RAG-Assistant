# Baseline Retriever Results

## Stage

Feature branch: `feature/retrieval-baseline`.

This document records the local baseline retrieval smoke-test results. It does not include local datasets or FAISS index artifacts in Git.

## Built Indexes

The following local artifacts were built under `indexes/baseline/`:

```text
indexes/baseline/ru.index
indexes/baseline/ru_metadata.jsonl
indexes/baseline/kk.index
indexes/baseline/kk_metadata.jsonl
```

These files are local runtime artifacts and must not be committed.

## Commands Used

Install runtime dependencies:

```bash
pip install sentence-transformers faiss-cpu numpy pandas pyarrow pyyaml
```

Download datasets:

```bash
python scripts/download_datasets.py --config configs/datasets.yaml --output-dir data/raw/hf
```

Build baseline indexes:

```bash
python scripts/build_retrieval_index.py --config configs/retriever_baseline.yaml --output-dir indexes/baseline --batch-size 32
```

Search Russian index:

```bash
python scripts/search_retrieval_index.py --config configs/retriever_baseline.yaml --index-dir indexes/baseline --lang ru --query "что такое скорость света" --top-k 5
```

Search Kazakh index:

```bash
python scripts/search_retrieval_index.py --config configs/retriever_baseline.yaml --index-dir indexes/baseline --lang kk --query "жарық жылдамдығы деген не" --top-k 5
```

## Runtime Notes

The baseline was built locally with:

- embedding model: `intfloat/multilingual-e5-base`;
- vector backend: FAISS;
- RU documents: `kaengreg/sberquad-retrieval`, `corpus.text`;
- KZ documents: `shyngys879/Kazakh-Wiki-RAG-Dataset`, `train_triplets.csv`, `positive`;
- chunking: disabled;
- GPU runtime observed during local build: `cuda:0`;
- PyTorch runtime observed during local build: `2.12.0+cu126`.

## RU Smoke Test

Query:

```text
что такое скорость света
```

Result:

- search completed successfully;
- top-1 passage directly defines the speed of light in vacuum;
- top-1 score: `0.859246`;
- top-5 passages are relevant to speed of light definition or measurement history.

The initial RU search showed a duplicate issue:

```text
doc_id=12538
doc_id=12
```

Both records had the same passage text about the speed of light in vacuum. This matches the EDA finding that the RU corpus contains duplicate `text` values.

## KZ Smoke Test

Query:

```text
жарық жылдамдығы деген не
```

Result:

- search completed successfully;
- top-1 passage is about `Жарық жылдамдығы`;
- top-1 score: `0.839463`;
- top-3 and top-4 passages are topically related to phase velocity and light propagation.

## Fixes Added

### Skip/Resume Index Building

`scripts/build_retrieval_index.py` now skips a language index only when both files exist:

```text
<lang>.index
<lang>_metadata.jsonl
```

This made it possible to skip the already built RU index and build only the missing KZ index.

### Result-Level Deduplication

`scripts/search_retrieval_index.py` now supports:

```bash
--deduplicate-results true|false
```

Default:

```text
true
```

Deduplication is done at result level by normalized `text`. The index and metadata are not rebuilt or modified.

After this fix, the RU smoke test no longer returns the same passage as both top-1 and top-2.

## Current Limitations

- RU relevance mapping remains unresolved, so RU retrieval quality is currently validated only by smoke tests.
- KZ retrieval has not yet been evaluated with Recall@k, MRR, or NDCG.
- FAISS indexes and metadata are local runtime artifacts and are not committed.
- RU corpus duplicates still exist in the index; current mitigation is result-level deduplication only.
- No reranker is used in this baseline.
- No RAG generation is included in this stage.

## Decision

Baseline retriever implementation is ready to merge after review.

The verified baseline path is:

```text
query -> embedding -> FAISS search -> top-k passages
```

Step status: `SUCCESS`.
