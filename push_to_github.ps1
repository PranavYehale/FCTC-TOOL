# PowerShell script to push FCTC project to GitHub

Write-Host "Cleaning up git repository..." -ForegroundColor Yellow

# Force remove .git directory
if (Test-Path .git) {
    Get-ChildItem -Path .git -Recurse -Force | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path .git -Force -Recurse -ErrorAction SilentlyContinue
}

Write-Host "Initializing new git repository..." -ForegroundColor Green
git init

Write-Host "Adding remote repository..." -ForegroundColor Green
git remote add origin https://github.com/PranavYehale/FCTC-TOOL.git

Write-Host "Adding required files..." -ForegroundColor Green

# Add backend files
git add backend/app.py
git add backend/logic.py
git add backend/utils.py
git add backend/__init__.py
git add backend/requirements.txt
git add backend/utils_modules/

# Add frontend files
git add frontend/

# Add documentation
git add .gitignore
git add README.md
git add CHANGELOG.md
git add CONTRIBUTING.md
git add LICENSE
git add SECURITY.md
git add SETUP_GUIDE.md
git add GIT_SETUP_GUIDE.md

# Add update documentation
git add FCTC_FIELD_EXTRACTION_UPDATE.md
git add COLUMN_NAME_FLEXIBILITY_UPDATE.md
git add CASE_INSENSITIVE_MATCHING_UPDATE.md
git add AUTOMATIC_HEADER_DETECTION_FIX.md

# Add scripts
git add QUICK_START.bat
git add run_project.bat
git add START_PROJECT.bat
git add setup_and_run.ps1

# Add directory structure
git add uploads/.gitkeep
git add logs/.gitkeep

Write-Host "Committing changes..." -ForegroundColor Green
git commit -m "Updated FCTC tool with automatic header detection, case-insensitive matching, and flexible field extraction

Features added:
- Automatic header row detection (handles headers in rows 0-9)
- Case-insensitive column name matching
- Flexible field extraction from FCTC files
- Support for multiple column name variations
- Enhanced error messages and logging"

Write-Host "Setting main branch..." -ForegroundColor Green
git branch -M main

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main --force

Write-Host "Done! Project pushed to https://github.com/PranavYehale/FCTC-TOOL" -ForegroundColor Cyan
