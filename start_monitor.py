#!/usr/bin/env python3
"""
BSE Monitor Startup Script
Provides a user-friendly interface to start the monitoring system
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import requests
        import beautifulsoup4
        import schedule
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_configuration():
    """Check if configuration file exists."""
    if not os.path.exists('.env'):
        print("❌ Configuration file (.env) not found")
        print("Please copy env_example.txt to .env and configure your settings")
        return False
    
    print("✅ Configuration file found")
    return True

def run_tests():
    """Run system tests."""
    print("\n🧪 Running system tests...")
    try:
        result = subprocess.run([sys.executable, 'test_monitor.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_monitor():
    """Start the BSE monitor."""
    print("\n🚀 Starting BSE Monitor...")
    print("Press Ctrl+C to stop the monitor")
    print("-" * 50)
    
    try:
        # Import and run the monitor
        from bse_monitor import BSEMonitor
        monitor = BSEMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitor stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting monitor: {e}")

def main():
    """Main startup function."""
    print("🔍 BSE Corporate Announcement Monitor")
    print("=" * 50)
    
    # Check prerequisites
    if not check_dependencies():
        return
    
    if not check_configuration():
        return
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Run tests only")
    print("2. Start monitoring (with tests)")
    print("3. Start monitoring (skip tests)")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            run_tests()
            break
        elif choice == '2':
            if run_tests():
                start_monitor()
            break
        elif choice == '3':
            start_monitor()
            break
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main() 