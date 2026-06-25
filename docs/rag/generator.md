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
- config-compatible generation parameters;
- deterministic decoding for smoke tests;
- repetition controls with `repetition_penalty` and `no_repeat_ngram_size`;
- generation kwargs filtering so sampling-only parameters are not passed when `do_sample=false`;
- Qwen/Instruct chat-template formatting;
- simple post-processing that collapses consecutive duplicate lines;
- answer-format normalization for RU/KZ outputs.

## Repetition Control

The first KZ RAG smoke test after prompt hardening answered in Kazakh, but repeated the same fallback sentence many times. The generator config now uses shorter deterministic generation:

```yaml
generation:
  max_new_tokens: 160
  do_sample: false
  repetition_penalty: 1.15
  no_repeat_ngram_size: 4
```

When `do_sample=false`, the wrapper does not pass sampling-only parameters such as `temperature`, `top_p`, or `top_k` to the Transformers pipeline. This avoids ignored-flag warnings and keeps smoke-test decoding deterministic.

The wrapper also collapses consecutive duplicate lines in the generated answer. This is intentionally minimal post-processing, not a full answer validator.

## Chat Template

The baseline model is an instruct model, so the wrapper formats prompts with the tokenizer chat template before generation:

```text
system: You are a strict multilingual educational RAG assistant. Follow the requested answer language and answer format exactly.
user: <RAG prompt text>
assistant:
```

Config record:

```yaml
prompt_format:
  use_chat_template: true
  system_message: "You are a strict multilingual educational RAG assistant. Follow the requested answer language and answer format exactly."
```

`scripts/run_rag.py` currently instantiates the wrapper with default prompt-format values, so chat-template mode is active even before runner-level config wiring is added.

## Answer Normalization

The wrapper applies a minimal post-generation normalizer after decoding:

```text
raw_answer -> normalized_answer
```

Config record:

```yaml
postprocessing:
  normalize_answer_format: true
  fallback_source: "[1]"
  max_answer_sentences: 3
```

For Kazakh outputs, the normalizer:

- maps `Жауабы:` and `Жауобы:` to `Жауап:`;
- maps `Дереккерлер:` to `Дереккөздер:`;
- adds `Жауап:` when missing;
- adds `Дереккөздер: [1]` when missing;
- removes service lines such as `Context Items Used`, `Source:`, and `Answer:`;
- limits the answer body to 1-3 sentences before the source block.
- replaces clearly noisy model text with a short extractive fallback from context item `[1]`.

For Russian outputs, it applies the same shape with `Ответ:` and `Источники:`.

Not implemented:

- streaming;
- API endpoint;
- fine-tuning;
- 4-bit quantization;
- answer validation;
- RAG evaluation.

## Next Step

The next step is `scripts/run_rag.py`, which should connect:

```text
retriever -> context builder -> prompt builder -> generator
```
