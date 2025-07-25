#!/usr/bin/env python3
"""
Render.com Deployment Setup for BSE Monitor
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

def create_health_endpoint():
    """Create a simple health check endpoint"""
    health_code = '''#!/usr/bin/env python3
"""
Health check endpoint for Render.com
"""
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_health_app():
    """Create a simple Flask app for health checks"""
    try:
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'service': 'BSE Monitor',
                'timestamp': datetime.now().isoformat(),
                'email': '9ranjal@gmail.com'
            })
        
        @app.route('/')
        def home():
            return jsonify({
                'message': 'BSE Monitor is running',
                'status': 'active',
                'email': '9ranjal@gmail.com'
            })
        
        return app
    except ImportError:
        # Fallback if Flask is not available
        return None

# Modify bse_monitor.py to include health endpoint
def modify_bse_monitor():
    """Add health endpoint to bse_monitor.py"""
    try:
        with open('bse_monitor.py', 'r') as f:
            content = f.read()
        
        # Check if health endpoint already exists
        if 'health' in content:
            print("✅ Health endpoint already exists in bse_monitor.py")
            return
        
        # Add Flask import and health endpoint
        flask_import = "from flask import Flask, jsonify\nfrom datetime import datetime\n"
        
        # Find the main section and add health endpoint
        if "if __name__ == \"__main__\":" in content:
            # Add Flask app creation before the main section
            health_app_code = '''
# Create Flask app for health checks
app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'BSE Monitor',
        'timestamp': datetime.now().isoformat(),
        'email': '9ranjal@gmail.com'
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'BSE Monitor is running',
        'status': 'active',
        'email': '9ranjal@gmail.com'
    })

# Run Flask app in background
import threading
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
'''
            
            # Insert the Flask code before the main section
            content = content.replace(
                "if __name__ == \"__main__\":",
                flask_import + health_app_code + "\nif __name__ == \"__main__\":"
            )
            
            with open('bse_monitor.py', 'w') as f:
                f.write(content)
            
            print("✅ Added health endpoint to bse_monitor.py")
        else:
            print("⚠️  Could not find main section in bse_monitor.py")
            
    except Exception as e:
        print(f"❌ Error modifying bse_monitor.py: {e}")

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

## Troubleshooting:
- If build fails, check the logs in Render dashboard
- Ensure all files are committed to GitHub
- Verify environment variables are set correctly
"""
    
    with open('RENDER_DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(guide)
    print("✅ Created RENDER_DEPLOYMENT_GUIDE.md")

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

def main():
    """Create Render deployment setup"""
    print("🎨 Creating Render.com Deployment Setup")
    print("=" * 50)
    
    create_render_yaml()
    modify_bse_monitor()
    create_deployment_guide()
    create_git_setup()
    
    print("\n📋 Render Deployment Files Created:")
    print("✅ render.yaml - Auto-configuration for Render")
    print("✅ bse_monitor.py - Updated with health endpoint")
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