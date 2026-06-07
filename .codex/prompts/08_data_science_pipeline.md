# Data Science Pipeline Prompt

Use this prompt for data and ML planning.

## Strict Order

1. Problem formulation
2. Dataset inventory
3. EDA
4. Data quality report
5. Preprocessing plan
6. Preprocessing implementation
7. Baseline model or baseline RAG
8. Evaluation
9. Error analysis
10. Improvement plan
11. Re-evaluation
12. Documentation
13. Productionization

## Hard Rule

Preprocessing is forbidden before EDA.

## Required Output For Each Stage

- objective;
- allowed input files;
- generated artifacts;
- metrics;
- validation checks;
- risks;
- decision to continue or stop.

## Guardrails

- Do not open `data/` from root without user permission.
- Do not mutate raw data during EDA.
- Do not introduce preprocessing logic before documenting data quality issues.
- Do not compare models without fixed evaluation data and metrics.

