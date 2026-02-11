@echo off
echo ========================================
echo FCTC Tool - Git Push Script
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

echo Step 5: Committing...
git commit -m "FCTC Tool with automatic header detection, case-insensitive matching, and flexible field extraction"
echo.

echo Step 6: Checking current branch...
git branch
echo.

echo Step 7: Renaming branch to main...
git branch -M main
echo.

echo Step 8: Pushing to GitHub...
git push -u origin main --force
echo.

echo ========================================
echo Push Complete!
echo Repository: https://github.com/PranavYehale/FCTC-TOOL
echo ========================================
pause
