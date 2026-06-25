# RAG Generator Wrapper

## Goal

Add the generator boundary for the RAG pipeline:

```text
RAGPrompt -> LLM -> generated answer
```

This stage adds only a wrapper. It does not add API serving, streaming, fine-tuning, or model quality evaluation.

## Baseline Model

Baseline config:

```text
configs/rag_generator.yaml
```

Initial model:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

Reason:

- smaller than 7B models;
- faster for smoke tests;
- lower VRAM requirement;
- enough to validate the RAG pipeline wiring before quality upgrades.

## Inputs

- `RAGPrompt` or raw prompt string;
- generator config;
- local or downloadable Transformers model.

## Output

The wrapper returns `GeneratedAnswer`:

- `answer_text`;
- original `prompt_text`;
- `model_name`;
- generation metadata.

## Implementation

Implemented:

- `GeneratedAnswer`;
- `TransformersGenerator`;
- lazy Transformers pipeline loading;
- non-streaming generation;
- config-compatible generation parameters.

Not implemented:

- streaming;
- API endpoint;
- fine-tuning;
- 4-bit quantization;
- model-specific chat template handling;
- answer validation;
- RAG evaluation.

## Next Step

The next step is `scripts/run_rag.py`, which should connect:

```text
retriever -> context builder -> prompt builder -> generator
```
