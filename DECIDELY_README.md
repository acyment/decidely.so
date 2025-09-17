# Decidely.so - Decision Tracking Slack Bot

A Slack bot that helps teams track and discuss decision-making patterns by collecting reports on:
- Situations where individuals lacked information/authority to decide
- Situations where others were expected to decide but didn't

This data can lead to productive conversations about delegation, authority, and initiative during retrospectives.

## Commands

### `/decidely` - Report a decision situation
Opens a dialog where you can:
- Select the type of situation (lacked authority/information or expected initiative)
- Describe the specific situation

### `/decidely-list` - View all reports
Shows a summary of all decision reports in your workspace, including:
- Total count of each type
- Detailed list of all reports with timestamps and descriptions

## MVP Architecture

The bot is built using:
- **Slack Bolt for Python** - Slack app framework
- **TDD approach** - All features developed test-first
- **In-memory storage** - Simple storage for MVP (easily replaceable)
- **Domain-driven design** - Clear separation of concerns

## Project Structure

```
decidely.so/
├── models/           # Domain models (Report, ReportType)
├── repositories/     # Data access layer
├── services/         # Business logic
├── listeners/        # Slack event handlers
│   ├── commands/     # Slash command handlers
│   └── views/        # Modal/view handlers
└── tests/           # Comprehensive test suite
    ├── unit/        # Unit tests for models, services, repositories
    ├── listeners/   # Tests for Slack handlers
    └── e2e/         # End-to-end tests
```

## Development

### Setup
```bash
# Install dependencies using uv
uv sync

# Run tests
PYTHONPATH=/Users/acyment/dev/decidely.so uv run pytest -v

# Start the bot
export SLACK_BOT_TOKEN=xoxb-your-token
export SLACK_APP_TOKEN=xapp-your-token
uv run python app.py
```

### Testing
- 20 unit tests covering models, repositories, and services
- 4 integration tests for Slack command handlers
- 5 E2E tests verifying the complete flow
- All tests passing with 100% coverage of core functionality

## Future Enhancements

- Persistent storage (PostgreSQL/SQLite)
- Report filtering by date range
- Export functionality (CSV/JSON)
- Analytics and insights
- Scheduled reminders for retrospectives
- Team-specific reporting