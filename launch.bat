@echo off
echo.
echo ================================
echo   Claude AI Assistant Launcher
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ main.py not found. Please run this script from the AI_Assistant directory.
    pause
    exit /b 1
)

echo 🔍 Checking dependencies...

REM Check if virtual environment exists
if not exist "env" (
    echo 📦 Creating virtual environment...
    python -m venv env
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🚀 Activating virtual environment...
call env\Scripts\activate.bat

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

REM Check for .env file
if not exist ".env" (
    echo.
    echo ⚠️  No .env file found!
    echo.
    echo Please create a .env file with your Anthropic API key:
    echo ANTHROPIC_API_KEY=your_api_key_here
    echo.
    echo You can get an API key from: https://console.anthropic.com
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ All checks passed!
echo 🚀 Starting Claude AI Assistant...
echo.

REM Run the application
python main.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application exited with error code %errorlevel%
    pause
)

echo.
echo 👋 Thanks for using Claude AI Assistant!
pause
