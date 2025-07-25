#!/bin/bash
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
