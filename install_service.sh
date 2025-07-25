#!/bin/bash
# Install BSE Monitor Service (macOS)

echo "🚀 Installing BSE Monitor Service..."

# Create logs directory
mkdir -p logs

# Copy service file to LaunchAgents
cp com.bse.monitor.plist ~/Library/LaunchAgents/

# Load the service
launchctl load ~/Library/LaunchAgents/com.bse.monitor.plist

echo "✅ BSE Monitor Service installed!"
echo "📊 Check status: launchctl list | grep bse"
echo "⏹️  Stop: launchctl unload ~/Library/LaunchAgents/com.bse.monitor.plist"
echo "🔄 Start: launchctl load ~/Library/LaunchAgents/com.bse.monitor.plist"
