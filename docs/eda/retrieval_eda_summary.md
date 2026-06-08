# Retrieval EDA Summary

## Scope

This summary covers retrieval EDA status for:

- `shyngys879/Kazakh-Wiki-RAG-Dataset`
- `kaengreg/sberquad-retrieval`

Instruction datasets are out of scope for this retrieval summary.

## Current Status

Retrieval EDA has notebook-level findings for Russian and Kazakh retrieval datasets:

- `notebooks/eda_ru_corpus_rag.ipynb`
- `notebooks/eda_kaz_corpus_rag.ipynb`

The work is not ready for merge to `main` because Russian relevance mapping is still unresolved.

No preprocessing, chunking, embeddings, indexing, RAG, or QLoRA were performed.

## What Must Be Fixed Before Merge To Main

Russian retrieval EDA has one critical open question:

```text
Where is the relevance mapping for sberquad-retrieval?
```

This must be answered before claiming retrieval evaluation readiness.

## Required EDA Evidence

| Area | Kazakh retrieval | Russian retrieval |
| --- | --- | --- |
| Sizes | `17,320` train/pairs/triplets rows | `17,474` corpus rows, `74,300` query rows |
| Columns | `anchor`, `positive`, `negative`, `source` | `_id`, `text`, `processed_text`, `title`, `processed_title` |
| Duplicates | `negative`: `6,119`; `anchor`/`positive`: `0` | corpus duplicate `text`: `3,985`; query duplicate `text`: `16` |
| Lengths | anchor p50 `38`, positive p50 `306`, negative p50 `306` | corpus text p50 `681`, processed text p50 `572` |
| Language distribution | Not measured yet | Not measured yet |
| Relevance mapping | Triplets provide anchor-positive-negative structure | Open critical question |
| Retrieval metrics readiness | Partially ready, needs split/negative review | Not ready |

## Decisions Still Blocked

- final `chunk_size`
- final `chunk_overlap`
- shared vs separate RU/KZ indexes
- language router strategy
- embedding model shortlist
- reranker need
- retrieval metric implementation
- RAG baseline readiness

## Merge Recommendation

Do not merge into `main` yet.

Recommended order:

1. Commit and push notebooks plus retrieval findings documents in `feature/eda-notebook`.
2. Resolve Russian relevance mapping for `sberquad-retrieval`.
3. Measure language distribution.
4. Add final retrieval EDA conclusions.
5. Only then consider merge into `main`.

## Next Step

Implement the EDA script or notebook cells that inspect dataset schemas and metadata first. The first measured output should be a table with dataset name, split, row count, columns, and relevance label availability.
