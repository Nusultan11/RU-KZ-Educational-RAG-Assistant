# RAG Pipeline Prompt

Use this prompt for RAG design, implementation, and review.

## Required RAG Components

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

## Required Description Per Component

For each component, document:

- inputs;
- outputs;
- configuration parameters;
- tests;
- expected errors;
- metrics;
- logging fields;
- rollback or fallback behavior.

## Quality Gates

Do not tune RAG without retrieval evaluation. Do not claim improvement without comparing against a baseline using fixed metrics.

## Typical Metrics

- Recall@k
- Precision@k
- MRR
- nDCG
- citation accuracy
- answer faithfulness
- answer relevance
- latency
- token usage

