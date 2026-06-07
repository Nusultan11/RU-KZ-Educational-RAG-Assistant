# Project Operating System Prompt

Use this prompt as the main operating system for Codex work in this project.

## Project

You are working on an LLM + RAG educational assistant for Russian and Kazakh languages.

The goal is to bring the system to production-ready quality through a controlled Data Science and ML Engineering pipeline.

## Problem

The project must answer educational questions reliably, cite sources, support Russian and Kazakh language behavior, and remain testable as the RAG and LLM stack evolves.

## Dataset Roles

Before changing data behavior, identify dataset roles:

- source documents for retrieval;
- metadata used for filtering and citations;
- evaluation sets for retrieval and generation quality;
- instruction or preference data, if fine-tuning is later justified;
- feedback and error-analysis records.

Do not mix these roles without documentation.

## Required Pipeline Order

Follow this strict order:

1. Problem formulation
2. Dataset inventory
3. EDA
4. Data quality report
5. Preprocessing plan
6. Preprocessing implementation
7. Baseline RAG
8. Retrieval evaluation
9. RAG evaluation
10. Error analysis
11. Improvements
12. Re-evaluation
13. QLoRA planning only if justified
14. Productionization

Preprocessing is forbidden before EDA. QLoRA is forbidden before baseline RAG, EDA, preprocessing, retrieval evaluation, RAG evaluation, and error analysis.

## Root Mode

When working from the repository root, do not analyze the whole project.

Allowed root scope:

- `AGENTS.md`
- `.codex/`
- `docs/`
- `docs/project_control/`
- `docs/mcp/`
- `docs/references/`

Ignored unless explicitly approved:

- `data/`
- `notebooks/`
- `tests/`
- `logs/`
- `.git/`
- `models/`
- `checkpoints/`
- `indexes/`
- `artifacts/`
- large binary files

If broader access is needed, ask the user before opening or changing those files.

## Code Quality Rules

Use clean architecture, typed Python, config-driven parameters, small functions, focused modules, useful docstrings, and testable components. Separate data loading, EDA, preprocessing, indexing, retrieval, reranking, generation, evaluation, API, and UI.

Avoid hardcode, long strategy `if` / `else` chains, mixed responsibilities, hidden side effects, and print-based operational logging.

## Reporting Rules

Every completed step must end with:

- status: SUCCESS, PARTIAL, or FAILED;
- changed files;
- what changed and why;
- checks run;
- passed, failed, and skipped checks;
- remaining risks;
- rollback plan;
- next step;
- decision about whether to continue.

## Git Workflow

Use feature branches for substantial changes when the folder is a Git repository. Do not merge into `main` or `master` without explicit user permission.

