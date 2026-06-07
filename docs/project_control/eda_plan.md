# EDA Plan

## Цель

Определить, что нужно проверить до preprocessing, indexing, baseline RAG и QLoRA.

EDA должен дать доказательную базу для решений: `chunk_size`, `chunk_overlap`, language routing, фильтрация данных, split strategy, retrieval metrics и будущая пригодность fine-tuning.

## Scope

План покрывает:

- retrieval-датасеты для русского и казахского RAG;
- instruction-датасеты для будущего анализа;
- структуру, размер, язык, качество текста, дубли и evaluation readiness.

Этот план не реализует EDA и не открывает `data/`.

## EDA-проверки

### 1. Структура датасетов

Проверить:

- доступные файлы и splits;
- колонки;
- поля query/question;
- поля answer/output;
- поля context/document;
- поля source и metadata;
- стабильные ids.

Результат:

- schema report по каждому датасету;
- missing-column risks;
- mapping raw columns -> internal contracts.

### 2. Размеры данных

Проверить:

- количество строк;
- количество уникальных документов;
- количество уникальных вопросов или instructions;
- размеры train/validation/test;
- пустые или null значения;
- дубли строк.

Результат:

- таблица размеров по датасетам и splits;
- missing-value report;
- duplicate report.

### 3. Длины текстов

Проверить:

- длину question;
- длину answer;
- длину context/document;
- длину instruction;
- длину output;
- p50, p75, p90, p95, p99.

Результат:

- length distribution report;
- кандидаты для `chunk_size`, `chunk_overlap` и `max_seq_length`.

### 4. Распределение языков

Проверить:

- русские записи;
- казахские записи;
- английские или другие языки;
- смешанные записи;
- записи, где заявленный язык конфликтует с detected language.

Результат:

- language distribution table;
- рекомендация: один общий index или отдельные RU/KZ indexes;
- требования к language router.

### 5. Качество текста

Проверить:

- HTML markup;
- лишние пробелы;
- broken encoding;
- special-character noise;
- слишком короткие записи;
- слишком длинные записи;
- boilerplate;
- malformed rows.

Результат:

- data quality report;
- preprocessing recommendations;
- записи для manual review.

### 6. Retrieval readiness

Проверить:

- наличие query;
- наличие positive context;
- наличие source;
- negative examples;
- duplicate или near-duplicate contexts;
- поддерживают ли labels расчет Recall@k, MRR и nDCG.

Результат:

- решение о retrieval evaluation readiness;
- baseline retrieval metric plan;
- риски для RAG evaluation.

### 7. Instruction readiness

Проверить:

- наличие instruction/input/output;
- полноту ответов;
- unsafe или low-quality records;
- дубли;
- language consistency;
- future QLoRA suitability.

Результат:

- instruction dataset quality report;
- решение, что QLoRA остается заблокирован до baseline RAG, retrieval evaluation, RAG evaluation и error analysis.

## Решения, которые должен поддержать EDA

| Решение | Нужное доказательство |
| --- | --- |
| `chunk_size` | Percentiles длины document/context |
| `chunk_overlap` | Структура текста и context length distribution |
| Отдельные RU/KZ indexes или общий index | Language distribution и retrieval baseline |
| Language router strategy | Доля mixed-language и unknown-language |
| Embedding model shortlist | Структура retrieval datasets и language coverage |
| Нужен ли reranker | Retrieval baseline и error analysis |
| Data filtering rules | Text quality и duplicate reports |
| QLoRA eligibility | Baseline RAG, evaluation и error analysis, не только EDA |

## Quality Gate перед preprocessing

Preprocessing можно начинать только после:

- структура датасетов задокументирована;
- есть size и missing-value reports;
- дубли измерены;
- language distribution измерен;
- text quality issues задокументированы;
- retrieval readiness решен;
- preprocessing recommendations написаны.

## Ожидаемые артефакты будущего EDA implementation

- `artifacts/eda/dataset_inventory_report.md`
- `artifacts/eda/data_quality_report.md`
- `artifacts/eda/language_distribution_report.md`
- `artifacts/eda/text_length_report.md`
- `artifacts/eda/retrieval_readiness_report.md`

Эти пути являются только планируемыми outputs. Их нельзя создавать на Stage 1.
