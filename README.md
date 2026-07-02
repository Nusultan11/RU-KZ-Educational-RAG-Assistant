# RU-KZ Educational RAG Assistant

Двуязычный образовательный RAG-ассистент для русского и казахского языков.

## Текущий этап

Stage 2: EDA Foundation.

На этом этапе создаётся воспроизводимый способ проверить структуру и качество четырёх датасетов до preprocessing, chunking, embeddings и RAG.

EDA фиксирует:

- доступные dataset configs и splits;
- колонки и количество строк;
- пустые значения и полные дубли;
- примеры записей;
- длины текстовых полей и percentiles;
- ошибки загрузки отдельных датасетов.

Language detection пока отключён в `configs/eda.yaml`. Он будет добавлен отдельным проверяемым шагом.

## Pipeline

1. Project Control
2. EDA Foundation
3. Data Quality Report
4. Preprocessing
5. Retrieval baseline
6. RAG baseline
7. Evaluation
8. QLoRA, только если она обоснована результатами evaluation

## Stage 1 Files

- `configs/datasets.yaml`
- `docs/project_control/problem_formulation.md`
- `docs/project_control/dataset_inventory.md`
- `docs/project_control/eda_plan.md`

## Download datasets

```bash
python scripts/download_datasets.py --config configs/datasets.yaml --output-dir data/raw/hf
```

Локальные dataset snapshots сохраняются в `data/` и не коммитятся.

## Run EDA

```bash
python scripts/run_eda.py \
  --datasets-config configs/datasets.yaml \
  --eda-config configs/eda.yaml
```

Отчёты сохраняются в:

```text
reports/eda/
  kazakh_wiki_rag_dataset.json
  sberquad_retrieval.json
  kazakh_instruction_v2.json
  russian_instructions_2.json
  summary.md
```

Профилирование использует детерминированную head-выборку размером `eda.sample_size`. Каждый отчёт отдельно показывает полное количество строк и число проанализированных записей.

## Stage 2 validation

Полный Hugging Face EDA-run выполнен 2026-07-02. Все четыре dataset reports и `summary.md` созданы со статусом `success`.

Реальные структуры:

- KZ retrieval: pairs `anchor/positive/source` и triplets `anchor/positive/negative/source`;
- RU retrieval: configs `corpus` и `queries`;
- KZ instruction: `instruction/input/output`;
- RU instruction: `question/answer`.

Это завершает EDA foundation, но не заменяет следующий Data Quality Report и не разрешает автоматически переходить к preprocessing или RAG tuning.

## Основное правило

Нельзя выбирать `chunk_size`, embedding model, reranker или QLoRA до EDA и retrieval evaluation.
