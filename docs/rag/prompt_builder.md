# RAG Prompt Builder

## Goal

Build a generator-ready prompt from a prepared `RAGContext`.

Pipeline position:

```text
Query -> Retriever -> Context Builder -> Prompt Builder -> Generator
```

This stage does not call a model and does not generate an answer.

## Inputs

- `RAGContext`;
- optional question override;
- prompt configuration from `configs/rag_prompt.yaml`.

## Output

The output is a `RAGPrompt` object with:

- final question;
- full `prompt_text`;
- source `context_text`;
- instruction text;
- metadata for downstream logging.

## Baseline Prompt Policy

Current config:

```text
configs/rag_prompt.yaml
```

The baseline prompt requires the future generator to:

- answer only from retrieved context;
- answer in the same language as the question;
- cite retrieved context item numbers;
- say that the answer is not available when context is insufficient.

## Current Scope

Implemented:

- `RAGPrompt`;
- `PromptBuilder`;
- deterministic prompt assembly;
- configurable instruction;
- source citation instruction;
- insufficient-context instruction.

Not implemented:

- LLM generation;
- model-specific chat template formatting;
- streaming;
- hallucination validation;
- answer scoring.

## Next Step

The next component can be `generator.py`, which will consume `RAGPrompt` and call a selected LLM.
