import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

logging.basicConfig(level=logging.DEBUG)

# Add debug logging for all events
def log_all_events(event, say, logger):
    logger.debug(f"📨 Received event: {event.get('type', 'unknown')}")
    logger.debug(f"Full event: {event}")

# Initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Register Listeners
register_listeners(app)

# Add catch-all event handler for debugging
app.event("")(log_all_events)

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
