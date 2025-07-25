#!/usr/bin/env python3
"""
Simple Email Test for BSE Monitor
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_gmail_connection():
    """Test Gmail SMTP connection"""
    
    # Email settings from .env
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "9ranjal@gmail.com"
    password = "yhhw rxir wpow pxqh"
    sender_email = "9ranjal@gmail.com"
    recipient_email = "9ranjal@gmail.com"
    
    print("🧪 Testing Gmail Connection")
    print("=" * 40)
    print(f"📧 From: {sender_email}")
    print(f"📬 To: {recipient_email}")
    print(f"🔧 SMTP: {smtp_server}:{smtp_port}")
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🚨 BSE Monitor Test - " + datetime.now().strftime("%Y-%m-%d %H:%M")
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Simple text content
        text_content = f"""
BSE Monitor Test Email

This is a test email to verify your BSE Monitor configuration is working correctly.

✅ Email Configuration: Working
✅ SMTP Connection: Working
✅ Authentication: Working

Test completed at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

If you receive this email, your BSE Monitor is ready to send alerts!
"""
        
        msg.attach(MIMEText(text_content, 'plain'))
        
        # Connect and send
        print("🔌 Connecting to Gmail...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("🔐 Authenticating...")
            server.login(username, password)
            print("📤 Sending test email...")
            server.send_message(msg)
        
        print("✅ Test email sent successfully!")
        print("📧 Check your inbox at 9ranjal@gmail.com")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Make sure your App Password is correct")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    
    if success:
        print("\n🎉 Email configuration is working!")
        print("\nNext steps:")
        print("1. Run: python quick_test.py (test the full system)")
        print("2. Run: python start_monitor.py (start monitoring)")
    else:
        print("\n⚠️  Email configuration needs attention")
        print("Check your App Password and try again") 