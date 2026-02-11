@echo off
title FCTC Exam Automation System
color 0A

echo.
echo  ███████╗ ██████╗████████╗ ██████╗ 
echo  ██╔════╝██╔════╝╚══██╔══╝██╔════╝ 
echo  █████╗  ██║        ██║   ██║      
echo  ██╔══╝  ██║        ██║   ██║      
echo  ██║     ╚██████╗   ██║   ╚██████╗ 
echo  ╚═╝      ╚═════╝   ╚═╝    ╚═════╝ 
echo.
echo  EXAM AUTOMATION SYSTEM - v1.0
echo  ================================
echo.
echo  [1] Starting Flask Server...
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed or not in PATH
    echo  Please install Python 3.7+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo  [2] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo  Installing required packages...
    pip install -r backend/requirements.txt
)

echo  [3] Starting application...
echo.
echo  ✓ Server will start at: http://127.0.0.1:5000
echo  ✓ Press Ctrl+C to stop the server
echo.

python backend/app.py