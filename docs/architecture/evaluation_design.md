# Evaluation Design

## Goal

Evaluation must make RAG changes measurable and comparable.

## Evaluation Stages

1. Dataset inventory for evaluation records.
2. EDA on evaluation data.
3. Retrieval baseline.
4. RAG baseline.
5. Error analysis.
6. Improvement plan.
7. Re-evaluation with the same metrics.

## Retrieval Evaluation

Required metrics:

- Recall@5 and Recall@10
- MRR@10
- nDCG@10
- language-specific breakdown for Russian and Kazakh
- latency

## RAG Evaluation

Required checks:

- answer relevance;
- faithfulness to retrieved context;
- source citation correctness;
- context precision;
- language consistency;
- fallback behavior when context is missing.

## Error Analysis Categories

- wrong language detection;
- bad query normalization;
- missing relevant chunk;
- relevant chunk retrieved too low;
- reranker regression;
- context too long or noisy;
- unsupported LLM claim;
- missing or wrong citation;
- wrong language in final answer.

## Decision Rule

An improvement is accepted only if it improves the targeted metric without unacceptable regression in latency, citation correctness, or language consistency.

