# Dataset Inventory

## Цель

Разделить датасеты по ролям до EDA, preprocessing и RAG.

## Датасеты

| Датасет | Роль |
| --- | --- |
| `Kazakh-Wiki-RAG-Dataset` | казахский retrieval |
| `sberquad-retrieval` | русский retrieval |
| `kazakh-instruction-v2` | казахский instruction/SFT |
| `russian_instructions_2` | русский instruction/SFT |

## Правило

Retrieval-данные не смешиваем с instruction-данными.

Retrieval-данные нужны для:

```text
query -> relevant context
```

Instruction-данные нужны для:

```text
instruction/input -> output
```

## Что проверить в EDA

Для retrieval-датасетов:

- есть ли query;
- есть ли positive context;
- есть ли source;
- можно ли считать Recall@k, MRR, nDCG.

Для instruction-датасетов:

- есть ли instruction/input/output;
- нет ли дублей;
- нет ли мусорных ответов;
- пригодны ли данные для будущего SFT/QLoRA.
