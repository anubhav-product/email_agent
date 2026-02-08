#!/bin/bash

# 🚀 LeadFinder AI - SaaS Startup Script

echo "🚀 Starting LeadFinder AI (SaaS Version)..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env from template..."
    echo "HUNTER_API_KEY=your_hunter_api_key_here" > .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
    echo ""
    echo "✅ Created .env file. Please edit it with your API keys:"
    echo "   - HUNTER_API_KEY (get from hunter.io)"
    echo "   - OPENAI_API_KEY (get from platform.openai.com)"
    echo ""
fi

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from app_saas import app, db; app.app_context().push(); db.create_all(); print('✅ Database initialized')"

echo ""
echo "✨ Starting Flask app on http://localhost:5000"
echo ""
echo "📖 Quick Start:"
echo "   1. Open http://localhost:5000 in your browser"
echo "   2. Click 'Start Free - 5 Searches'"
echo "   3. Sign up with any email"
echo "   4. Start generating leads!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Flask app
python3 app_saas.py
