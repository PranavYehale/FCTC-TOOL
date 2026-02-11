# Vercel Deployment Guide for FCTC Tool

## Files Created for Vercel Deployment

### 1. `vercel.json` - Vercel Configuration
- Configures Python runtime
- Sets up routing to Flask app
- Defines environment variables

### 2. `requirements.txt` - Python Dependencies
- Flask and required packages
- Pandas for Excel processing
- CORS support

### 3. `api/index.py` - Vercel Entry Point
- Entry point for Vercel serverless functions
- Imports the main Flask app

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy from project directory:**
   ```bash
   vercel
   ```

4. **Follow the prompts:**
   - Link to existing project? No
   - Project name: fctc-tool
   - Directory: ./
   - Override settings? No

### Option 2: Deploy via GitHub Integration

1. **Go to Vercel Dashboard:** https://vercel.com/dashboard
2. **Click "New Project"**
3. **Import from GitHub:** Select your repository `PranavYehale/FCTC-TOOL`
4. **Configure Project:**
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
5. **Click "Deploy"**

## Important Notes for Vercel

### Limitations:
1. **No File Storage:** Vercel is serverless, so uploaded files are temporary
2. **Function Timeout:** 30 seconds max execution time
3. **Memory Limit:** Limited memory for large Excel files

### Modifications Made:
1. **Temporary Directories:** Uses `tempfile` instead of local folders
2. **File Downloads:** Modified to work with serverless environment
3. **Path Handling:** Updated for Vercel's file structure

## Environment Variables (if needed)

If you need to set environment variables:

1. **In Vercel Dashboard:**
   - Go to Project Settings
   - Navigate to Environment Variables
   - Add any required variables

2. **Via CLI:**
   ```bash
   vercel env add VARIABLE_NAME
   ```

## Testing the Deployment

After deployment, test these endpoints:

1. **Home Page:** `https://your-app.vercel.app/`
2. **Health Check:** `https://your-app.vercel.app/health`
3. **File Processing:** Upload files via the web interface

## Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Check `requirements.txt` for correct package versions
   - Ensure all imports are available

2. **Runtime Errors:**
   - Check Vercel function logs
   - Verify file paths are correct

3. **Timeout Issues:**
   - Large Excel files may cause timeouts
   - Consider file size limits

### Logs:
- View logs in Vercel Dashboard under "Functions" tab
- Use `vercel logs` command for CLI access

## Post-Deployment

1. **Custom Domain:** Add custom domain in Vercel Dashboard
2. **Analytics:** Enable Vercel Analytics if needed
3. **Monitoring:** Set up monitoring for function performance

## Alternative: Railway/Render

If Vercel doesn't work well for this Flask app, consider:
- **Railway:** Better for Flask apps with file handling
- **Render:** Good Flask support with persistent storage
- **Heroku:** Traditional platform with file system access

## Files Modified for Vercel:
- ✅ `backend/app.py` - Updated for serverless environment
- ✅ `backend/logic.py` - Modified file handling
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Dependencies
- ✅ `api/index.py` - Entry point

The project is now ready for Vercel deployment! 🚀