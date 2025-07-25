#!/usr/bin/env python3
"""
Test script to verify BSE Monitor web endpoints
"""

import requests
import json
import time
from datetime import datetime

def test_endpoint(url, endpoint_name):
    """Test a specific endpoint"""
    try:
        print(f"\n🔍 Testing {endpoint_name}: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {endpoint_name} - SUCCESS (Status: {response.status_code})")
            try:
                data = response.json()
                print(f"📊 Response: {json.dumps(data, indent=2)}")
                return True
            except json.JSONDecodeError:
                print(f"⚠️  Response is not JSON: {response.text[:200]}...")
                return False
        else:
            print(f"❌ {endpoint_name} - FAILED (Status: {response.status_code})")
            print(f"📄 Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint_name} - CONNECTION ERROR (Service may not be running)")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {endpoint_name} - TIMEOUT (Service may be starting up)")
        return False
    except Exception as e:
        print(f"❌ {endpoint_name} - ERROR: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 BSE Monitor Web Endpoints Test")
    print("=" * 50)
    
    # Get the service URL from user
    print("\n📋 Please enter your Render service URL:")
    print("   Example: https://bse-monitor-xxxxx.onrender.com")
    print("   (Get this from your Render dashboard)")
    
    base_url = input("\nEnter your service URL: ").strip()
    
    if not base_url:
        print("❌ No URL provided. Exiting.")
        return
    
    # Remove trailing slash if present
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    print(f"\n🎯 Testing service at: {base_url}")
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test endpoints
    endpoints = [
        ("/health", "Health Check"),
        ("/", "Home Page"),
        ("/status", "Status Page")
    ]
    
    results = []
    for endpoint, name in endpoints:
        url = f"{base_url}{endpoint}"
        success = test_endpoint(url, name)
        results.append((name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n🎯 Overall: {passed}/{total} endpoints working")
    
    if passed == total:
        print("🎉 All endpoints are working! Your BSE Monitor is running successfully.")
        print("📧 Email alerts will be sent to: 9ranjal@gmail.com")
    elif passed > 0:
        print("⚠️  Some endpoints are working. Check Render logs for issues.")
    else:
        print("❌ No endpoints are working. Check if service is deployed and running.")
        print("🔍 Check your Render dashboard for deployment status and logs.")

if __name__ == "__main__":
    main() 