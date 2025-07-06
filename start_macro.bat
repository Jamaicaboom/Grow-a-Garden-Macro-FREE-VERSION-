@echo off
echo 🌱 Grow a Garden Macro - Windows Quick Start
echo ========================================================

cd /d "%~dp0"

echo Checking if Python is available...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found!

echo Checking if main.py exists...
if not exist "main.py" (
    echo ❌ main.py not found! Please run this script from the macro directory.
    pause
    exit /b 1
)

echo ✅ main.py found!

echo Starting the macro...
python start_macro.py

pause