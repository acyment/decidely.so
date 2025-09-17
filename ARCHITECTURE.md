# Decidely.so Slack Bot Architecture

## Overview
A Slack bot that helps teams track and discuss decision-making patterns by collecting reports on:
1. Situations where individuals lacked information/authority to decide
2. Situations where others were expected to decide but didn't

## Architecture Components

### 1. Slack Integration Layer
- **Slack SDK**: Using `slack-sdk` for Python
- **Event Handlers**: 
  - Slash commands: `/decidely report`, `/decidely list`
  - Interactive components: Buttons and dialogs
- **OAuth**: For workspace installation

### 2. Core Domain Models
- **Report**: Represents a decision situation
  - `id`: UUID
  - `user_id`: Slack user ID
  - `timestamp`: When reported
  - `type`: 'lacked_authority' | 'expected_initiative'
  - `description`: Detailed context
  - `workspace_id`: Slack workspace ID

### 3. Storage Layer
- **SQLite** for MVP (easily replaceable)
- **Repository Pattern** for data access abstraction

### 4. Business Logic
- **ReportService**: Handles report creation and retrieval
- **NotificationService**: Formats reports for Slack

### 5. API Layer
- **Flask** web framework
- Endpoints:
  - `/slack/events` - Slack event subscriptions
  - `/slack/commands` - Slash command handler
  - `/slack/interactive` - Interactive component handler

## Data Flow
1. User triggers slash command
2. Bot presents interactive dialog
3. User submits report
4. Report stored in database
5. Confirmation sent to user
6. Reports retrieved on demand

## Testing Strategy
- **Unit Tests**: For each component
- **Integration Tests**: Database and Slack API
- **E2E Tests**: Full user flows using Slack's testing tools