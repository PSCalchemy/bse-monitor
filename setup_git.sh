#!/bin/bash
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
