#!/usr/bin/env python3
"""
Quick test script to demonstrate BSE Monitor functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from announcement_analyzer import AnnouncementAnalyzer
from xbrl_parser import XBRLParser
from datetime import datetime

def test_analyzer():
    """Test the announcement analyzer with sample data."""
    print("🧪 Testing Announcement Analyzer")
    print("=" * 40)
    
    analyzer = AnnouncementAnalyzer()
    
    # Sample announcement data
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
    
    print(f"📊 Analyzing announcement for: {test_announcement['company']}")
    print(f"📅 Time: {test_announcement['timestamp']}")
    print(f"📋 Title: {test_announcement['title']}")
    print(f"📄 Text: {test_announcement['announcement_text'][:100]}...")
    
    # Analyze the announcement
    analysis = analyzer.analyze(test_announcement)
    
    print("\n📈 Analysis Results:")
    print(f"   🚨 Urgency Score: {analysis['urgency_score']:.2f}")
    print(f"   ✅ Confidence Score: {analysis['confidence_score']:.2f}")
    print(f"   😊 Sentiment: {analysis['sentiment'].title()}")
    
    print(f"\n🏷️  Flags: {', '.join(analysis['flags'])}")
    print(f"🔍 Keywords: {', '.join(analysis['keywords'][:5])}")
    
    if analysis['key_metrics']:
        print(f"\n📊 Key Metrics:")
        for key, value in analysis['key_metrics'].items():
            print(f"   • {key}: {value}")
    
    return analysis

def test_xbrl_parser():
    """Test XBRL parser with sample data."""
    print("\n\n📄 Testing XBRL Parser")
    print("=" * 40)
    
    parser = XBRLParser()
    
    # Sample XBRL content
    sample_xbrl = """<?xml version="1.0" encoding="UTF-8"?>
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
</xbrl>"""
    
    print("📊 Parsing sample XBRL data...")
    parsed_data = parser.parse(sample_xbrl)
    
    print(f"✅ Parsing completed:")
    print(f"   📈 Financial data: {len(parsed_data.get('financial_data', {}))} items")
    print(f"   📅 Dates: {parsed_data.get('dates', [])}")
    print(f"   💰 Amounts: {parsed_data.get('amounts', [])}")
    print(f"   📊 Percentages: {parsed_data.get('percentages', [])}")
    
    if parsed_data.get('financial_data'):
        print(f"\n💰 Financial Data:")
        for key, value in parsed_data['financial_data'].items():
            print(f"   • {key}: {value}")
    
    return parsed_data

def test_web_scraping():
    """Test web scraping functionality."""
    print("\n\n🌐 Testing Web Scraping")
    print("=" * 40)
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        print("🔍 Testing connection to BSE website...")
        response = requests.get("https://www.bseindia.com/corporates/ann.html", timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully connected to BSE website")
            print(f"📄 Page size: {len(response.text)} characters")
            
            # Try to parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"🔍 Found {len(soup.find_all('table'))} tables on the page")
            
            # Look for announcement-related content
            announcement_elements = soup.find_all(text=lambda text: text and any(keyword in text.lower() for keyword in ['announcement', 'corporate', 'bse']))
            print(f"📢 Found {len(announcement_elements)} announcement-related text elements")
            
            return True
        else:
            print(f"❌ Failed to connect: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing web scraping: {e}")
        return False

def main():
    """Run all tests."""
    print("🔍 BSE Monitor - Quick Test")
    print("=" * 50)
    print(f"⏰ Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Analyzer
    analyzer_result = test_analyzer()
    
    # Test 2: XBRL Parser
    xbrl_result = test_xbrl_parser()
    
    # Test 3: Web Scraping
    web_result = test_web_scraping()
    
    # Summary
    print("\n\n📋 Test Summary")
    print("=" * 40)
    print(f"✅ Analyzer: Working (Urgency Score: {analyzer_result['urgency_score']:.2f})")
    print(f"✅ XBRL Parser: Working ({len(xbrl_result.get('financial_data', {}))} items parsed)")
    print(f"{'✅' if web_result else '❌'} Web Scraping: {'Working' if web_result else 'Failed'}")
    
    print("\n🎯 System Status:")
    if analyzer_result['urgency_score'] > 0.5 and web_result:
        print("🟢 READY: System is working correctly!")
        print("\nNext steps:")
        print("1. Configure email settings in .env file")
        print("2. Run: python start_monitor.py")
        print("3. Monitor logs for new announcements")
    else:
        print("🟡 PARTIAL: Some components need attention")
        print("\nIssues to address:")
        if analyzer_result['urgency_score'] <= 0.5:
            print("• Analyzer scoring needs adjustment")
        if not web_result:
            print("• Web scraping connectivity issues")
    
    return analyzer_result['urgency_score'] > 0.5 and web_result

if __name__ == "__main__":
    main() 