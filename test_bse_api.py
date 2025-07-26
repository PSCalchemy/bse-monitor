#!/usr/bin/env python3
"""
Test script to find the correct BSE API endpoint for announcements
"""

import requests
import json
from datetime import datetime

# Possible API endpoints
API_ENDPOINTS = [
    "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w",
    "https://api.bseindia.com/BseIndiaAPI/api/Announcement/GetData",
    "https://api.bseindia.com/BseIndiaAPI/api/CorporateAnnouncement/GetData",
    "https://api.bseindia.com/BseIndiaAPI/api/Announcement/GetLatest",
    "https://api.bseindia.com/BseIndiaAPI/api/CorporateAnnouncement/GetLatest",
    "https://api.bseindia.com/BseIndiaAPI/api/Announcement/GetAll",
    "https://api.bseindia.com/BseIndiaAPI/api/CorporateAnnouncement/GetAll",
]

def test_api_endpoints():
    """Test different API endpoints to find the correct one"""
    print("🔍 Testing BSE API Endpoints")
    print("=" * 50)
    
    # Setup session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bseindia.com/corporates/ann.html',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })
    
    for endpoint in API_ENDPOINTS:
        print(f"\n📡 Testing: {endpoint}")
        try:
            response = session.get(endpoint, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 200:
                try:
                    # Try to parse as JSON
                    data = response.json()
                    print(f"   ✅ JSON Response: {type(data)}")
                    if isinstance(data, dict):
                        print(f"   Keys: {list(data.keys())[:5]}...")
                    elif isinstance(data, list):
                        print(f"   List length: {len(data)}")
                        if data:
                            print(f"   First item keys: {list(data[0].keys())[:5] if isinstance(data[0], dict) else 'Not dict'}...")
                except json.JSONDecodeError:
                    print(f"   📄 Text Response (first 200 chars): {response.text[:200]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"   ❌ Network error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

def test_with_parameters():
    """Test API with common parameters"""
    print(f"\n🔍 Testing API with Parameters")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bseindia.com/corporates/ann.html',
        'Accept': 'application/json, text/plain, */*',
    })
    
    # Common parameters
    params_variations = [
        {},
        {'page': 1},
        {'page': 1, 'size': 10},
        {'date': datetime.now().strftime('%Y-%m-%d')},
        {'type': 'all'},
        {'category': 'all'},
    ]
    
    base_endpoint = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w"
    
    for params in params_variations:
        print(f"\n📡 Testing: {base_endpoint} with params: {params}")
        try:
            response = session.get(base_endpoint, params=params, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ JSON Response: {type(data)}")
                    if isinstance(data, dict):
                        print(f"   Keys: {list(data.keys())[:5]}...")
                except json.JSONDecodeError:
                    print(f"   📄 Text Response (first 200 chars): {response.text[:200]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"   ❌ Network error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    test_with_parameters() 