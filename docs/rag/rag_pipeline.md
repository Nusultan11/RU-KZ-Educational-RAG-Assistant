# End-to-End RAG Pipeline

This document records the first local end-to-end RAG runner for the project.

## Goal

The runner connects the already implemented retrieval and RAG components:

```text
query
-> FAISS index search
-> RetrievedDocument objects
-> ContextBuilder
-> PromptBuilder
-> Generator
-> answer
```

The step is intended for local smoke testing before adding API, UI, streaming, or model-quality upgrades.

## Files

```text
scripts/run_rag.py
configs/retriever_baseline.yaml
configs/rag_context.yaml
configs/rag_prompt.yaml
configs/rag_generator.yaml
```

The script reads local FAISS indexes from `indexes/baseline`, but indexes are local artifacts and must not be committed.

## CLI

```bash
python scripts/run_rag.py \
  --query "жарық жылдамдығы деген не" \
  --lang kk \
  --index-dir indexes/baseline \
  --retriever-config configs/retriever_baseline.yaml \
  --context-config configs/rag_context.yaml \
  --prompt-config configs/rag_prompt.yaml \
  --generator-config configs/rag_generator.yaml
```

Russian smoke-test example:

```bash
python scripts/run_rag.py \
  --query "что такое скорость света" \
  --lang ru \
  --index-dir indexes/baseline \
  --retriever-config configs/retriever_baseline.yaml \
  --context-config configs/rag_context.yaml \
  --prompt-config configs/rag_prompt.yaml \
  --generator-config configs/rag_generator.yaml
```

## Behavior

1. Loads retriever, context, prompt, and generator configs.
2. Loads `{lang}.index` and `{lang}_metadata.jsonl` from the index directory.
3. Encodes the query with the configured embedding model.
4. Retrieves top-k documents with FAISS.
5. Deduplicates retrieved results by text by default.
6. Converts metadata rows into `RetrievedDocument` objects.
7. Builds an LLM-ready `RAGContext`.
8. Builds a final prompt.
9. Runs the configured local Transformers generator.
10. Prints retrieved sources and the generated answer.

## Current Limitations

- No API layer.
- No streaming.
- No reranker.
- No fine-tuned generator.
- No prompt or answer evaluation yet.
- Index files are local and are not committed.
- The generator model may need to be downloaded or loaded from local cache on the first run.
- RU retrieval evaluation remains limited by unresolved relevance mapping.

## Completion Criteria

This stage is complete when the runner can execute both smoke tests:

```text
kk query -> retrieved KZ context -> generated answer
ru query -> retrieved RU context -> generated answer
```

After smoke tests, the next decision is whether `feature/rag-pipeline` is ready to merge or needs a small fix before merge.
