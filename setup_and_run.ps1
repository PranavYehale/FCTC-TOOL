# FCTC Exam Automation System - PowerShell Setup Script

Write-Host "FCTC Exam Automation System - Setup and Run Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Install packages
Write-Host ""
Write-Host "Step 2: Installing required packages..." -ForegroundColor Yellow
Set-Location backend

try {
    python -m pip install --upgrade pip
    python -m pip install flask flask-cors pandas openpyxl
    Write-Host "✓ All packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to install packages" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 3: Create directories
Write-Host ""
Write-Host "Step 3: Creating required directories..." -ForegroundColor Yellow
$directories = @("../uploads", "../outputs/master", "../outputs/department", "../outputs/division", "../logs")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Directory exists: $dir" -ForegroundColor Green
    }
}

# Step 4: Start the application
Write-Host ""
Write-Host "Step 4: Starting the Flask application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  FCTC Exam Automation System is starting..." -ForegroundColor Green
Write-Host "  Open your browser and go to: http://localhost:5000" -ForegroundColor Yellow
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Start the Flask app
python app.py