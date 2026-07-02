# EDA Plan

## Цель

Понять структуру, качество и ограничения данных до preprocessing, chunking, embeddings, RAG и QLoRA.

## Что проверяем

1. Колонки датасетов.
2. Размеры.
3. Пустые значения.
4. Дубли.
5. Длины question / answer / context.
6. Языки ru / kk / en.
7. HTML-мусор и спецсимволы.
8. Retrieval-пары.
9. Instruction-формат.
10. Риски данных.

## Какие решения должны выйти после EDA

- Какой выбрать `chunk_size`.
- Какой выбрать `chunk_overlap`.
- Нужны ли отдельные RU/KZ индексы.
- Нужен ли language router.
- Можно ли честно считать Recall@k и MRR.
- Какие записи нужно удалить.
- Какие данные подходят для retrieval.
- Какие данные подходят для instruction/SFT.

## Запрет

До завершения EDA нельзя делать preprocessing, RAG tuning или QLoRA.

## Реализация Stage 2

EDA реализуется воспроизводимым CLI:

```bash
python scripts/run_eda.py \
  --datasets-config configs/datasets.yaml \
  --eda-config configs/eda.yaml
```

Параметры анализа находятся в `configs/eda.yaml`. Базовый этап использует детерминированную head-выборку и считает:

- колонки, configs и splits;
- полное и проанализированное количество строк;
- пустые значения;
- полные дубли внутри проанализированной выборки;
- примеры записей;
- min, max, mean, median и percentiles длин текстовых полей.

Машиночитаемые JSON-отчёты и общий `summary.md` сохраняются в `reports/eda/`.

Language detection на этом подшаге отключён, чтобы базовый EDA не зависел от дополнительной модели или внешнего language-detection package.

## Результат валидации

Полный запуск на Hugging Face выполнен 2026-07-02:

- `shyngys879/Kazakh-Wiki-RAG-Dataset`: две load-configurations, четыре splits, статус `success`;
- `kaengreg/sberquad-retrieval`: configs `corpus` и `queries`, статус `success`;
- `AmanMussa/kazakh-instruction-v2`: train split, статус `success`;
- `Den4ikAI/russian_instructions_2`: train split, статус `success`.

KZ retrieval repository содержит CSV с несовместимыми схемами, поэтому pairs и triplets загружаются отдельными configurations из `configs/datasets.yaml`. Это предотвращает смешение `anchor/positive/source` и `anchor/positive/negative/source`.

Stage 2 EDA Foundation считается завершённым. Следующий допустимый этап — Data Quality Report; preprocessing остаётся запрещённым до отдельного плана и решения continue/stop.
