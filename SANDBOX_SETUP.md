# Testing Decidely.so in a Slack Sandbox

## 1. Create a Slack Workspace (if needed)

- Go to https://slack.com/create
- Create a free workspace for testing

## 2. Create the Slack App

### Option A: Using the Manifest (Recommended)

1. Update the manifest.json to include our commands:

```json
{
    "display_information": {
        "name": "Decidely.so",
        "description": "Track decision-making patterns",
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
                "description": "Report a decision situation",
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
                "commands",
                "chat:write",
                "im:history",
                "im:read",
                "im:write"
            ]
        }
    },
    "settings": {
        "interactivity": {
            "is_enabled": true
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": true,
        "token_rotation_enabled": false
    }
}
```

2. Go to https://api.slack.com/apps/new
3. Choose "From an app manifest"
4. Select your test workspace
5. Paste the updated manifest
6. Create the app

### Option B: Manual Setup

1. Go to https://api.slack.com/apps
2. Click "Create New App" > "From scratch"
3. Name it "Decidely.so" and select your workspace
4. Enable Socket Mode under "Socket Mode" (needed for local development)
5. Add slash commands under "Slash Commands":
   - `/decidely` - "Report a decision situation"
   - `/decidely-list` - "List all decision reports"
6. Enable Interactivity under "Interactivity & Shortcuts"

## 3. Get Your Tokens

1. **Bot Token**: 
   
   - Go to "OAuth & Permissions"
   - Copy the "Bot User OAuth Token" (starts with `xoxb-`)

2. **App Token** (for Socket Mode):
   
   - Go to "Basic Information"
   - Under "App-Level Tokens", click "Generate Token and Scopes"
   - Add the `connections:write` scope
   - Name it "Socket Mode Token"
   - Copy the token (starts with `xapp-`)

## 4. Set Up Environment

```bash
# Create .env file
cat << EOF > .env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
EOF

# Or export directly
export SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
export SLACK_APP_TOKEN="xapp-your-app-token-here"
```

## 5. Run the Bot

```bash
# Make sure dependencies are installed
uv sync

# Start the bot
uv run python app.py
```

You should see:

```
⚡️ Bolt app is running!
```

## 6. Test the Commands

1. **Install the app to your workspace**:
   
   - In the Slack API dashboard, click "Install to Workspace"
   - Authorize the permissions

2. **Test in Slack**:
   
   - Open your test workspace
   - In any channel, type `/decidely`
   - You should see a modal popup to report a decision situation
   - Fill it out and submit
   - Type `/decidely-list` to see your reports

## 7. Testing Tips

### Quick Test Flow:

```
1. /decidely
   - Select "Lacked Authority/Information"
   - Enter: "Couldn't approve overtime for critical bug fix"
   - Submit

2. /decidely
   - Select "Expected Initiative"  
   - Enter: "Developer didn't fix obvious typo in error message"
   - Submit

3. /decidely-list
   - Should show summary with 2 total reports
   - Should list both reports with details
```

### Debugging:

- Check the terminal where you ran `app.py` for error messages
- Add `logging.basicConfig(level=logging.DEBUG)` for more details
- The bot uses in-memory storage, so reports are lost when you restart

### Common Issues:

- **"Invalid auth"**: Check your bot token
- **Commands not showing**: Make sure you installed the app to workspace
- **Modal not opening**: Check app token and Socket Mode is enabled
- **No response**: Ensure the bot is running and connected

## 8. Using ngrok for Webhooks (Alternative to Socket Mode)

If you prefer webhooks over Socket Mode:

```bash
# Install ngrok
brew install ngrok  # or download from ngrok.com

# Start your app on port 3000
uv run python app_oauth.py

# In another terminal, expose it
ngrok http 3000

# Use the HTTPS URL from ngrok in your Slack app settings
```

Then update your Slack app's Request URL to: `https://your-ngrok-url.ngrok.io/slack/events`