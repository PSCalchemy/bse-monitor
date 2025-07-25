#!/usr/bin/env python3
"""
Test script to check if BSE monitor can import all modules
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        print("✓ Importing requests...")
        import requests
        
        print("✓ Importing beautifulsoup4...")
        import bs4
        
        print("✓ Importing lxml...")
        import lxml
        
        print("✓ Importing schedule...")
        import schedule
        
        print("✓ Importing python-dotenv...")
        import dotenv
        
        print("✓ Importing email-validator...")
        import email_validator
        
        print("✓ Importing textblob...")
        import textblob
        
        print("✓ Importing flask...")
        import flask
        
        print("✓ Importing config...")
        import config
        
        print("✓ Importing xbrl_parser...")
        import xbrl_parser
        
        print("✓ Importing email_sender...")
        import email_sender
        
        print("✓ Importing announcement_analyzer...")
        import announcement_analyzer
        
        print("✓ Importing bse_monitor_web...")
        import bse_monitor_web
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")
    
    try:
        from bse_monitor_web import app
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

if __name__ == "__main__":
    print("BSE Monitor Import Test")
    print("=" * 30)
    
    imports_ok = test_imports()
    flask_ok = test_flask_app()
    
    if imports_ok and flask_ok:
        print("\n✅ All tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed! Check the errors above.")
        sys.exit(1) 