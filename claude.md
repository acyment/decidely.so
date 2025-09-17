# Python Slack Bot TDD Development Guide for MVP

## 🚨 CRITICAL RULE: TEST AFTER EVERY CHANGE

**Run `uv run pytest` after EVERY code modification. No exceptions.**

## Core TDD Cycle - MANDATORY

### 🔴 RED Phase

1. **PROPOSE TEST FIRST**: Show test to user for approval
2. Write test file only after approval
3. Run test to confirm it fails

### 🟢 GREEN Phase

1. Write MINIMUM code to pass test
2. Apply YAGNI ruthlessly
3. Run `uv run pytest`

### 🔵 REFACTOR Phase

1. **PROPOSE REFACTORING FIRST**: Get user approval
2. Only refactor with green tests
3. Run `uv run pytest` after refactoring

## Project Guidelines

### Shell Scripts Guidelines
- All shell scripts should be done for fish, not bash

## Technology Stack

```toml
# pyproject.toml
[project]
name = "slack-bot-mvp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "slack-bolt>=1.19",
    "slack-sdk>=3.33",
    "python-dotenv>=1.0",
    "structlog>=24.4",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "pytest-mock>=3.14",
    "pytest-cov>=5.0",
    "black>=24.8",
    "ruff>=0.7",
    "mypy>=1.11",
]

[tool.uv]
dev-dependencies = [
    "ipython>=8.27",
]
```

[Rest of the original content remains unchanged]