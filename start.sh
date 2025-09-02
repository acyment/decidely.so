#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if required environment variables are set
if [ -z "$SLACK_BOT_TOKEN" ]; then
    echo "❌ Error: SLACK_BOT_TOKEN is not set"
    echo "Please copy .env.example to .env and add your tokens"
    exit 1
fi

if [ -z "$SLACK_APP_TOKEN" ]; then
    echo "❌ Error: SLACK_APP_TOKEN is not set"
    echo "Please copy .env.example to .env and add your tokens"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run: uv venv"
    exit 1
fi

# Start the bot
echo "🚀 Starting Decidely bot..."
uv run python app.py