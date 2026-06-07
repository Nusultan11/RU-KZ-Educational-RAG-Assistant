# Big Step Planner Prompt

Use this prompt before any substantial change.

## Instruction

Plan the big step before editing files. Do not start implementation until scope, risks, quality gates, and rollback are clear. If user approval is required, ask for it before code changes.

## Required Output

Big Step:

- Name the big step.

Goal:

- State the problem being solved.

Why:

- Explain why this step matters for the project.

Scope:

- List files and folders that may be opened or changed.

Ignore:

- List files and folders that must not be opened or changed.

Substeps:

- Break the big step into small verifiable substeps.

Expected Result:

- Describe the concrete result that should exist when the step is done.

Quality Gates:

- List formatting, linting, typing, tests, smoke checks, secret checks, and documentation checks that apply.

Rollback:

- Explain how to revert the step safely.

User Approval:

- State whether approval is required before implementation, branch creation, commit, PR, merge, or push.

