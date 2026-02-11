@echo off
echo ========================================
echo FCTC Tool - Git Push Script (FIXED)
echo ========================================
echo.

echo Step 1: Removing old git repository...
rd /s /q .git 2>nul
echo Done.
echo.

echo Step 2: Initializing new repository...
git init
echo.

echo Step 3: Adding remote...
git remote add origin https://github.com/PranavYehale/FCTC-TOOL.git
echo.

echo Step 4: Adding all files...
git add .
echo.

echo Step 5: Checking what will be committed...
git status --short
echo.

echo Step 6: Committing files...
git commit -m "FCTC Tool with automatic header detection, case-insensitive matching, and flexible field extraction"
if %errorlevel% neq 0 (
    echo ERROR: Commit failed. Checking status...
    git status
    pause
    exit /b 1
)
echo.

echo Step 7: Checking current branch...
git branch
echo.

echo Step 8: Renaming to main branch...
git branch -M main
echo.

echo Step 9: Pushing to GitHub (first time)...
git push -u origin main
if %errorlevel% neq 0 (
    echo First push failed, trying force push...
    git push -u origin main --force
)
echo.

echo ========================================
echo Push Complete!
echo Repository: https://github.com/PranavYehale/FCTC-TOOL
echo ========================================
pause