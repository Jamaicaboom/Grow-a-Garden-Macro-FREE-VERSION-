#!/bin/bash
echo "🌱 Grow a Garden Macro - Linux/macOS Quick Start"
echo "========================================================"

# Change to script directory
cd "$(dirname "$0")"

echo "Checking if Python is available..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python3 found!"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Python found!"
else
    echo "❌ Python not found! Please install Python 3.7+ from https://python.org"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Checking if main.py exists..."
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found! Please run this script from the macro directory."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ main.py found!"

echo "Starting the macro..."
$PYTHON_CMD start_macro.py

read -p "Press Enter to exit..."