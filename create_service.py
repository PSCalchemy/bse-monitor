#!/usr/bin/env python3
"""
System Service Setup for BSE Monitor
Run as a background service that starts automatically
"""

import os
import platform

def create_systemd_service():
    """Create systemd service file for Linux"""
    service_content = """[Unit]
Description=BSE Monitor Service
After=network.target

[Service]
Type=simple
User=pranjal
WorkingDirectory=/Users/pranjalsingh/nse project
Environment=PATH=/Users/pranjalsingh/nse project/venv/bin
ExecStart=/Users/pranjalsingh/nse project/venv/bin/python /Users/pranjalsingh/nse project/bse_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open('bse-monitor.service', 'w') as f:
        f.write(service_content)
    print("✅ Created systemd service file")

def create_launchd_service():
    """Create launchd service file for macOS"""
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bse.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/pranjalsingh/nse project/venv/bin/python</string>
        <string>/Users/pranjalsingh/nse project/bse_monitor.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/pranjalsingh/nse project</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/pranjalsingh/nse project/logs/bse-monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/pranjalsingh/nse project/logs/bse-monitor-error.log</string>
</dict>
</plist>
"""
    
    with open('com.bse.monitor.plist', 'w') as f:
        f.write(plist_content)
    print("✅ Created launchd service file")

def create_install_script():
    """Create installation script"""
    if platform.system() == "Darwin":  # macOS
        script_content = """#!/bin/bash
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
"""
    else:  # Linux
        script_content = """#!/bin/bash
# Install BSE Monitor Service (Linux)

echo "🚀 Installing BSE Monitor Service..."

# Copy service file to systemd
sudo cp bse-monitor.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable bse-monitor
sudo systemctl start bse-monitor

echo "✅ BSE Monitor Service installed!"
echo "📊 Check status: sudo systemctl status bse-monitor"
echo "⏹️  Stop: sudo systemctl stop bse-monitor"
echo "🔄 Start: sudo systemctl start bse-monitor"
"""
    
    with open('install_service.sh', 'w') as f:
        f.write(script_content)
    os.chmod('install_service.sh', 0o755)
    print("✅ Created install script")

def main():
    """Create service files"""
    print("🔧 Creating System Service")
    print("=" * 30)
    
    system = platform.system()
    print(f"🖥️  Detected OS: {system}")
    
    if system == "Darwin":  # macOS
        create_launchd_service()
        print("\n📋 macOS Service Commands:")
        print("1. Install: ./install_service.sh")
        print("2. Check status: launchctl list | grep bse")
        print("3. View logs: tail -f logs/bse-monitor.log")
        print("4. Stop: launchctl unload ~/Library/LaunchAgents/com.bse.monitor.plist")
        
    elif system == "Linux":
        create_systemd_service()
        print("\n📋 Linux Service Commands:")
        print("1. Install: ./install_service.sh")
        print("2. Check status: sudo systemctl status bse-monitor")
        print("3. View logs: sudo journalctl -u bse-monitor -f")
        print("4. Stop: sudo systemctl stop bse-monitor")
        
    else:
        print("❌ Unsupported OS. Use Docker option instead.")
        return
    
    create_install_script()
    
    print("\n💡 Benefits:")
    print("- Starts automatically on boot")
    print("- Runs in background")
    print("- Auto-restarts if it crashes")
    print("- No need to keep terminal open")

if __name__ == "__main__":
    main() 