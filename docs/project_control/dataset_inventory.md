# Инвентарь датасетов

## Назначение

Этот документ фиксирует роль каждого датасета до доступа к данным, EDA, preprocessing или training.

Инвентарь не является результатом анализа данных. Это планировочный документ: он описывает, для чего каждый датасет нужен в проекте и какие вопросы должен закрыть будущий EDA.

## Роли датасетов

| Датасет | Язык | Основная роль | Ожидаемое использование |
| --- | --- | --- | --- |
| `Kazakh-Wiki-RAG-Dataset` | `kk` | Retrieval corpus | Казахский поиск документов/контекста для baseline RAG |
| `sberquad-retrieval` | `ru` | Retrieval dataset | Русская retrieval evaluation и baseline RAG |
| `kazakh-instruction-v2` | `kk` | Instruction dataset | Будущий анализ казахского instruction/SFT стиля только после RAG gates |
| `russian_instructions_2` | `ru` | Instruction dataset | Будущий анализ русского instruction/SFT стиля только после RAG gates |

## Правило разделения

Retrieval-датасеты и instruction-датасеты нельзя смешивать.

Retrieval-датасеты описывают задачу:

```text
query -> relevant context
```

Instruction-датасеты описывают задачу:

```text
instruction/input -> output
```

У них разные схемы, проверки качества, метрики и риски.

## Вопросы для retrieval-датасетов

Для каждого retrieval-датасета EDA должен ответить:

- какие колонки содержат query, answer, context, document, title, source и metadata;
- есть ли train, validation и test split;
- есть ли явный positive context для каждого query;
- есть ли negative examples или можно ли их построить;
- можно ли честно считать Recall@k, MRR и nDCG;
- разделены ли русские и казахские записи;
- доступны ли стабильные source citations.

## Вопросы для instruction-датасетов

Для каждого instruction-датасета EDA должен ответить:

- какие колонки содержат instruction, input, output, language и metadata;
- являются ли ответы полными и образовательными;
- есть ли дубли;
- есть ли unsafe, toxic, malformed или low-value записи;
- есть ли train, validation и test split;
- пригоден ли датасет для будущего QLoRA только после baseline RAG, evaluation и error analysis.

## Решение Stage 1

На этом этапе датасеты разрешены только для планирования. Файлы данных нельзя открывать, пока пользователь явно не утвердит scope для EDA implementation.
