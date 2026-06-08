# Embedding Selection

## Goal

Choose a practical baseline embedding model for the first retrieval baseline.

This document is a design artifact only. No model is downloaded, loaded, or benchmarked in this stage.

## Requirements

The baseline embedding model must:

- support Russian;
- support Kazakh;
- work for semantic retrieval;
- be available through common Python tooling;
- be reproducible from config;
- be small enough for local experimentation;
- provide a clear path to later comparison.

## Baseline Choice

Recommended baseline:

```text
intfloat/multilingual-e5-base
```

## Why This Baseline

- It is multilingual.
- It is designed for embedding/retrieval use cases.
- It can be used for both RU and KZ baseline experiments.
- It keeps the first retrieval implementation simple.
- It avoids starting with model fine-tuning.

## Query and Passage Format

For E5-style models, use explicit prefixes:

```text
query: <user query>
passage: <document or context>
```

This should be documented in the retrieval implementation config later.

## Alternatives To Compare Later

Potential comparison models:

- `intfloat/multilingual-e5-small`
- `intfloat/multilingual-e5-large`
- `BAAI/bge-m3`
- LaBSE-style multilingual sentence embeddings

These alternatives should be compared only after the baseline retrieval evaluation pipeline exists.

## Reranker Decision

Baseline:

```text
reranker = disabled
```

Reason:

- First measure embedding-only retrieval.
- Add reranker only after error analysis shows that top-k contains relevant contexts ranked too low.

## Metrics Needed For Model Choice

Model choice should be based on:

- Recall@5;
- Recall@10;
- MRR@10;
- nDCG@10;
- latency;
- memory use;
- language-specific breakdown for RU/KZ.

## Risks

- Kazakh quality may be weaker than Russian quality.
- Russian relevance mapping is still unresolved.
- Long RU corpus texts may require chunking before fair embedding evaluation.
- KZ positives are short enough for a simple baseline, but duplicate negatives need review.

## Decision

Use `intfloat/multilingual-e5-base` as the baseline candidate, then compare alternatives only after retrieval evaluation is implemented.

