@echo off
REM SRT Timestamp Fixer - Build Executables Script (Windows)

echo SRT Timestamp Fixer - Executable Builder
echo ========================================
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

echo Installing build dependencies...
pip install -r requirements.txt

echo.
echo Building GUI executable...
python -m PyInstaller --clean --onefile srt_fixer_gui.spec

echo.
echo Building Web App executable...
python -m PyInstaller --clean --onefile srt_fixer_web.spec

echo.
echo Build completed!
echo Executables are in the 'dist' folder:
echo   - SRT_Timestamp_Fixer_GUI.exe
echo   - SRT_Timestamp_Fixer_Web.exe
echo.

REM Create a simple test
if exist "dist\SRT_Timestamp_Fixer_GUI.exe" (
    echo GUI executable created successfully!
) else (
    echo Warning: GUI executable not found
)

if exist "dist\SRT_Timestamp_Fixer_Web.exe" (
    echo Web executable created successfully!
) else (
    echo Warning: Web executable not found
)

echo.
echo You can now distribute the executables without requiring Python installation.
echo.
pause
