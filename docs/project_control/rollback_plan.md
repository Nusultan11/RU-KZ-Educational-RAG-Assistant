# Rollback Plan

Every substantial step must include a rollback plan.

## Documentation Rollback

For documentation-only changes:

1. Identify created and modified Markdown files.
2. Remove created files if the step is rejected.
3. Restore modified files from the previous approved state.
4. Re-run the scoped file-existence check.

## Code Rollback

For code changes:

1. Identify changed files.
2. Revert only the files touched by the step.
3. Remove generated artifacts created by the step.
4. Re-run tests that cover the affected behavior.
5. Report residual risks.

## Data Rollback

For data work:

1. Do not modify raw data in place.
2. Write processed outputs to versioned artifact paths.
3. Keep dataset inventory and transformation config.
4. Delete only generated outputs after verifying paths.

## Git Rollback

When the folder is a Git repository:

- prefer reverting scoped commits over rewriting shared history;
- do not use destructive Git commands without explicit user approval;
- do not merge or reset `main` / `master` without approval.

