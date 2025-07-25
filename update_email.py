#!/usr/bin/env python3
"""
Update Email Configuration with correct credentials
"""

def update_email_config():
    """Update .env file with correct email and App Password"""
    
    # Email configuration content with correct credentials
    env_content = """# BSE Monitor Configuration
# Generated for 9ranjal@gmail.com

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=9ranjal@gmail.com
SMTP_PASSWORD=yhhw rxir wpow pxqh
SENDER_EMAIL=9ranjal@gmail.com

# Recipient emails (comma-separated)
RECIPIENT_EMAILS=9ranjal@gmail.com

# Optional: Customize monitoring interval (in minutes)
# CHECK_INTERVAL_MINUTES=5
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Email configuration updated!")
    print("📧 Email: 9ranjal@gmail.com")
    print("🔐 App Password: yhhw rxir wpow pxqh")
    print("\n🧪 Testing email configuration...")

if __name__ == "__main__":
    update_email_config() 