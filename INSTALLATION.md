# Decidely.so Installation Guide

This guide will walk you through installing Decidely.so in your Slack workspace.

## Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- A Slack workspace where you have admin privileges
- Git (for cloning the repository)

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/decidely.so.git
cd decidely.so
```

## Step 2: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From an app manifest"**
4. Select your workspace
5. Copy and paste the contents of `manifest.json` from this repository
6. Review the configuration and click **"Create"**

## Step 3: Configure Socket Mode

Socket Mode allows your app to connect to Slack without exposing a public URL.

1. In your app settings, go to **"Socket Mode"** (under Settings)
2. Toggle **"Enable Socket Mode"** to ON
3. Click **"Generate"** to create an app-level token
4. Name it `decidely-app-token` (or any name you prefer)
5. Add the scope `connections:write`
6. Click **"Generate"**
7. Copy the token (starts with `xapp-`) - you'll need it later

## Step 4: Install App to Workspace

1. Go to **"OAuth & Permissions"** (under Features)
2. Click **"Install to Workspace"**
3. Review the permissions and click **"Allow"**
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`) - you'll need it later

## Step 5: Configure OAuth Scopes (if needed)

The manifest should have already configured these, but verify you have:

- `chat:write` - Send messages as the bot
- `commands` - Add and respond to slash commands
- `users:read` - Access user profile information for localization

## Step 6: Set Up Environment Variables

1. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

2. Edit `.env` and add your tokens:

```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

## Step 7: Install Python Dependencies

Using uv (recommended):

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Step 8: Configure Slash Commands

The manifest should have created these automatically, but verify:

1. Go to **"Slash Commands"** (under Features)
2. You should see:
   - `/decidely` - Report a decision situation
   - `/decidely-list` - List all decision reports

If they're missing, add them manually:

### /decidely command:
- **Command**: `/decidely`
- **Request URL**: Leave empty (Socket Mode handles this)
- **Short Description**: Report a decision situation / Reportar una situación de decisión
- **Usage Hint**: `[authority|initiative|autoridad|iniciativa] <description>`

### /decidely-list command:
- **Command**: `/decidely-list`
- **Request URL**: Leave empty (Socket Mode handles this)
- **Short Description**: List all decision reports

## Step 9: Start the Bot

### Using Fish shell:
```fish
./start.fish
```

### Using Bash:
```bash
./start.sh
```

### Or directly with Python:
```bash
uv run python app.py
```

You should see:
```
⚡️ Bolt app is running!
```

## Step 10: Test the Installation

1. Open Slack and go to any channel
2. Type `/decidely` and press Enter
   - A form should appear to report a decision
3. Try the inline format: `/decidely authority couldn't approve budget`
   - You should get a confirmation message
4. Type `/decidely-list` to see all reports

## Troubleshooting

### Bot doesn't respond to commands

1. Check that Socket Mode is enabled in your app settings
2. Verify both tokens are correctly set in `.env`
3. Check the console for error messages
4. Ensure the bot is running (you should see "Bolt app is running!")

### "not_in_channel" error

This shouldn't happen with the current implementation, but if it does:
- The bot uses ephemeral messages that don't require channel membership
- No need to invite the bot to channels

### Commands don't appear in Slack

1. Refresh Slack (Cmd/Ctrl + R)
2. Check that commands are enabled in your app settings
3. Try reinstalling the app to your workspace

### Missing permissions

1. Go to **"OAuth & Permissions"**
2. Add any missing scopes
3. Click **"Reinstall to Workspace"**
4. Update the bot token in `.env`

## Production Deployment

For production use, consider:

1. **Use SQLite for persistence**: 
   - Modify `listeners/commands/decidely_list.py` to use `SQLiteReportRepository`
   - Set a database path in your environment

2. **Environment-specific settings**:
   - Use different `.env` files for dev/staging/prod
   - Set appropriate logging levels

3. **Process management**:
   - Use systemd, supervisor, or similar for auto-restart
   - Consider using Docker for containerization

4. **Monitoring**:
   - Set up error tracking (e.g., Sentry)
   - Monitor uptime with tools like UptimeRobot

## Security Considerations

1. **Never commit tokens**: 
   - Keep `.env` in `.gitignore`
   - Use environment variables in production

2. **Token rotation**:
   - Regularly rotate your Slack tokens
   - Update them in your deployment environment

3. **Access control**:
   - The bot only responds to slash commands
   - Reports are workspace-specific

## Support

- Create an issue in the repository for bugs
- Check `docs/LOCALIZATION.md` for language support
- Review `claude.md` for development guidelines