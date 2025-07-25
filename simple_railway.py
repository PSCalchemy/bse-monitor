#!/usr/bin/env python3
"""
Simple Railway Deployment for BSE Monitor
Lightweight version without complex dependencies
"""

import os

def create_simple_requirements():
    """Create simplified requirements.txt"""
    requirements = """requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
schedule>=1.2.0
python-dotenv>=1.0.0
email-validator>=2.1.0
textblob>=0.17.1
flask>=2.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Updated requirements.txt")

def create_simple_procfile():
    """Create simple Procfile"""
    procfile = """web: python bse_monitor.py
"""
    
    with open('Procfile', 'w') as f:
        f.write(procfile)
    print("✅ Created simple Procfile")

def create_simple_deploy_script():
    """Create simple deployment script"""
    script_content = """#!/bin/bash
# Simple Railway Deployment

echo "🚀 Simple Railway Deployment for BSE Monitor"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize project (if not already done)
if [ ! -f ".railway" ]; then
    echo "🏗️  Initializing Railway project..."
    railway init
fi

# Set environment variables
echo "🔧 Setting environment variables..."
railway variables set SMTP_SERVER=smtp.gmail.com
railway variables set SMTP_PORT=587
railway variables set SMTP_USERNAME=9ranjal@gmail.com
railway variables set SMTP_PASSWORD="yhhw rxir wpow pxqh"
railway variables set SENDER_EMAIL=9ranjal@gmail.com
railway variables set RECIPIENT_EMAILS=9ranjal@gmail.com

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo "✅ BSE Monitor deployed to Railway!"
echo "🌐 Check your Railway dashboard for the service URL"
"""
    
    with open('simple_deploy.sh', 'w') as f:
        f.write(script_content)
    os.chmod('simple_deploy.sh', 0o755)
    print("✅ Created simple_deploy.sh")

def create_alternative_solutions():
    """Create alternative deployment solutions"""
    
    # Render.com deployment
    render_content = """# Render.com Deployment
# Alternative to Railway

services:
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
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_content)
    print("✅ Created render.yaml")
    
    # Heroku deployment
    heroku_content = """# Heroku Deployment
# Alternative to Railway

# Procfile
web: python bse_monitor.py

# Environment variables to set in Heroku dashboard:
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=9ranjal@gmail.com
# SMTP_PASSWORD=yhhw rxir wpow pxqh
# SENDER_EMAIL=9ranjal@gmail.com
# RECIPIENT_EMAILS=9ranjal@gmail.com
"""
    
    with open('heroku_deploy.md', 'w') as f:
        f.write(heroku_content)
    print("✅ Created heroku_deploy.md")

def main():
    """Create simple deployment files"""
    print("🚀 Creating Simple Railway Deployment")
    print("=" * 40)
    
    create_simple_requirements()
    create_simple_procfile()
    create_simple_deploy_script()
    create_alternative_solutions()
    
    print("\n📋 Simple Deployment Options:")
    print("1. 🚂 Railway (Simplified): ./simple_deploy.sh")
    print("2. 🎨 Render.com: Deploy using render.yaml")
    print("3. 🦸 Heroku: Follow heroku_deploy.md")
    print("4. 🐳 Docker: docker-compose up -d")
    
    print("\n💡 Quick Start:")
    print("1. Run: ./simple_deploy.sh")
    print("2. Or try Render.com (often faster than Railway)")
    print("3. Monitor will run 24/7 in the cloud!")

if __name__ == "__main__":
    main() 