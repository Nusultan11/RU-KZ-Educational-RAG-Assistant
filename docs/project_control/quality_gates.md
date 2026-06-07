# Quality Gates

Quality gates define when a step can be called successful.

## Documentation-Only Gate

Required:

- required files exist;
- Markdown files are readable;
- no obvious secret patterns were introduced;
- no business logic was intentionally changed;
- skipped code checks are explained.

## Code Gate

Required when code changes are made:

- formatting;
- lint;
- type check;
- unit tests;
- integration tests when available;
- smoke test when relevant;
- no secrets in changed files;
- no accidental changes in `data/`;
- no large binary files added;
- documentation updated when behavior changes.

## ML and Data Gate

Required for ML/data work:

- problem statement;
- dataset inventory;
- EDA before preprocessing;
- fixed evaluation data;
- baseline metrics;
- error analysis;
- reproducible configuration;
- logged experiment parameters.

## RAG Gate

Required for RAG work:

- retrieval baseline;
- retrieval metrics;
- source citation checks;
- response faithfulness checks;
- latency and token usage tracking;
- error analysis before improvements.

## QLoRA Gate

Required before QLoRA:

- baseline RAG;
- EDA;
- preprocessing;
- retrieval evaluation;
- RAG evaluation;
- error analysis;
- documented reason fine-tuning is needed.

