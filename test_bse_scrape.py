#!/usr/bin/env python3
"""
Test script to directly scrape BSE website and analyze HTML structure
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

# BSE Configuration
BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"
BSE_BASE_URL = "https://www.bseindia.com"

def test_bse_scrape():
    """Test scraping the BSE announcements page"""
    print("🔍 Testing BSE Website Scraping")
    print("=" * 50)
    
    # Setup session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        print(f"📡 Fetching: {BSE_ANNOUNCEMENTS_URL}")
        response = session.get(BSE_ANNOUNCEMENTS_URL, timeout=30)
        response.raise_for_status()
        
        print(f"✅ Success! Status: {response.status_code}")
        print(f"📄 Content length: {len(response.text)} characters")
        print(f"🔗 Final URL: {response.url}")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"\n📊 HTML Analysis:")
        print(f"   Title: {soup.title.string if soup.title else 'No title'}")
        
        # Look for tables
        tables = soup.find_all('table')
        print(f"   Tables found: {len(tables)}")
        
        # Look for announcement-related content
        announcement_keywords = ['announcement', 'corporate', 'company', 'bse', 'stock']
        
        for i, table in enumerate(tables):
            print(f"\n📋 Table {i+1}:")
            rows = table.find_all('tr')
            print(f"   Rows: {len(rows)}")
            
            if rows:
                # Check first few rows
                for j, row in enumerate(rows[:3]):
                    cells = row.find_all(['td', 'th'])
                    cell_text = [cell.get_text(strip=True) for cell in cells]
                    print(f"   Row {j+1}: {len(cells)} cells - {cell_text[:3]}...")
        
        # Look for specific announcement patterns
        print(f"\n🔍 Looking for announcement patterns:")
        
        # Check for rows with announcement/corporate classes
        announcement_rows = soup.find_all('tr', class_=re.compile(r'announcement|corporate'))
        print(f"   Rows with announcement/corporate classes: {len(announcement_rows)}")
        
        # Check for any rows with multiple cells (potential announcements)
        all_rows = soup.find_all('tr')
        multi_cell_rows = [row for row in all_rows if len(row.find_all(['td', 'th'])) >= 3]
        print(f"   Rows with 3+ cells: {len(multi_cell_rows)}")
        
        # Look for company names (common patterns)
        company_patterns = [
            r'[A-Z]{2,}',  # All caps words (like RELIANCE, TCS)
            r'Ltd\.?',     # Limited companies
            r'Limited',    # Limited companies
            r'Corp',       # Corporation
        ]
        
        print(f"\n🏢 Looking for company names:")
        text_content = soup.get_text()
        for pattern in company_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                unique_matches = list(set(matches))[:10]  # First 10 unique matches
                print(f"   Pattern '{pattern}': {len(matches)} matches - {unique_matches}")
        
        # Check for recent timestamps
        print(f"\n🕐 Looking for timestamps:")
        timestamp_patterns = [
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}:\d{2}',        # HH:MM
        ]
        
        for pattern in timestamp_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                unique_matches = list(set(matches))[:5]  # First 5 unique matches
                print(f"   Pattern '{pattern}': {len(matches)} matches - {unique_matches}")
        
        # Save HTML for manual inspection
        with open('bse_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n💾 Saved HTML to 'bse_page.html' for manual inspection")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_bse_scrape() 