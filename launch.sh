#!/bin/bash

echo ""
echo "================================"
echo "   Claude AI Assistant Launcher"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this script from the AI_Assistant directory."
    exit 1
fi

echo "🔍 Checking dependencies..."

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv env
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source env/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo ""
    echo "Please create a .env file with your Anthropic API key:"
    echo "ANTHROPIC_API_KEY=your_api_key_here"
    echo ""
    echo "You can get an API key from: https://console.anthropic.com"
    echo ""
    exit 1
fi

echo ""
echo "✅ All checks passed!"
echo "🚀 Starting Claude AI Assistant..."
echo ""

# Run the application
python main.py

echo ""
echo "👋 Thanks for using Claude AI Assistant!"
