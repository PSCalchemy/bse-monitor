# 🎨 Render.com Deployment Guide

## Quick Deploy Steps:

### 1. Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial BSE Monitor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bse-monitor.git
git push -u origin main
```

### 2. Deploy to Render.com
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `bse-monitor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bse_monitor.py`

### 3. Environment Variables (Auto-configured via render.yaml)
The render.yaml file automatically sets:
- SMTP_SERVER=smtp.gmail.com
- SMTP_PORT=587
- SMTP_USERNAME=9ranjal@gmail.com
- SMTP_PASSWORD=yhhw rxir wpow pxqh
- SENDER_EMAIL=9ranjal@gmail.com
- RECIPIENT_EMAILS=9ranjal@gmail.com

### 4. Deploy
Click "Create Web Service" and wait for deployment.

## Benefits:
- ✅ **Faster builds** than Railway
- ✅ **More reliable** free tier
- ✅ **Auto-restart** on failure
- ✅ **Health checks** included
- ✅ **Custom domains** available

## Monitor Your Service:
- **Health Check**: https://your-app.onrender.com/health
- **Home Page**: https://your-app.onrender.com/
- **Logs**: Available in Render dashboard
