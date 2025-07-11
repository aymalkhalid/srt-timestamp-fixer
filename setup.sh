#!/bin/bash
# SRT Timestamp Fixer - Quick Setup Script

echo "SRT Timestamp Fixer - Quick Setup"
echo "=================================="
echo

# Change to the script directory
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed or not in PATH"
    echo "Please install Python from https://python.org"
    echo "Then run this script again."
    exit 1
fi

echo "✅ Python found"

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "📦 Installing dependencies..."
cd src
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo
echo "🎉 Setup completed successfully!"
echo
echo "Available options:"
echo "  1. GUI Application:  ./src/launch_gui.sh"
echo "  2. Web Application:  ./src/launch_web.sh"
echo "  3. Build Executables: ./src/build_executables.sh"
echo
echo "For detailed usage instructions, see USER_GUIDE.md"
