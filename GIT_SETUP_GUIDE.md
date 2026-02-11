# Git Setup and Repository Push Guide

## Step 1: Install Git (Required)

### Download and Install Git
1. Go to: https://git-scm.com/download/win
2. Download Git for Windows
3. Run the installer with default settings
4. Restart your Command Prompt/PowerShell after installation

### Verify Git Installation
```bash
git --version
```

## Step 2: Configure Git (First Time Setup)

```bash
# Set your name and email (replace with your details)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

## Step 3: Initialize Repository and Push to GitHub

### Option A: Initialize New Repository
```bash
# Navigate to project directory
cd "D:\FCTC PROJECT"

# Initialize git repository
git init

# Add remote repository
git remote add origin https://github.com/sumityelmar07/FCTC-EXAM-PROJECT.git

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: FCTC Exam Automation System

- Complete Flask backend with Excel processing
- Modern web frontend with file upload
- Intelligent student matching (PRN + Roll fallback)
- Comprehensive report generation (Master, Department, Division)
- Data validation and error handling
- Automated setup scripts
- Complete documentation"

# Push to GitHub
git push -u origin main
```

### Option B: Clone and Replace (if repository exists)
```bash
# Clone the existing repository
git clone https://github.com/sumityelmar07/FCTC-EXAM-PROJECT.git temp_repo

# Copy our files to the cloned repository
# (You'll need to manually copy files or use robocopy)

# Navigate to cloned repository
cd temp_repo

# Add all changes
git add .

# Commit changes
git commit -m "Complete FCTC Exam Automation System implementation"

# Push changes
git push origin main
```

## Step 4: Automated Git Setup Script

I've created a script to automate this process once Git is installed.