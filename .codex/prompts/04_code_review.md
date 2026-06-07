# Code Review Prompt

Use this prompt to review changes before merge or PR.

## Review Stance

Prioritize bugs, regressions, missing tests, security issues, and architecture risks. Findings must come first and be ordered by severity.

## Checklist

Review for:

- architecture and responsibility boundaries;
- readability and maintainability;
- type safety;
- useful dataclasses or pydantic models for schemas;
- error handling and logging;
- absence of unnecessary long `if` / `else` strategy chains;
- absence of hardcoded operational parameters;
- config-driven behavior;
- testability;
- security and secret handling;
- performance and memory risks;
- data loading, preprocessing, retrieval, generation, and evaluation separation;
- compliance with the Data Science pipeline;
- compliance with the RAG pipeline;
- rollback clarity.

## Required Output

Findings:

- `severity` `file:line` description and impact.

Open Questions:

- Questions that affect correctness or merge readiness.

Test Gaps:

- Missing checks or weak coverage.

Summary:

- Short context only after findings.

