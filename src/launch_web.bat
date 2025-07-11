@echo off
REM SRT Timestamp Fixer - Web Application Launcher (Windows)
echo Starting SRT Timestamp Fixer Web App...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "__pycache__" (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo Web server will start on: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Launch the web application
python srt_fixer_web.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error. Press any key to exit.
    pause
)
