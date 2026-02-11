# FCTC Exam Automation System - Setup Guide

## Quick Start (After Python Installation)

### Option 1: Automated Setup (Windows)

**Using Batch File:**
```bash
# Double-click on run_project.bat
# OR run in Command Prompt:
run_project.bat
```

**Using PowerShell:**
```powershell
# Right-click on setup_and_run.ps1 -> Run with PowerShell
# OR run in PowerShell:
.\setup_and_run.ps1
```

### Option 2: Manual Setup

1. **Install Python Dependencies:**
   ```bash
   cd backend
   python -m pip install flask flask-cors pandas openpyxl
   ```

2. **Create Required Directories:**
   ```bash
   mkdir uploads
   mkdir outputs\master
   mkdir outputs\department  
   mkdir outputs\division
   mkdir logs
   ```

3. **Run the Application:**
   ```bash
   cd backend
   python app.py
   ```

4. **Access the Application:**
   - Open your web browser
   - Go to: http://localhost:5000

## Prerequisites

### Install Python (Required)

**Windows:**
1. Download Python from: https://www.python.org/downloads/
2. Run the installer
3. ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation: Open Command Prompt and run `python --version`

**Alternative - Microsoft Store:**
1. Open Microsoft Store
2. Search for "Python 3.11"
3. Install the official Python package

## Usage Instructions

1. **Prepare Your Excel Files:**
   - **FCTC File**: Should contain columns like PRN, Roll, Name, Marks
   - **Roll Call File**: Should contain columns like PRN, Roll, Name, Division

2. **Upload and Process:**
   - Select FCTC Excel file
   - Select Roll Call Excel file
   - Choose academic year (I, II, III)
   - Click "Generate Report"

3. **Download Reports:**
   - Master Report: Complete student list
   - Department Reports: Organized by department
   - Division Reports: Organized by division

## Troubleshooting

### Python Not Found
```
Error: 'python' is not recognized as an internal or external command
```
**Solution:** Install Python and ensure "Add Python to PATH" is checked during installation.

### Module Not Found
```
Error: No module named 'flask'
```
**Solution:** Install dependencies using `python -m pip install flask flask-cors pandas openpyxl`

### Permission Denied
```
Error: Permission denied when creating directories
```
**Solution:** Run Command Prompt or PowerShell as Administrator.

### Port Already in Use
```
Error: Address already in use
```
**Solution:** 
- Close other applications using port 5000
- Or change the port in `backend/app.py`: `app.run(debug=True, port=5001)`

## File Structure After Setup

```
FCTC-Exam-Automation/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── logic.py            # Business logic
│   ├── utils.py            # Helper functions
│   └── requirements.txt    # Dependencies
├── frontend/
│   ├── templates/
│   │   └── index.html      # Web interface
│   └── static/
│       ├── style.css       # Styling
│       └── script.js       # Frontend logic
├── uploads/                # Temporary file uploads
├── outputs/                # Generated reports
│   ├── master/            # Master reports
│   ├── department/        # Department reports
│   └── division/          # Division reports
├── logs/                  # Application logs
├── run_project.bat        # Windows batch script
├── setup_and_run.ps1      # PowerShell script
└── README.md              # Documentation
```

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Ensure Python is properly installed
3. Verify all dependencies are installed
4. Check the console for error messages
5. Ensure Excel files have the required columns

## Next Steps

Once the application is running:
1. Test with sample Excel files
2. Verify report generation
3. Check output quality
4. Customize as needed for your institution

---

**Happy Processing!** 🎓📊