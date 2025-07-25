#!/usr/bin/env python3
"""
Simple Render.com Setup for BSE Monitor
"""

import os

def create_render_yaml():
    """Create render.yaml for automatic deployment"""
    render_yaml = """services:
  - type: web
    name: bse-monitor
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bse_monitor.py
    envVars:
      - key: SMTP_SERVER
        value: smtp.gmail.com
      - key: SMTP_PORT
        value: 587
      - key: SMTP_USERNAME
        value: 9ranjal@gmail.com
      - key: SMTP_PASSWORD
        value: yhhw rxir wpow pxqh
      - key: SENDER_EMAIL
        value: 9ranjal@gmail.com
      - key: RECIPIENT_EMAILS
        value: 9ranjal@gmail.com
    healthCheckPath: /health
    autoDeploy: true
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_yaml)
    print("✅ Created render.yaml")

def create_git_setup():
    """Create git setup script"""
    git_script = """#!/bin/bash
# Git Setup for Render Deployment

echo "🚀 Setting up Git repository for Render deployment..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Initialized git repository"
fi

# Add all files
git add .

# Commit changes
git commit -m "BSE Monitor - Ready for Render deployment"

echo "✅ Git repository ready!"
echo ""
echo "📋 Next steps:"
echo "1. Create GitHub repository: https://github.com/new"
echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/bse-monitor.git"
echo "   git push -u origin main"
echo "3. Deploy to Render: https://render.com"
"""
    
    with open('setup_git.sh', 'w') as f:
        f.write(git_script)
    os.chmod('setup_git.sh', 0o755)
    print("✅ Created setup_git.sh")

def create_deployment_guide():
    """Create step-by-step deployment guide"""
    guide = """# 🎨 Render.com Deployment Guide

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
"""
    
    with open('RENDER_DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(guide)
    print("✅ Created RENDER_DEPLOYMENT_GUIDE.md")

def main():
    """Create Render deployment setup"""
    print("🎨 Creating Render.com Deployment Setup")
    print("=" * 50)
    
    create_render_yaml()
    create_deployment_guide()
    create_git_setup()
    
    print("\n📋 Render Deployment Files Created:")
    print("✅ render.yaml - Auto-configuration for Render")
    print("✅ RENDER_DEPLOYMENT_GUIDE.md - Step-by-step guide")
    print("✅ setup_git.sh - Git setup script")
    
    print("\n🚀 Quick Start:")
    print("1. Run: ./setup_git.sh")
    print("2. Create GitHub repository")
    print("3. Push to GitHub")
    print("4. Deploy to Render.com")
    print("5. Monitor will run 24/7 in the cloud!")
    
    print("\n💡 Why Render.com is better:")
    print("- 🚀 Faster builds than Railway")
    print("- 🔧 Simpler configuration")
    print("- 📊 Better monitoring")
    print("- 🆓 Reliable free tier")

if __name__ == "__main__":
    main() 