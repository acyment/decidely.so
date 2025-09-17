# Decidely.so Slack Bot

Decidely.so helps teams surface decision-making friction directly inside Slack. Team members log moments when they lacked authority or when initiative stalled. The bot aggregates those signals so retrospectives focus on concrete examples instead of gut feelings.

## What You Get
- Slash commands for capturing and reviewing decision reports in-channel
- Socket Mode bot that runs locally with no public ingress required
- Structured storage layer (SQLite by default) behind a repository interface
- Service layer that formats insight-rich summaries for Slack surfaces
- Comprehensive test suite covering models, repositories, listeners, and end-to-end flows

## Commands
| Command | Purpose |
|---------|---------|
| `/decidely` | Open a modal to submit a new decision report |
| `/decidely-list` | Post a workspace-wide summary with per-report detail |

Each report records the reporter, workspace, situation type (`lacked_authority` or `expected_initiative`), human-readable description, and UTC timestamp.

## Architecture Snapshot
```
app.py                 # Socket Mode entrypoint
listeners/             # Slack Bolt listeners grouped by surface
  commands/            # Slash command handlers
  views/               # Modal submissions
  actions/, events/, messages/, shortcuts/ # Additional surfaces
services/report_service.py   # Business logic & Slack-friendly formatting
models/report.py       # Immutable domain model with serialization helpers
repositories/          # Storage abstraction & SQLite implementation
tests/                 # Unit, listener, and e2e coverage
```
Supporting docs live in `ARCHITECTURE.md`, `DECIDELY_README.md`, and `SANDBOX_SETUP.md` if you need deeper dives.

## Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Slack workspace where you can install custom apps

## Install Dependencies
```bash
uv sync
```

## Configure Slack Credentials
Create a `.env` file (or export variables in your shell):
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-level-token
```
Socket Mode is required; follow `SANDBOX_SETUP.md` for manifest-based installation and token generation.

## Run the Bot
```bash
uv run python app.py
```
The helper script `start.fish` bootstraps the same flow for fish users, loading `.env` automatically and validating tokens.

## Populate Slash Commands (Optional Script)
Once your app is installed, you can seed slash commands via:
```bash
./setup_commands.fish
```
This script hits Slack's `commands.create` endpoint with the credentials from your environment.

## Testing
```bash
uv run pytest -v
```
Tests rely on the project root being on `PYTHONPATH`. When invoking outside of `uv`, export `PYTHONPATH=$(pwd)`.

## Project Conventions
- Code style enforced via `ruff` and `black` (see `.flake8` and `pyproject.toml`)
- Domain-first design keeps Bolt listeners thin while services handle behavior
- Repositories abstract storage; swap `SQLiteReportRepository` for another backend without touching listeners

## Deployment Notes
For production or multi-workspace distribution, run `app_oauth.py` behind a public HTTPS endpoint (ngrok or your reverse proxy) and wire OAuth callbacks per `SANDBOX_SETUP.md`.

## License
This project ships with the MIT License (`LICENSE`).
