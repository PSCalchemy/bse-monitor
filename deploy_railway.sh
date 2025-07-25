#!/bin/bash
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
