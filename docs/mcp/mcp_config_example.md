# MCP Config Example

This is a placeholder example. It is not an active configuration and contains no secrets.

Use environment variables for real credentials. Limit filesystem roots to the smallest required paths.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${PROJECT_ROOT}/AGENTS.md",
        "${PROJECT_ROOT}/.codex",
        "${PROJECT_ROOT}/docs"
      ]
    },
    "git": {
      "command": "mcp-server-git",
      "args": [
        "--repository",
        "${PROJECT_ROOT}"
      ],
      "env": {
        "MCP_GIT_READ_ONLY": "true"
      }
    },
    "github": {
      "command": "github-mcp-server",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "fetch": {
      "command": "mcp-server-fetch"
    },
    "memory": {
      "command": "mcp-server-memory",
      "env": {
        "MEMORY_NO_SECRETS": "true"
      }
    },
    "context7": {
      "command": "context7-mcp"
    },
    "playwright": {
      "command": "playwright-mcp",
      "env": {
        "PLAYWRIGHT_SCOPE": "local"
      }
    },
    "sqlite": {
      "command": "mcp-server-sqlite",
      "args": [
        "${PROJECT_ROOT}/artifacts/evaluation/example.sqlite"
      ]
    },
    "docker": {
      "command": "docker-mcp",
      "env": {
        "DOCKER_MCP_REQUIRE_APPROVAL": "true"
      }
    }
  }
}
```

Before using this example, replace commands with the exact installed MCP server commands and verify each server's permissions.

