# Project Workflow

This project uses a controlled Codex workflow:

1. Big step planning
2. Small substep execution
3. Validation
4. Report
5. Decision to continue, retry, or stop

## Big Step

A big step changes a project capability or engineering stage, such as EDA, preprocessing, baseline RAG, retrieval evaluation, API, UI, or QLoRA planning.

Before implementation, define:

- goal;
- why it matters;
- scope;
- ignored files;
- substeps;
- expected result;
- quality gates;
- rollback plan;
- required approval.

## Small Substep

A small substep must be scoped to a small set of files and produce a verifiable result.

Each substep must include:

- mini-plan;
- changes;
- checks;
- short report.

## Root Mode

From the repository root, Codex works only with:

- `AGENTS.md`
- `.codex/`
- `docs/`
- `docs/project_control/`
- `docs/mcp/`
- `docs/references/`

Anything outside that scope requires explicit user permission.

## Current Stage

The current stage is project-control setup only. Do not start EDA, preprocessing, RAG, QLoRA, API, or UI work during this stage.

