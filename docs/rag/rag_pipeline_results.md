# RAG Pipeline Smoke Results

## Status

The local RAG pipeline now works end-to-end:

```text
query
-> FAISS search
-> RetrievedDocument
-> ContextBuilder
-> PromptBuilder
-> Generator
-> formatted answer
```

The pipeline uses local indexes and local model/cache artifacts. These artifacts are not committed.

## KZ Smoke Test

Command:

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

Result: passed after prompt, generator, chat-template, and postprocessing fixes.

Observed answer shape:

```text
Жауап:
Берілген контексте ... Жарық жылдамдығын ... топтық жылдамдықты ... өлшейді.

Дереккөздер: [1]
```

KZ smoke criteria:

- Kazakh answer: passed.
- No English answer: passed.
- No repeated fallback text: passed.
- Required `Жауап:` block: passed.
- Required `Дереккөздер: [1]` block: passed.
- No `Context Items Used` block: passed.

## RU Smoke Test

Command:

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

Result: passed by format.

Observed answer shape:

```text
Ответ:
Скорость света ...

Источники: [1]
```

RU smoke criteria:

- Russian answer format: passed.
- No English answer: passed.
- No repeated answer block: passed.
- Required `Ответ:` block: passed.
- Required `Источники: [1]` block: passed.
- No `Context Items Used` block: passed.

## Fixes Applied

The RAG smoke tests required several quality fixes:

- stricter RU/KZ prompt rules;
- required answer format for RU and KZ;
- shorter deterministic generation settings;
- repetition controls;
- Qwen chat-template formatting;
- post-generation answer-format normalization;
- extractive safety fallback when the model output is clearly noisy.

## Limitations

- RU answer language quality is not ideal.
- `Qwen/Qwen2.5-1.5B-Instruct` is useful for smoke testing but weak for final answer quality.
- Postprocessing is required as a safety layer because the small generator does not reliably follow format instructions.
- Retrieval indexes are local and are not committed.
- Dataset files are local and are not committed.
- Model/cache artifacts are local and are not committed.
- Current smoke tests check pipeline behavior and answer format, not full answer quality.

## Decision

The `feature/rag-pipeline` branch is ready for merge preparation from a smoke-test perspective.

The next major branch should be:

```text
feature/rag-quality-evaluation
```

Focus:

```text
build a small RU/KZ evaluation set and evaluate answer quality, not only answer format
```
