# Retrieval Architecture

## Stage

Feature branch: `feature/retrieval-design`.

This document defines retrieval design only. No retriever implementation, preprocessing, indexing, RAG generation, or QLoRA is done in this stage.

## Goal

Design the baseline retrieval layer for the RU/KZ Educational RAG Assistant.

The retrieval layer must answer:

1. Which data goes into the index?
2. Should RU and KZ use separate indexes?
3. Is a language router required?
4. What is the baseline embedding model?
5. Is a reranker part of baseline?
6. Which retrieval metrics will be used?
7. What does the retrieval pipeline look like?

## EDA Inputs

### Kazakh Retrieval

Dataset: `shyngys879/Kazakh-Wiki-RAG-Dataset`

Known from EDA:

- `train.csv`: `17,320` rows;
- `train_pairs.csv`: `17,320` rows;
- `train_triplets.csv`: `17,320` rows;
- confirmed columns: `anchor`, `positive`, `negative`, `source`;
- duplicate `anchor`: `0`;
- duplicate `positive`: `0`;
- duplicate `negative`: `6,119`;
- positive p50 length: `306`;
- positive p95 length: `629`;
- positive max length: `650`.

### Russian Retrieval

Dataset: `kaengreg/sberquad-retrieval`

Known from EDA:

- corpus: `17,474` rows;
- queries: `74,300` rows;
- corpus columns: `_id`, `title`, `text`, `processed_text`, `processed_title`;
- queries columns: `_id`, `text`, `processed_text`, `title`, `processed_title`;
- corpus duplicate `text`: `3,985`;
- query duplicate `text`: `16`;
- corpus text p50 length: `681`;
- corpus text p95 length: `1204`;
- corpus text max length: `7231`;
- relevance mapping is still unresolved.

## Data That Goes Into Index

### Baseline KZ Index

Index candidate:

- `positive` passages from `Kazakh-Wiki-RAG-Dataset` triplets or pairs.

Query candidate:

- `anchor`.

Rationale:

- `anchor -> positive` is explicit.
- `positive` has manageable lengths and no measured duplicates.
- `negative` has many duplicates and should not be indexed as positive evidence.

### Baseline RU Index

Index candidate:

- corpus `text` from `sberquad-retrieval`.

Query candidate:

- queries `text`.

Rationale:

- corpus and queries configs are explicit.
- corpus text is the document side.
- queries text is the query side.

Risk:

- relevance mapping between query ids and corpus ids is not confirmed yet.
- RU retrieval evaluation must not claim Recall@k/MRR/nDCG until relevance mapping is found.

## Separate Indexes vs Shared Index

Decision for baseline design:

```text
Use separate RU and KZ indexes first.
```

Reasons:

- RU and KZ datasets have different schemas.
- KZ has explicit anchor-positive-negative records.
- RU has separate corpus and queries configs.
- Separate indexes simplify debugging and per-language evaluation.
- A shared multilingual index can be tested later after baseline metrics exist.

## Language Router

Decision for baseline design:

```text
Use a simple language router.
```

Routing:

- `kk` -> KZ index
- `ru` -> RU index
- unknown/mixed -> search both indexes and merge top-k results

Why:

- The product is bilingual.
- Separate indexes require routing.
- Unknown-language fallback prevents hard failure.

## Baseline Retrieval Pipeline

```text
user query
  -> language detection
  -> query normalization
  -> route to RU/KZ/both
  -> query embedding
  -> vector search
  -> top-k candidates
  -> context candidate output
  -> retrieval logging
```

## Reranker

Decision for baseline:

```text
No reranker in the first baseline.
```

Why:

- Baseline should isolate embedding retrieval quality.
- Reranker adds another variable.
- Reranker decision should come after retrieval metrics and error analysis.

## Logging Fields

Each retrieval call should log:

- query text hash or id;
- detected language;
- selected index;
- embedding model name;
- top-k;
- returned document ids;
- retrieval scores;
- latency;
- fallback path, if used.

## Open Questions

1. Where is relevance mapping for `sberquad-retrieval`?
2. Are KZ validation/test splits available?
3. Should KZ duplicate negatives be removed or downweighted?
4. Which language detector should be used in baseline?
5. Should RU corpus duplicates be filtered before indexing?

