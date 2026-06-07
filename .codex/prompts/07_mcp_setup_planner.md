# MCP Setup Planner Prompt

Use this prompt before enabling or changing MCP servers.

## Goal

MCP servers must help the project without weakening security or scope control.

## Required Analysis For Each MCP Server

For every proposed MCP server, document:

- why it is needed;
- which tools or resources it can access;
- which paths, repositories, or services it can reach;
- which risks it introduces;
- how access is limited;
- how to disable it;
- what secrets or environment variables are required.

Do not store secrets in the repository.

## Planned MCP Servers

1. `filesystem`
   - Purpose: safe project file work.
   - Restriction: no access to `data/`, `.git/`, `models/`, or `indexes/` without approval.
2. `git`
   - Purpose: read diff, status, and branches.
   - Restriction: no commit, merge, or push without user permission.
3. `github`
   - Purpose: pull requests, issues, and code review.
   - Restriction: no PR creation without confirmation.
4. `fetch`
   - Purpose: read official documentation and articles.
   - Restriction: use trusted sources.
5. `memory`
   - Purpose: store project decisions.
   - Restriction: no secrets, tokens, or personal data.
6. `sequential-thinking`
   - Purpose: plan large ML/RAG steps.
7. `context7`
   - Purpose: current library documentation.
8. `playwright`
   - Purpose: UI smoke tests for Streamlit, Gradio, or FastAPI docs.
9. `postgres` / `sqlite`
   - Purpose: metadata, feedback, and evaluation-result experiments.
10. `docker`
    - Purpose: containerization for API, vector DB, and UI.

## Required Output

MCP Plan:

- server name;
- purpose;
- permissions;
- restrictions;
- secrets policy;
- disable path;
- approval needed: yes / no.

