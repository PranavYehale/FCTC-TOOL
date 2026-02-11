# Vercel Deployment - Manual Steps

## Current Status
✅ Vercel CLI is installed (version 50.15.1)
✅ Project is configured for Vercel deployment
✅ All files are ready in GitHub repository

## Deploy via Vercel Dashboard (EASIEST METHOD)

### Step 1: Go to Vercel Dashboard
Visit: https://vercel.com/dashboard

### Step 2: Sign In/Sign Up
- Use GitHub account for easy integration
- Or create new Vercel account

### Step 3: Import Project
1. Click **"New Project"**
2. Click **"Import Git Repository"**
3. Connect your GitHub account if not connected
4. Find and select: **`PranavYehale/FCTC-TOOL`**

### Step 4: Configure Project
- **Framework Preset:** Other
- **Root Directory:** `./` (default)
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)
- **Install Command:** `pip install -r requirements.txt`

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait for deployment to complete (2-3 minutes)
3. Get your live URL!

## Deploy via CLI (Alternative)

If you prefer command line:

```bash
# In project directory, run:
vercel

# Answer the prompts:
# ? Set up and deploy? → Y
# ? Which scope? → (select your account)
# ? Link to existing project? → N
# ? What's your project's name? → fctc-tool
# ? In which directory is your code located? → ./
```

## Expected Deployment URL
Your app will be available at:
`https://fctc-tool-[random-string].vercel.app`

## Post-Deployment Testing

Test these URLs after deployment:

1. **Home Page:** `https://your-app.vercel.app/`
2. **Health Check:** `https://your-app.vercel.app/health`
3. **Upload Form:** Test with sample Excel files

## Troubleshooting

### If deployment fails:

1. **Check Build Logs** in Vercel dashboard
2. **Verify Python version** (should use Python 3.9+)
3. **Check requirements.txt** for package compatibility

### Common Issues:

- **Import Errors:** Check file paths in `api/index.py`
- **Module Not Found:** Verify all dependencies in `requirements.txt`
- **Timeout:** Large Excel files may cause function timeouts

## Files Ready for Deployment:

✅ `vercel.json` - Vercel configuration
✅ `requirements.txt` - Python dependencies
✅ `api/index.py` - Entry point for Vercel
✅ `backend/app.py` - Modified for serverless
✅ `backend/logic.py` - Updated file handling
✅ All frontend files (HTML/CSS/JS)

## Next Steps After Deployment:

1. **Test the application** with sample files
2. **Add custom domain** (optional)
3. **Monitor performance** in Vercel dashboard
4. **Check function logs** for any issues

---

**RECOMMENDATION:** Use the **Vercel Dashboard method** as it's more reliable and provides better error feedback.

Visit: https://vercel.com/dashboard to start deployment!