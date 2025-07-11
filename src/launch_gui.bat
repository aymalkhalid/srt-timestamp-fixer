@echo off
REM SRT Timestamp Fixer - Desktop GUI Launcher (Windows)
echo Starting SRT Timestamp Fixer GUI...
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

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed or not in PATH
    echo Please install pip for Python
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "__pycache__" (
    if exist "requirements.txt" (
        echo Installing required packages...
        pip install -r requirements.txt
    ) else (
        echo Warning: requirements.txt not found. Skipping package installation.
    )
)

REM Check if srt_fixer_gui.py exists
if not exist "srt_fixer_gui.py" (
    echo Error: srt_fixer_gui.py not found in this directory.
    pause
    exit /b 1
)

REM Launch the GUI application
python srt_fixer_gui.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error. Press any key to exit.
    pause
)
