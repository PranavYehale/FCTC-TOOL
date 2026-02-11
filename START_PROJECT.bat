@echo off
echo.
echo ========================================
echo   FCTC EXAM AUTOMATION SYSTEM
echo ========================================
echo.
echo Starting Flask server...
echo.

cd /d "%~dp0"
python backend/app.py

echo.
echo Server stopped. Press any key to exit...
pause >nul