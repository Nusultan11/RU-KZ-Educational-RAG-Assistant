# MCP Servers Plan

MCP servers may be useful for project work, but each server must have a clear purpose and restricted access.

## Planned Servers

| Server | Purpose | Key Restrictions |
| --- | --- | --- |
| `filesystem` | Safe work with approved project files | No access to `data/`, `.git/`, `models/`, or `indexes/` without approval |
| `git` | Read diff, status, and branches | No commit, merge, or push without user permission |
| `github` | PRs, issues, code review | No PR creation or mutation without confirmation |
| `fetch` | Read official docs and articles | Use trusted sources |
| `memory` | Store project decisions | No secrets, tokens, personal data, or raw dataset content |
| `sequential-thinking` | Plan large ML/RAG steps | Planning only; no file mutation |
| `context7` | Current library documentation | Use for library docs, not secrets |
| `playwright` | UI smoke tests | Local test targets only unless approved |
| `postgres` / `sqlite` | Metadata, feedback, evaluation results | Use local or approved databases only |
| `docker` | Containerization for API, vector DB, UI | No privileged containers without approval |

## Approval Checklist

Before enabling a new MCP server, document:

- why it is needed;
- which files, tools, or services it can access;
- whether it can write or mutate state;
- which environment variables it needs;
- how secrets are protected;
- how to disable it;
- what risk remains.

## Current Recommendation

Start with read-oriented and tightly scoped tools. Add write-capable MCP servers only after the project has clear quality gates and rollback procedures.

