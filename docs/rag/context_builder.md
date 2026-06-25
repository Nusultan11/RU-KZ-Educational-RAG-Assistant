# RAG Context Builder

## Goal

Build the context layer between retrieval and generation:

```text
Query -> Retriever -> Top-k passages -> Context Builder -> RAGContext
```

This stage does not call an LLM and does not build prompts for a specific model.

## Inputs

- user question;
- top-k retrieved passages;
- document metadata such as `doc_id`, `source`, `language`, and `score`.

## Output

The output is a `RAGContext` object with:

- original question;
- selected retrieved documents;
- bounded `context_text`;
- truncation flag;
- omitted document count.

## Context Limit

The baseline context limit is configured in:

```text
configs/rag_context.yaml
```

Current value:

```text
max_context_chars = 6000
```

This keeps the first context builder deterministic and model-independent. Token-based limits can be added later when a generator model is selected.

## Current Scope

Implemented:

- `RetrievedDocument`;
- `RAGContext`;
- `ContextBuilder`;
- source, score, language, and document id rendering;
- max character budget;
- LLM-ready context text.

Not implemented:

- generator call;
- prompt template selection;
- tokenization;
- reranking;
- citation validation.

## Next Step

After this component is verified, the next stage can add RAG generation in a separate branch.
