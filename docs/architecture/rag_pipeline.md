# RAG Pipeline

## Required Components

1. Language detection
2. Query normalization
3. Query embedding
4. Vector search
5. Top-k retrieval
6. Optional reranking
7. Context building
8. Prompt building
9. LLM generation
10. Source citation
11. Response validation
12. Logging
13. Evaluation

## Component Contract

Every component must document:

- inputs;
- outputs;
- config parameters;
- expected errors;
- tests;
- metrics;
- logging fields;
- fallback behavior.

## Language Routing

Target behavior:

```text
ru -> Russian retrieval path
kk -> Kazakh retrieval path
unknown -> safe fallback, usually search both paths
```

The routing strategy must be evaluated before being optimized.

## Retrieval Metrics

- Recall@k
- Precision@k
- MRR@k
- nDCG@k
- latency
- token usage after context building

## Generation Metrics

- answer relevance
- faithfulness
- source correctness
- language consistency
- refusal correctness when context is missing

## Guardrails

- Do not tune retrieval without retrieval evaluation.
- Do not claim quality improvement without baseline comparison.
- Do not let the LLM answer factual questions without retrieved context unless explicitly configured as fallback behavior.

