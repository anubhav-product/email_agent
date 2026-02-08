#!/bin/bash
# Gmail Authorization Helper
# This script helps you authorize Gmail access in a dev container

echo "=== Gmail Authorization ==="
echo ""
echo "Since we're in a dev container, you need to authorize Gmail manually:"
echo ""
echo "1. The agent will show you a URL"
echo "2. Open that URL in your browser"
echo "3. Authorize the app"
echo "4. You'll be redirected to a URL starting with http://localhost"
echo "5. Copy the ENTIRE URL and paste it back"
echo ""
echo "Starting agent..."
echo ""

/workspaces/email_agent/.venv/bin/python /workspaces/email_agent/run_agent.py "$@" --gmail-drafts
