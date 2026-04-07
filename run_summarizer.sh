#!/bin/bash
# Incident Channel Summarizer Runner
# This script checks for required environment variables and runs the summarizer

set -e

echo "🔍 Incident Channel Summarizer"
echo "================================"
echo ""

# Check for required environment variables
MISSING_VARS=()

if [ -z "$SLACK_BOT_TOKEN" ] && [ -z "$SLACK_TOKEN" ]; then
    MISSING_VARS+=("SLACK_BOT_TOKEN or SLACK_TOKEN")
fi

if [ -z "$CONFLUENCE_USERNAME" ]; then
    MISSING_VARS+=("CONFLUENCE_USERNAME")
fi

if [ -z "$CONFLUENCE_API_TOKEN" ]; then
    MISSING_VARS+=("CONFLUENCE_API_TOKEN")
fi

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo "❌ Missing required environment variables:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "Please set these variables or create a .env file based on .env.example"
    echo ""
    echo "For Cursor Cloud Agents:"
    echo "  Add secrets at: https://cursor.com/settings → Cloud Agents → Secrets"
    echo ""
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import slack_sdk" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "✅ Configuration validated"
echo "🚀 Running summarizer..."
echo ""

# Run the summarizer
python3 incident_channel_summarizer.py

exit $?
