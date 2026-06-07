# MCP Security Rules

MCP servers receive tool access, so they must not be connected without restrictions.

## General Rules

- Do not store secrets in the repository.
- Tokens must be provided through environment variables.
- MCP filesystem access must not cover the whole computer.
- GitHub MCP must not push, merge, or create PRs without confirmation.
- Fetch MCP must use trusted sources.
- Memory MCP must not store secrets, tokens, personal data, or raw private datasets.
- Write-capable MCP servers require a rollback plan.

## Filesystem Rules

The filesystem server should be limited to the smallest required project paths.

Default denied without explicit approval:

- `data/`
- `.git/`
- `models/`
- `checkpoints/`
- `indexes/`
- `artifacts/`
- large binary files

## Required Record Before Enabling A Server

Before enabling any new MCP server, document:

- why it is needed;
- what rights it receives;
- what data it can access;
- what risks it introduces;
- how to disable it;
- who approved it.

## Secret Handling

Use placeholders in examples. Real values must stay outside the repository:

- `${GITHUB_TOKEN}`
- `${HF_TOKEN}`
- `${OPENAI_API_KEY}`
- `${DATABASE_URL}`

Never commit real token values.

