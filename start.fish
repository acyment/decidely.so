#!/usr/bin/env fish
# Start script for decidely.so bot

echo "🚀 Starting Decidely.so Bot..."

# Load .env first if it exists
if test -f .env
    echo "📄 Loading environment from .env file..."
    for line in (cat .env | grep -v '^#' | grep -v '^$')
        set -x (echo $line | cut -d= -f1) (echo $line | cut -d= -f2-)
    end
end

# Check if tokens are set (after potentially loading from .env)
if test -z "$SLACK_BOT_TOKEN"; or test -z "$SLACK_APP_TOKEN"
    echo "❌ Error: SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set"
    echo ""
    echo "Current environment:"
    echo "  SLACK_BOT_TOKEN: "(if test -n "$SLACK_BOT_TOKEN"; echo "Set (hidden)"; else; echo "Not set"; end)
    echo "  SLACK_APP_TOKEN: "(if test -n "$SLACK_APP_TOKEN"; echo "Set (hidden)"; else; echo "Not set"; end)
    echo ""
    echo "Please export your tokens:"
    echo "  set -x SLACK_BOT_TOKEN 'xoxb-your-bot-token'"
    echo "  set -x SLACK_APP_TOKEN 'xapp-your-app-token'"
    echo ""
    echo "Or create a .env file with:"
    echo "  SLACK_BOT_TOKEN=xoxb-your-bot-token"
    echo "  SLACK_APP_TOKEN=xapp-your-app-token"
    exit 1
end

# Run the bot
echo "⚡ Starting bot with Socket Mode..."
echo "📝 Commands available:"
echo "   /decidely - Report a decision situation"
echo "   /decidely-list - List all reports"
echo ""

uv run python app.py