# RU-KZ Educational RAG Assistant

Двуязычный образовательный RAG-ассистент для русского и казахского языков.

## Текущий этап

Stage 1: Project Control.

Сейчас фиксируем:

- цель проекта;
- проблему проекта;
- роли датасетов;
- EDA-план;
- конфиг источников данных.

Пока не делаем:

- preprocessing;
- RAG pipeline;
- embeddings;
- chunking;
- QLoRA;
- API/UI.

Главная идея:

```text
Сначала цель, данные и EDA-план. Только потом код.
```

## Pipeline

1. Project Control
2. EDA scripts
3. Preprocessing
4. Retrieval baseline
5. RAG baseline
6. Evaluation
7. QLoRA, если реально нужна

## Stage 1 Files

- `configs/datasets.yaml`
- `docs/project_control/problem_formulation.md`
- `docs/project_control/dataset_inventory.md`
- `docs/project_control/eda_plan.md`

## Download datasets

```bash
python scripts/download_datasets.py --config configs/datasets.yaml --output-dir data/raw/hf
```

## Основное правило

Нельзя выбирать `chunk_size`, embedding model, reranker или QLoRA до EDA и retrieval evaluation.
