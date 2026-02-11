@echo off
echo FCTC Exam Automation System - Setup and Run Script
echo ================================================

echo.
echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo.
echo Step 2: Installing required packages...
cd backend
python -m pip install --upgrade pip
python -m pip install flask flask-cors pandas openpyxl

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Step 3: Creating required directories...
if not exist "..\uploads" mkdir "..\uploads"
if not exist "..\outputs\master" mkdir "..\outputs\master"
if not exist "..\outputs\department" mkdir "..\outputs\department"
if not exist "..\outputs\division" mkdir "..\outputs\division"
if not exist "..\logs" mkdir "..\logs"

echo.
echo Step 4: Starting the Flask application...
echo.
echo ================================================
echo  FCTC Exam Automation System is starting...
echo  Open your browser and go to: http://localhost:5000
echo ================================================
echo.

python app.py