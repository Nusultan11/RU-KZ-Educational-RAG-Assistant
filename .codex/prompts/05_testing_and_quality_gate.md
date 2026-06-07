# Testing and Quality Gate Prompt

Use this prompt before declaring a step successful.

## Required Checks

Before success, check what applies:

- formatting;
- lint;
- type check;
- unit tests;
- integration tests, if available;
- smoke test;
- secret scan;
- absence of accidental changes in `data/`;
- absence of large binary files in Git;
- documentation updated for behavior changes;
- rollback plan exists.

## Documentation-Only Changes

For documentation-only work:

- verify required files exist;
- verify Markdown files are readable;
- run a scoped secret-pattern check;
- confirm no business logic was intentionally changed;
- explain why code tests were skipped.

## Reporting Rule

If any check cannot be run, state:

- command or check name;
- reason it was skipped;
- risk left by skipping it.

Do not mark a step successful if a required check failed and the risk is unresolved.

