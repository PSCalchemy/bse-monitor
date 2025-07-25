#!/usr/bin/env python3
"""
Railway Deployment for BSE Monitor
Free alternative to Google Cloud
"""

import os

def create_railway_config():
    """Create Railway configuration files"""
    
    # Railway.toml configuration
    railway_toml = """[build]
builder = "nixpacks"

[deploy]
startCommand = "python bse_monitor.py"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[[services]]
name = "bse-monitor"
"""
    
    with open('railway.toml', 'w') as f:
        f.write(railway_toml)
    print("✅ Created railway.toml")
    
    # Nixpacks configuration
    nixpacks_toml = """[phases.setup]
nixPkgs = ["python3", "python3Packages.pip"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "python bse_monitor.py"
"""
    
    with open('nixpacks.toml', 'w') as f:
        f.write(nixpacks_toml)
    print("✅ Created nixpacks.toml")
    
    # Procfile for Railway
    procfile = """web: python bse_monitor.py
"""
    
    with open('Procfile', 'w') as f:
        f.write(procfile)
    print("✅ Created Procfile")

def create_railway_deploy_script():
    """Create Railway deployment script"""
    script_content = """#!/bin/bash
# Railway Deployment Script for BSE Monitor

echo "🚀 Deploying BSE Monitor to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize Railway project
echo "🏗️  Initializing Railway project..."
railway init

# Set environment variables
echo "🔧 Setting environment variables..."
railway variables set SMTP_SERVER=smtp.gmail.com
railway variables set SMTP_PORT=587
railway variables set SMTP_USERNAME=9ranjal@gmail.com
railway variables set SMTP_PASSWORD=yhhw rxir wpow pxqh
railway variables set SENDER_EMAIL=9ranjal@gmail.com
railway variables set RECIPIENT_EMAILS=9ranjal@gmail.com

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo "✅ BSE Monitor deployed to Railway!"
echo "🌐 Check your Railway dashboard for the service URL"
echo "📊 Monitor logs: railway logs"
"""
    
    with open('deploy_railway.sh', 'w') as f:
        f.write(script_content)
    os.chmod('deploy_railway.sh', 0o755)
    print("✅ Created deploy_railway.sh")

def create_health_check():
    """Create health check endpoint"""
    health_content = '''#!/usr/bin/env python3
# Health check endpoint for Railway
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health_check():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
'''
    
    with open('health_check.py', 'w') as f:
        f.write(health_content)
    print("✅ Created health_check.py")

def main():
    """Create Railway deployment files"""
    print("🚂 Creating Railway Deployment")
    print("=" * 40)
    
    create_railway_config()
    create_railway_deploy_script()
    create_health_check()
    
    print("\n📋 Railway Deployment Steps:")
    print("1. Install Railway CLI: npm install -g @railway/cli")
    print("2. Run: ./deploy_railway.sh")
    print("3. Monitor will run 24/7 on Railway!")
    
    print("\n💡 Railway Benefits:")
    print("- 🆓 Free tier available")
    print("- 🚀 Easy deployment")
    print("- 📊 Built-in monitoring")
    print("- 🔄 Auto-restart on failure")
    print("- 🌐 Global CDN")

if __name__ == "__main__":
    main() 