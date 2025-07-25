# 🎨 Render.com Deployment Guide

## Quick Deploy to Render.com

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account
3. Create a new account

### Step 2: Deploy from GitHub
1. Connect your GitHub repository
2. Select "New Web Service"
3. Choose your repository
4. Configure:
   - **Name**: `bse-monitor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bse_monitor.py`

### Step 3: Set Environment Variables
Add these in Render dashboard:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=9ranjal@gmail.com
SMTP_PASSWORD=yhhw rxir wpow pxqh
SENDER_EMAIL=9ranjal@gmail.com
RECIPIENT_EMAILS=9ranjal@gmail.com
```

### Step 4: Deploy
Click "Create Web Service" and wait for deployment.

## Benefits of Render.com:
- ✅ **Faster builds** than Railway
- ✅ **More reliable** free tier
- ✅ **Better documentation**
- ✅ **Auto-restart** on failure
- ✅ **Custom domains** available

## Alternative: Use the render.yaml file
Upload the `render.yaml` file to your repository and Render will auto-configure everything! 