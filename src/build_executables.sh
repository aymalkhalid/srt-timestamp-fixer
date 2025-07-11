#!/bin/bash
# SRT Timestamp Fixer - Build Executables Script (Linux/macOS)

echo "SRT Timestamp Fixer - Executable Builder"
echo "========================================"
echo

# Change to the script directory
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python from https://python.org"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "Installing build dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt

echo
echo "Building GUI executable..."
$PYTHON_CMD -m PyInstaller --clean --onefile srt_fixer_gui.spec

echo
echo "Building Web App executable..."
$PYTHON_CMD -m PyInstaller --clean --onefile srt_fixer_web.spec

echo
echo "Build completed!"
echo "Executables are in the 'dist' folder:"
echo "  - SRT_Timestamp_Fixer_GUI"
echo "  - SRT_Timestamp_Fixer_Web"
echo

# Create a simple test
if [ -f "dist/SRT_Timestamp_Fixer_GUI" ]; then
    echo "GUI executable created successfully!"
else
    echo "Warning: GUI executable not found"
fi

if [ -f "dist/SRT_Timestamp_Fixer_Web" ]; then
    echo "Web executable created successfully!"
else
    echo "Warning: Web executable not found"
fi

echo
echo "You can now distribute the executables without requiring Python installation."
