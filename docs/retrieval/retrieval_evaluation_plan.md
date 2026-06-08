# Retrieval Evaluation Plan

## Goal

Define how retrieval quality will be measured before implementing the retriever.

No evaluation code is written in this stage.

## Evaluation Principles

- Use fixed evaluation data.
- Keep RU and KZ metrics separate.
- Report global and per-language metrics.
- Do not tune the retriever without evaluation.
- Do not compare embedding models without the same splits and metrics.

## Kazakh Evaluation Design

Dataset:

```text
shyngys879/Kazakh-Wiki-RAG-Dataset
```

Known structure:

- query side: `anchor`;
- positive side: `positive`;
- negative side: `negative`;
- source: `source`.

Initial evaluation idea:

- use `anchor` as query;
- index `positive` passages;
- treat paired `positive` as relevant evidence;
- use `negative` only after duplicate-negative policy is defined.

Metrics:

- Recall@5;
- Recall@10;
- MRR@10;
- nDCG@10.

Open risk:

- validation/test splits are not confirmed.
- if only train files exist, create a deterministic split after EDA approval.

## Russian Evaluation Design

Dataset:

```text
kaengreg/sberquad-retrieval
```

Known structure:

- corpus config: document side;
- queries config: query side;
- relevance mapping: unresolved.

Initial evaluation idea:

- index corpus `text`;
- use queries `text` as queries;
- do not report Recall@k/MRR/nDCG until query-to-corpus relevance mapping is found.

Open blocker:

```text
Where is relevance mapping for sberquad-retrieval?
```

Fallback if no relevance mapping exists:

- use RU dataset for corpus-only retrieval smoke tests;
- do not claim retrieval quality metrics;
- find or build a separate RU qrels/evaluation set.

## Metrics

Primary metrics:

- Recall@5
- Recall@10
- MRR@10
- nDCG@10

Operational metrics:

- query embedding latency;
- vector search latency;
- total retrieval latency;
- memory footprint;
- index size;
- number of returned contexts.

Quality diagnostics:

- empty result rate;
- wrong-language result rate;
- duplicate result rate;
- source coverage;
- top-k score distribution.

## Baseline Evaluation Table

Each run should produce a report table:

| dataset | language | split | model | index | top_k | recall@5 | recall@10 | mrr@10 | ndcg@10 | latency_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Acceptance Criteria For Baseline

The baseline is accepted when:

- KZ retrieval metrics are computed on a fixed split;
- RU relevance mapping is resolved or RU metric limitation is documented;
- logs include model, split, index, top-k and latency;
- results are reproducible from config;
- no preprocessing or reranker tuning is hidden inside the baseline.

## Next Implementation Step

After this design is approved, implement a retrieval evaluation scaffold that:

1. loads dataset metadata/config;
2. builds deterministic evaluation records;
3. embeds queries/passages with the baseline model;
4. computes metrics only where relevance labels exist;
5. writes a metrics report.

