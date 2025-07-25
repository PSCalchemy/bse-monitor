#!/usr/bin/env python3
"""
Simple Email Setup for pranjal@gmail.com
"""

import os

def setup_email():
    """Set up email configuration for pranjal@gmail.com"""
    
    # Email configuration content
    env_content = """# BSE Monitor Configuration
# Generated for pranjal@gmail.com

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=pranjal@gmail.com
SMTP_PASSWORD=your_app_password_here
SENDER_EMAIL=pranjal@gmail.com

# Recipient emails (comma-separated)
RECIPIENT_EMAILS=pranjal@gmail.com

# Optional: Customize monitoring interval (in minutes)
# CHECK_INTERVAL_MINUTES=5
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Email configuration created for pranjal@gmail.com")
    print("\n📧 Next steps:")
    print("1. Get your Gmail App Password:")
    print("   - Go to: https://myaccount.google.com/apppasswords")
    print("   - Enable 2-Factor Authentication if not already enabled")
    print("   - Generate App Password for 'Mail'")
    print("   - Copy the 16-character password")
    print()
    print("2. Edit the .env file and replace 'your_app_password_here' with your actual App Password")
    print("   nano .env")
    print()
    print("3. Test the configuration:")
    print("   python test_monitor.py")
    print()
    print("4. Start monitoring:")
    print("   python start_monitor.py")

if __name__ == "__main__":
    setup_email() 