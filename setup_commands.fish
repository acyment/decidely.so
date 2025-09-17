#!/usr/bin/env fish
# Setup slash commands for decidely.so bot

echo "🔧 Setting up Decidely.so slash commands..."

# Load .env if it exists
if test -f .env
    echo "📄 Loading environment from .env file..."
    for line in (cat .env | grep -v '^#' | grep -v '^$')
        set -x (echo $line | cut -d= -f1) (echo $line | cut -d= -f2-)
    end
end

# Check if token is set
if test -z "$SLACK_BOT_TOKEN"
    echo "❌ Error: SLACK_BOT_TOKEN must be set"
    exit 1
end

echo "🚀 Creating slash commands..."

# Create /decidely command
echo "Creating /decidely command..."
set response1 (curl -s -X POST https://slack.com/api/commands.create \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "/decidely",
    "description": "Report a decision situation",
    "usage_hint": "Opens a form to report a decision situation"
  }')

if echo $response1 | grep -q '"ok":true'
    echo "✅ /decidely command created successfully"
else
    echo "❌ Failed to create /decidely command:"
    echo $response1 | python3 -m json.tool
end

# Create /decidely-list command
echo "Creating /decidely-list command..."
set response2 (curl -s -X POST https://slack.com/api/commands.create \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "/decidely-list",
    "description": "List all decision reports",
    "usage_hint": "Shows all decision reports for your workspace"
  }')

if echo $response2 | grep -q '"ok":true'
    echo "✅ /decidely-list command created successfully"
else
    echo "❌ Failed to create /decidely-list command:"
    echo $response2 | python3 -m json.tool
end

echo ""
echo "🎉 Setup complete! Now restart your bot and the commands should work."
echo "Note: It may take a minute for the commands to appear in Slack."