#!/usr/bin/env python3
"""
Test script for BSE Monitor system
"""

import logging
import sys
from datetime import datetime

from config import *
from email_sender import EmailSender
from announcement_analyzer import AnnouncementAnalyzer
from xbrl_parser import XBRLParser

def test_email_configuration():
    """Test email configuration."""
    print("Testing email configuration...")
    
    email_sender = EmailSender()
    
    if not email_sender.recipient_emails:
        print("❌ No recipient emails configured!")
        return False
    
    print(f"✅ Found {len(email_sender.recipient_emails)} recipient(s)")
    
    # Test email sending
    success = email_sender.test_email_configuration()
    if success:
        print("✅ Email test successful!")
    else:
        print("❌ Email test failed!")
    
    return success

def test_analyzer():
    """Test announcement analyzer."""
    print("\nTesting announcement analyzer...")
    
    analyzer = AnnouncementAnalyzer()
    
    # Test announcement
    test_announcement = {
        'company': 'ABC Ltd.',
        'timestamp': '2025-01-25 13:05',
        'title': 'Quarterly Results - 300% increase in profits',
        'category': 'Financial Results',
        'announcement_text': 'ABC Ltd. announces quarterly results with 300% increase in profits. New order worth ₹150 crore from MoD received.',
        'financial_data': {
            'revenue': 5000000000,
            'profit': 750000000,
            'growth': 300
        }
    }
    
    analysis = analyzer.analyze(test_announcement)
    
    print(f"✅ Analysis completed:")
    print(f"   - Urgency Score: {analysis['urgency_score']:.2f}")
    print(f"   - Confidence Score: {analysis['confidence_score']:.2f}")
    print(f"   - Flags: {analysis['flags']}")
    print(f"   - Keywords: {analysis['keywords'][:5]}")
    print(f"   - Sentiment: {analysis['sentiment']}")
    
    return True

def test_xbrl_parser():
    """Test XBRL parser."""
    print("\nTesting XBRL parser...")
    
    parser = XBRLParser()
    
    # Sample XBRL content
    sample_xbrl = """
    <?xml version="1.0" encoding="UTF-8"?>
    <xbrl xmlns="http://www.xbrl.org/2003/instance">
        <context id="D-2024">
            <entity>
                <identifier scheme="http://www.bseindia.com">ABC123</identifier>
            </entity>
            <period>
                <startDate>2024-01-01</startDate>
                <endDate>2024-03-31</endDate>
            </period>
        </context>
        <unit id="INR">
            <measure>iso4217:INR</measure>
        </unit>
        <revenue contextRef="D-2024" unitRef="INR" decimals="0">5000000000</revenue>
        <profit contextRef="D-2024" unitRef="INR" decimals="0">750000000</profit>
        <announcementText>ABC Ltd. announces quarterly results with 300% increase in profits. New order worth ₹150 crore from MoD received.</announcementText>
    </xbrl>
    """
    
    parsed_data = parser.parse(sample_xbrl)
    
    print(f"✅ XBRL parsing completed:")
    print(f"   - Financial data: {len(parsed_data.get('financial_data', {}))} items")
    print(f"   - Dates: {parsed_data.get('dates', [])}")
    print(f"   - Amounts: {parsed_data.get('amounts', [])}")
    print(f"   - Percentages: {parsed_data.get('percentages', [])}")
    
    return True

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    required_vars = [
        'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 
        'SMTP_PASSWORD', 'SENDER_EMAIL', 'RECIPIENT_EMAILS'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(sys.modules['config'], var, None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing configuration variables: {missing_vars}")
        print("Please check your .env file and env_example.txt for required variables.")
        return False
    
    print("✅ Configuration loaded successfully")
    return True

def main():
    """Run all tests."""
    print("🧪 BSE Monitor System Tests")
    print("=" * 40)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    tests = [
        ("Configuration", test_configuration),
        ("Email Configuration", test_email_configuration),
        ("Analyzer", test_analyzer),
        ("XBRL Parser", test_xbrl_parser),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
    
    print("\n" + "=" * 40)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Run: python bse_monitor.py")
        print("2. Monitor the logs for any issues")
        print("3. Check your email for test alerts")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the monitor.")
    
    return passed == total

if __name__ == "__main__":
    main() 