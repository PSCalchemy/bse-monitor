#!/bin/bash
# Final Render.com Deployment Script

echo "🚀 BSE Monitor - Render.com Deployment"
echo "======================================"

echo ""
echo "📋 Step 1: GitHub Repository Setup"
echo ""

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found. Let's use it to create the repository..."
    
    # Check if user is logged in
    if gh auth status &> /dev/null; then
        echo "✅ GitHub CLI authenticated"
        
        # Create repository
        echo "Creating GitHub repository..."
        gh repo create bse-monitor --public --source=. --remote=origin --push
        
        if [ $? -eq 0 ]; then
            echo "✅ Repository created and code pushed!"
            echo ""
            echo "📋 Step 2: Deploy to Render.com"
            echo "1. Go to: https://render.com"
            echo "2. Sign up with GitHub"
            echo "3. Click 'New Web Service'"
            echo "4. Connect your GitHub repository"
            echo "5. Select the bse-monitor repository"
            echo "6. The render.yaml file will auto-configure everything!"
            echo "7. Click 'Create Web Service'"
            echo ""
            echo "🎉 Your BSE Monitor will be running 24/7 in the cloud!"
            echo "📧 Email alerts will be sent to: 9ranjal@gmail.com"
            exit 0
        else
            echo "❌ Failed to create repository with GitHub CLI"
        fi
    else
        echo "⚠️  GitHub CLI not authenticated. Please run: gh auth login"
    fi
fi

# Fallback to manual process
echo "📋 Manual GitHub Repository Setup"
echo ""

echo "Please follow these steps:"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: bse-monitor"
echo "3. Make it public"
echo "4. Don't initialize with README"
echo "5. Click 'Create repository'"
echo ""

read -p "Have you created the GitHub repository? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please enter your GitHub username:"
    read github_username
    
    if [ -z "$github_username" ]; then
        echo "❌ GitHub username cannot be empty. Please run the script again."
        exit 1
    fi
    
    echo "Adding remote origin..."
    git remote add origin https://github.com/$github_username/bse-monitor.git
    
    echo "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Code pushed to GitHub successfully!"
        echo ""
        echo "📋 Step 2: Deploy to Render.com"
        echo "1. Go to: https://render.com"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Select the bse-monitor repository"
        echo "6. The render.yaml file will auto-configure everything!"
        echo "7. Click 'Create Web Service'"
        echo ""
        echo "🎉 Your BSE Monitor will be running 24/7 in the cloud!"
        echo "📧 Email alerts will be sent to: 9ranjal@gmail.com"
        echo ""
        echo "🔗 Your repository URL: https://github.com/$github_username/bse-monitor"
    else
        echo "❌ Failed to push to GitHub. Please check your repository URL and try again."
    fi
else
    echo "❌ Please create the GitHub repository first, then run this script again."
fi 