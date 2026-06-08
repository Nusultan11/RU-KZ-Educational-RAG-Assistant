# Russian Retrieval EDA Findings

## Dataset

- Name: `kaengreg/sberquad-retrieval`
- Role: Russian retrieval dataset
- Stage: Retrieval EDA findings report

## Current Status

EDA notebook: `notebooks/eda_ru_corpus_rag.ipynb`.

The notebook inspected the Hugging Face dataset configs `corpus` and `queries`. No preprocessing, chunking, embeddings, indexing, RAG, or QLoRA were performed.

## Findings

### Sizes

Measured:

- corpus config: `17,474` rows, `5` columns;
- queries config: `74,300` rows, `5` columns;
- corpus `_id` range: `0..17473`;
- queries `_id` range: `100..74399`;
- corpus unique `text`: `13,489`.

### Columns

Confirmed columns:

- corpus: `_id`, `title`, `text`, `processed_text`, `processed_title`;
- queries: `_id`, `text`, `processed_text`, `title`, `processed_title`;
- available configs: `corpus`, `queries`.

### Duplicates

Measured:

- corpus duplicate `text`: `3,985`;
- query duplicate `text`: `16`;
- corpus unique text count is lower than row count, so duplicate filtering needs a documented rule before preprocessing.

### Lengths

Measured on corpus `text`:

- mean: `751.98`;
- p50: `681`;
- p75: `856`;
- p90: `1072.7`;
- p95: `1204`;
- p99: `1596.16`;
- max: `7231`.

Measured on corpus `processed_text`:

- mean: `629.24`;
- p50: `572`;
- p75: `716`;
- p90: `896.7`;
- p95: `1002`;
- p99: `1342.27`;
- max: `5948`.

### Retrieval Readiness

Status: blocked by relevance mapping question.

The key unresolved question is:

```text
Where is the relevance mapping for sberquad-retrieval?
```

Before retrieval evaluation, the project must identify how each query maps to its relevant context(s). Without this mapping, Recall@k, MRR, and nDCG cannot be computed honestly.

## Conclusions

- Russian corpus and query schemas are known.
- Russian corpus has substantial duplicate text: `3,985` duplicate rows.
- Query text duplicates are low: `16`.
- Title and processed title are empty in all checked rows, so source/citation strategy cannot rely on title fields.
- The dataset cannot be used for a reliable retrieval baseline until relevance mapping is confirmed.
- No RAG tuning should be done from this dataset yet.

## Open Questions

1. Which field or file maps query ids to relevant context ids?
2. Are there explicit qrels or only positive contexts per row?
3. Are negative examples present or must they be sampled later?
4. Are train/validation/test splits already defined?
5. Are source references stable enough for citation evaluation?

## Next Step

Run a scoped EDA script that loads only dataset metadata/schema first, then records column names, split names, row counts, and relevance mapping evidence.
