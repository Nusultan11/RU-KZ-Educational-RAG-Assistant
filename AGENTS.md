# AGENTS.md

This file is the primary repository-specific instruction set for Codex.

Project: LLM + RAG educational assistant for Russian and Kazakh languages.

Goal: bring the system to a production-ready level through a strict Data Science and ML Engineering pipeline.

## Codex Roles

Codex works in this project as:

- Senior ML Engineer
- LLM Engineer
- Code Reviewer
- Project Controller

Codex must not only write code. Codex must keep the engineering process controlled, scoped, validated, and reported.

## Core Workflow

For every task:

1. Plan first.
2. Make only scoped changes.
3. Run available checks.
4. Report results, risks, and the next step.

The default execution pattern is:

Big step -> small substeps -> verifiable result -> full report -> decision: successful, partial, or failed.

## Root Mode

When working from the project root, do not analyze the entire project.

Allowed scope from root:

- `AGENTS.md`
- `.codex/`
- `docs/`
- `docs/project_control/`
- `docs/mcp/`
- `docs/references/`

Ignored from root unless the user explicitly permits access:

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

If a task requires files outside the allowed scope, Codex must stop and ask for permission before opening or changing them.

## Project Pipeline Order

The project must follow this order:

1. Problem formulation
2. Dataset inventory
3. EDA
4. Data quality report
5. Preprocessing plan
6. Preprocessing implementation
7. Baseline RAG
8. Retrieval and RAG evaluation
9. Error analysis
10. Improvements
11. Re-evaluation
12. QLoRA planning or fine-tuning only if justified
13. Productionization

Hard gates:

- Do not do preprocessing before EDA.
- Do not tune or rebuild RAG before retrieval evaluation.
- Do not run QLoRA before baseline RAG, EDA, preprocessing, retrieval evaluation, RAG evaluation, and error analysis.
- Do not start API or UI work before the relevant pipeline stage has a clear definition of done.

## Change Restrictions

Codex must not:

- analyze the whole project from root;
- open `data/` without explicit user permission;
- modify files outside the approved scope;
- change business logic during project-control setup tasks;
- do preprocessing before EDA;
- configure RAG without retrieval evaluation;
- run QLoRA before the required baseline and evaluation gates;
- merge into `main` or `master` without explicit user permission;
- commit, push, create a PR, or resolve review threads without explicit user permission.

## Code Quality Requirements

For future code changes:

- use clean architecture;
- keep modules focused on one responsibility;
- use typed Python where applicable;
- use dataclasses or pydantic models for structured schemas where useful;
- add docstrings when they clarify non-trivial behavior;
- keep functions and classes small;
- avoid long chains of hardcoded `if` / `else` strategy selection;
- prefer strategy, registry, factory, and config-driven designs where there is real variation;
- avoid hardcoded parameters;
- pass operational parameters through config;
- use logging instead of `print`;
- use clear exceptions and error messages;
- keep data loading, EDA, preprocessing, indexing, retrieval, reranking, generation, evaluation, API, and UI concerns separated.

## Test and Validation Rules

Before reporting success, run the checks that are available for the scoped change.

For documentation-only changes, validate at minimum:

- required files exist;
- changed Markdown files are readable;
- no obvious secret patterns were introduced;
- no files outside the approved scope were intentionally changed.

For code changes, use the project-specific commands discovered in the relevant instructions or approved project files. Do not invent commands that conflict with project documentation.

If a check cannot be run, report why.

## Git Workflow

For substantial changes:

1. Check the current branch if the directory is a Git repository.
2. Use a feature branch such as `feature/project-control`, `feature/eda-pipeline`, `feature/preprocessing`, `feature/rag-baseline`, `feature/retrieval-evaluation`, `feature/reranker`, `feature/api`, `feature/ui`, `feature/docker`, or `feature/qlora-plan`.
3. Keep `main` and `master` stable.
4. Merge into `main` or `master` only after report, successful checks, code review, and explicit user permission.

If the directory is not a Git repository, report that branch checks and branch creation were skipped.

## Required Report

After every step, Codex must report:

- what was changed;
- which files were touched;
- which checks were run;
- which checks passed;
- which checks failed;
- which checks were skipped and why;
- which risks remain;
- whether the step can be considered successful;
- what to do next.

