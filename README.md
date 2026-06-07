# RUKZ Educational RAG Assistant

LLM + RAG educational assistant for Russian and Kazakh languages.

The project is organized as a controlled ML system, not as a collection of notebooks or one-off scripts. The architecture separates data loading, EDA, preprocessing, indexing, retrieval, generation, evaluation, API, UI, monitoring, and future training work.

## Current Stage

Current stage: architecture skeleton only.

Do not start EDA, preprocessing, RAG implementation, API implementation, or QLoRA training from this step.

## Architecture Layers

- `src/rag_assistant/core`: shared configuration, logging, exceptions, registries.
- `src/rag_assistant/data`: dataset loading contracts, schemas, validation.
- `src/rag_assistant/eda`: dataset profiling and quality reporting.
- `src/rag_assistant/preprocessing`: normalization, cleaning, deduplication, language filtering, chunking.
- `src/rag_assistant/indexing`: embedding and vector-store boundaries.
- `src/rag_assistant/retrieval`: language routing, query processing, retrieval, reranking, context building.
- `src/rag_assistant/generation`: prompt building, LLM client boundary, answer generation, response validation.
- `src/rag_assistant/evaluation`: retrieval, RAG, and generation metrics.
- `src/rag_assistant/training`: future retriever fine-tuning and QLoRA planning.
- `src/rag_assistant/api`: future FastAPI boundaries.
- `src/rag_assistant/monitoring`: logging, feedback, tracing boundaries.

## Pipeline Order

1. Problem formulation
2. Dataset inventory
3. EDA
4. Data quality report
5. Preprocessing plan
6. Preprocessing implementation
7. Baseline RAG
8. Retrieval and RAG evaluation
9. Error analysis
10. Improvements
11. Re-evaluation
12. QLoRA only if justified
13. Productionization

## Documentation

- `docs/architecture/system_design.md`
- `docs/architecture/data_flow.md`
- `docs/architecture/rag_pipeline.md`
- `docs/architecture/evaluation_design.md`
- `docs/project_control/`
- `docs/mcp/`

## Quality Rules

- EDA must happen before preprocessing.
- Retrieval evaluation must happen before RAG tuning.
- QLoRA must not start before baseline RAG, EDA, preprocessing, retrieval evaluation, RAG evaluation, and error analysis.
- All parameters should live in `configs/`.
- No secrets in the repository.

