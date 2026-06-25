# KZ Retrieval Evaluation Results

## Run

- Date: 2026-06-25
- Branch: `feature/retrieval-evaluation`
- Evaluation script: `scripts/evaluate_kz_retrieval.py`
- Config: `configs/retriever_baseline.yaml`
- Model: `intfloat/multilingual-e5-base`
- Index: `indexes/baseline/kk.index`
- Metadata: `indexes/baseline/kk_metadata.jsonl`
- Dataset: `shyngys879/Kazakh-Wiki-RAG-Dataset`
- Evaluation examples: `17,320`
- Query field: `anchor`
- Relevant passage field: `positive`
- Top-k: `5`

## Command

```bash
python scripts/evaluate_kz_retrieval.py --config configs/retriever_baseline.yaml --index-dir indexes/baseline --top-k 5
```

## Metrics

| Metric | Value |
| --- | ---: |
| Recall@1 | `0.640473` |
| Recall@5 | `0.803926` |
| MRR@5 | `0.704153` |

## Result Summary

The KZ baseline retrieval evaluation completed successfully on all `17,320` anchor-positive examples.

The current embedding-only FAISS baseline retrieves the paired positive passage in top-5 for about `80.39%` of queries and ranks it first for about `64.05%` of queries.

## Notes

- The evaluation uses the KZ dataset because it has explicit `anchor -> positive` pairs.
- The baseline uses the already built local `kk.index` and `kk_metadata.jsonl`.
- Metadata alignment is checked before metric computation.
- No reranker is used.
- No chunking is used.
- No RAG generation is evaluated in this step.

## Limitations

- The evaluation uses the same `train_triplets.csv` source used to build the baseline KZ index, so this is an index correctness and retrieval baseline measurement, not a held-out generalization test.
- KZ has no separate validation/test split documented in the current project state.
- RU retrieval evaluation is still postponed because `sberquad-retrieval` relevance mapping remains unresolved.
- Local index artifacts under `indexes/` are not committed.
- Local dataset artifacts under `data/` are not committed.

## Decision

The KZ retrieval baseline is functional and measurable.

Recommended next decision:

```text
Proceed to RAG baseline if current Recall@5 is acceptable for a first end-to-end pipeline, or improve retrieval first if higher KZ recall is required before generation.
```

Step status: `SUCCESS`.
