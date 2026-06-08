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
