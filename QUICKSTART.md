# Decidely.so Quick Start Guide

Get Decidely.so running in your Slack workspace in 5 minutes!

## 1. Create Slack App (2 minutes)

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From an app manifest"**
3. Select your workspace
4. Delete the default YAML and paste this JSON:

```json
{
  "_metadata": {
      "major_version": 1,
      "minor_version": 1
  },
  "display_information": {
      "name": "decidely.so",
      "description": "Track decision-making patterns in your team",
      "background_color": "#2c2d30"
  },
  "features": {
      "bot_user": {
          "display_name": "Decidely Bot",
          "always_online": true
      },
      "slash_commands": [
          {
              "command": "/decidely",
              "description": "Report a decision situation / Reportar una situación de decisión",
              "usage_hint": "[authority|initiative|autoridad|iniciativa] <description>",
              "should_escape": false
          },
          {
              "command": "/decidely-list",
              "description": "List all decision reports",
              "should_escape": false
          }
      ]
  },
  "oauth_config": {
      "scopes": {
          "bot": [
              "channels:history",
              "chat:write",
              "commands"
          ]
      }
  },
  "settings": {
      "event_subscriptions": {
          "bot_events": []
      },
      "interactivity": {
          "is_enabled": true
      },
      "org_deploy_enabled": true,
      "socket_mode_enabled": true,
      "token_rotation_enabled": false
  }
}
```

5. Click **"Create"**

## 2. Get Your Tokens (1 minute)

### App Token:
1. Go to **"Socket Mode"** → Enable it
2. Click **"Generate"** → Name: `decidely-token` → Add scope: `connections:write`
3. **Copy the token** (starts with `xapp-`)

### Bot Token:
1. Go to **"OAuth & Permissions"** → **"Install to Workspace"**
2. **Copy the Bot User OAuth Token** (starts with `xoxb-`)

## 3. Set Up the Bot (2 minutes)

```bash
# Clone and enter directory
git clone https://github.com/your-org/decidely.so.git
cd decidely.so

# Install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Configure tokens
cp .env.example .env
# Edit .env and add your tokens:
# SLACK_BOT_TOKEN=xoxb-your-token
# SLACK_APP_TOKEN=xapp-your-token

# Start the bot
./start.sh  # or ./start.fish for Fish shell
```

## 4. Test It!

In any Slack channel:

### Quick report:
```
/decidely authority couldn't approve the budget increase
```

### Spanish:
```
/decidely autoridad no pude aprobar el presupuesto
```

### Open form:
```
/decidely
```

### List reports:
```
/decidely-list
```

## Common Issues

**Bot not responding?**
- Check Socket Mode is enabled
- Verify tokens in `.env`
- Check console for errors

**Commands not showing?**
- Refresh Slack (Cmd/Ctrl + R)
- Wait 1-2 minutes for Slack to update

## Next Steps

- Read [INSTALLATION.md](INSTALLATION.md) for detailed setup
- Check [docs/LOCALIZATION.md](docs/LOCALIZATION.md) for language support
- Use SQLite for persistent storage (see INSTALLATION.md)