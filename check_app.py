import os
from slack_sdk import WebClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

print("🔍 Checking app configuration...\n")

# Get app info
try:
    response = client.auth_test()
    print(f"✅ Bot authenticated as: {response['user']} (ID: {response['user_id']})")
    print(f"✅ Workspace: {response['team']} (ID: {response['team_id']})")
    print(f"✅ Bot ID: {response['bot_id']}")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)

print("\n📝 To add slash commands:")
print("1. Go to https://api.slack.com/apps")
print("2. Click on your app (decidely.so)")
print("3. Go to 'Slash Commands' in the left sidebar")
print("4. Click 'Create New Command' and add:")
print("   - Command: /decidely")
print("   - Request URL: (leave empty for Socket Mode)")
print("   - Short Description: Report a decision situation")
print("   - Click 'Save'")
print("")
print("5. Click 'Create New Command' again and add:")
print("   - Command: /decidely-list")
print("   - Request URL: (leave empty for Socket Mode)")
print("   - Short Description: List all decision reports")
print("   - Click 'Save'")
print("")
print("6. Reinstall the app to your workspace:")
print("   - Go to 'Install App' or 'OAuth & Permissions'")
print("   - Click 'Reinstall to Workspace'")
print("")
print("The commands should then appear in Slack!")