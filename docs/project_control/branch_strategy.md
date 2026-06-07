# Branch Strategy

## Stable Branches

`main` and `master` are stable branches. They must contain only reviewed and validated work.

## Feature Branches

Substantial changes should use feature branches when the folder is a Git repository.

Suggested branch names:

- `feature/project-control`
- `feature/eda-pipeline`
- `feature/preprocessing`
- `feature/rag-baseline`
- `feature/retrieval-evaluation`
- `feature/reranker`
- `feature/api`
- `feature/ui`
- `feature/docker`
- `feature/qlora-plan`

## Merge Rules

Merge into `main` or `master` only after:

- full step report;
- successful required checks;
- code review;
- rollback plan;
- explicit user permission.

## Prohibited Actions

- automatic merge into `main` or `master`;
- commit without user approval;
- push without user approval;
- PR creation without user confirmation;
- hiding failed or skipped checks.

## If Git Is Not Initialized

If the project directory is not a Git repository, branch checks and branch creation are skipped. Codex must report that limitation and continue only with scoped file changes.

