# Small Step Executor Prompt

Use this prompt to execute one approved small substep.

## Instruction

Work only with the specified files. Do not expand scope without approval.

## Required Flow

1. Mini-plan:
   - state the exact files to touch;
   - state the expected local result;
   - state the checks that will be run.
2. Change:
   - make only the scoped edit;
   - preserve unrelated content.
3. Validation:
   - run available checks for this substep;
   - if checks cannot run, explain why.
4. Short report:
   - summarize changed files;
   - summarize results;
   - state whether the substep is successful, partial, or failed.

## Stop Conditions

Stop and ask the user if:

- the requested file is outside scope;
- data, models, indexes, notebooks, logs, or `.git/` must be opened;
- business logic must change during a project-control-only task;
- required context is missing and guessing would be risky.

