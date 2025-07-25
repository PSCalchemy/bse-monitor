#!/bin/bash
# Deploy to Render.com

echo "🚀 Deploying BSE Monitor to Render.com"
echo "======================================"

echo ""
echo "📋 Step 1: Create GitHub Repository"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: bse-monitor"
echo "3. Make it public"
echo "4. Don't initialize with README"
echo "5. Click 'Create repository'"
echo ""

read -p "Have you created the GitHub repository? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "✅ Great! Now let's push to GitHub..."
    
    # Get the repository URL
    echo ""
    echo "Please enter your GitHub username:"
    read github_username
    
    # Add remote and push
    git remote add origin https://github.com/$github_username/bse-monitor.git
    git push -u origin main
    
    echo ""
    echo "✅ Code pushed to GitHub!"
    echo ""
    echo "📋 Step 2: Deploy to Render.com"
    echo "1. Go to: https://render.com"
    echo "2. Sign up with GitHub"
    echo "3. Click 'New Web Service'"
    echo "4. Connect your GitHub repository"
    echo "5. Select the bse-monitor repository"
    echo "6. Configure:"
    echo "   - Name: bse-monitor"
    echo "   - Environment: Python 3"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python bse_monitor.py"
    echo "7. Click 'Create Web Service'"
    echo ""
    echo "🎉 Your BSE Monitor will be running 24/7 in the cloud!"
    echo "📧 Email alerts will be sent to: 9ranjal@gmail.com"
    
else
    echo "❌ Please create the GitHub repository first, then run this script again."
fi 