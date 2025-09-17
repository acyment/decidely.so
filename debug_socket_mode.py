import os
from slack_sdk import WebClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

print("🔍 Checking Socket Mode configuration...\n")

# Get app info
try:
    # Check app config
    response = client.api_call("apps.info", params={"app_id": os.environ.get("SLACK_APP_ID", "")})
    if response.get("ok"):
        print("✅ App info retrieved")
    else:
        print("ℹ️  Note: apps.info requires app_id which we don't have stored")
    
    # Test the app token
    app_client = WebClient(token=os.environ["SLACK_APP_TOKEN"])
    
    # This should work with app token
    test_response = app_client.api_call("apps.connections.open")
    if test_response.get("ok"):
        print("✅ App token is valid and can open connections")
        if "messages" in test_response.get("response_metadata", {}):
            for msg in test_response["response_metadata"]["messages"]:
                print(f"⚠️  {msg}")
    else:
        print("❌ App token test failed:", test_response.get("error"))
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📋 Troubleshooting steps:")
print("1. Go to https://api.slack.com/apps")
print("2. Click on your app (decidely.so)")
print("3. Go to 'Socket Mode' in the left sidebar")
print("4. Make sure Socket Mode is ENABLED (toggle should be ON)")
print("5. If it's already on, try turning it OFF and ON again")
print("6. Then go to 'Event Subscriptions' and make sure it's ENABLED")
print("7. Reinstall the app to your workspace")
print("\nIf Socket Mode shows as enabled but still doesn't work:")
print("- Go to 'Basic Information'")
print("- Scroll to 'App-Level Tokens'")
print("- Delete the existing token and create a new one with 'connections:write' scope")
print("- Update your .env file with the new SLACK_APP_TOKEN")