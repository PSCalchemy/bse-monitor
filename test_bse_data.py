#!/usr/bin/env python3
"""
Test script to examine the actual BSE API data structure
"""

import requests
import json
from datetime import datetime

def examine_bse_data():
    """Examine the actual BSE API data structure"""
    print("🔍 Examining BSE API Data Structure")
    print("=" * 50)
    
    # Setup session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bseindia.com/corporates/ann.html',
        'Accept': 'application/json, text/plain, */*',
    })
    
    endpoint = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w"
    
    try:
        print(f"📡 Fetching: {endpoint}")
        response = session.get(endpoint, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Data type: {type(data)}")
        
        # Examine the structure
        print(f"\n📊 Data Structure:")
        print(f"   Keys: {list(data.keys())}")
        
        if 'Table' in data:
            table_data = data['Table']
            print(f"\n📋 Table Data:")
            print(f"   Type: {type(table_data)}")
            print(f"   Length: {len(table_data) if isinstance(table_data, list) else 'Not a list'}")
            
            if isinstance(table_data, list) and table_data:
                print(f"   First item keys: {list(table_data[0].keys())}")
                print(f"   First item: {json.dumps(table_data[0], indent=2)}")
                
                # Show first few announcements
                print(f"\n📢 First 3 Announcements:")
                for i, announcement in enumerate(table_data[:3]):
                    print(f"\n   Announcement {i+1}:")
                    for key, value in announcement.items():
                        print(f"     {key}: {value}")
        
        if 'Table1' in data:
            table1_data = data['Table1']
            print(f"\n📋 Table1 Data:")
            print(f"   Type: {type(table1_data)}")
            print(f"   Length: {len(table1_data) if isinstance(table1_data, list) else 'Not a list'}")
            
            if isinstance(table1_data, list) and table1_data:
                print(f"   First item: {json.dumps(table1_data[0], indent=2)}")
        
        # Save the data for inspection
        with open('bse_api_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved API data to 'bse_api_data.json'")
        
        return data
        
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    examine_bse_data() 