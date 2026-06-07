# Branch and Merge Workflow Prompt

Use this prompt when planning branches, commits, PRs, or merges.

## Branch Rules

- `main` and `master` must remain stable.
- Every substantial change should happen in a separate feature branch when the folder is a Git repository.
- Do not create commits, pushes, PRs, or merges without explicit user permission.

## Suggested Branch Names

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

## Merge Requirements

Merge into `main` or `master` only after:

- step report is complete;
- required checks pass;
- code review is complete;
- rollback plan is clear;
- user explicitly approves the merge.

## Prohibitions

- Do not automatically merge into `main` or `master`.
- Do not push or open PRs without confirmation.
- Do not hide failed or skipped checks.

## If Git Is Unavailable

If the directory is not a Git repository:

- report that branch checks were skipped;
- continue only with file-level scoped work;
- recommend initializing Git or moving the task into a repository before merge-oriented workflows.

