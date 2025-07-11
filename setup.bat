@echo off
REM SRT Timestamp Fixer - Quick Setup Script

echo SRT Timestamp Fixer - Quick Setup
echo ==================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Then run this script again.
    pause
    exit /b 1
)

echo ✅ Python found

echo 📦 Installing dependencies...
cd src
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully
) else (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Available options:
echo   1. GUI Application:  launch_gui.bat
echo   2. Web Application:  launch_web.bat
echo   3. Build Executables: build_executables.bat
echo.
echo For detailed usage instructions, see USER_GUIDE.md
echo.
pause
