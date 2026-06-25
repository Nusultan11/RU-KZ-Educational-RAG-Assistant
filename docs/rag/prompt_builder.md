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

## Prompt Policy

The prompt requires the future generator to:

- answer only from retrieved context;
- answer in the expected RU/KZ language;
- avoid English answers for RU/KZ prompts;
- avoid repeating the same phrase;
- avoid explanations outside the required answer format;
- avoid writing a `Context Items Used` block;
- cite only source numbers that exist in the retrieved context;
- use the no-answer format when context is insufficient.

## Kazakh Answer Format

For Kazakh contexts, the prompt requires exactly this answer shape:

```text
Жауап:
<1-3 қысқа сөйлем. Тек қазақ тілінде. Тек контекст бойынша.>

Дереккөздер: [1]
```

If the answer is not present in the context:

```text
Жауап:
Берілген контексте бұл сұраққа нақты жауап жоқ.

Дереккөздер: []
```

## Russian Answer Format

For Russian contexts, the prompt requires exactly this answer shape:

```text
Ответ:
<1-3 коротких предложения. Только на русском языке. Только по контексту.>

Источники: [1]
```

If the answer is not present in the context:

```text
Ответ:
В предоставленном контексте нет точного ответа на этот вопрос.

Источники: []
```

## Implementation

Implemented:

- `RAGPrompt`;
- `PromptBuilder`;
- deterministic prompt assembly;
- language-specific hard rules;
- required answer format;
- required no-answer format;
- source citation instruction;
- insufficient-context instruction.

Not implemented:

- LLM generation;
- model-specific chat template formatting;
- streaming;
- hallucination validation;
- answer scoring.
