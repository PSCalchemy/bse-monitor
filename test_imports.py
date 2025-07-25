#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
"""

print("Testing imports...")

try:
    import requests
    print("✅ requests imported")
except ImportError as e:
    print(f"❌ requests failed: {e}")

try:
    import json
    print("✅ json imported")
except ImportError as e:
    print(f"❌ json failed: {e}")

try:
    import time
    print("✅ time imported")
except ImportError as e:
    print(f"❌ time failed: {e}")

try:
    import logging
    print("✅ logging imported")
except ImportError as e:
    print(f"❌ logging failed: {e}")

try:
    import schedule
    print("✅ schedule imported")
except ImportError as e:
    print(f"❌ schedule failed: {e}")

try:
    from datetime import datetime, timedelta
    print("✅ datetime imported")
except ImportError as e:
    print(f"❌ datetime failed: {e}")

try:
    from bs4 import BeautifulSoup
    print("✅ BeautifulSoup imported")
except ImportError as e:
    print(f"❌ BeautifulSoup failed: {e}")

try:
    import re
    print("✅ re imported")
except ImportError as e:
    print(f"❌ re failed: {e}")

try:
    from typing import List, Dict, Optional
    print("✅ typing imported")
except ImportError as e:
    print(f"❌ typing failed: {e}")

try:
    import os
    print("✅ os imported")
except ImportError as e:
    print(f"❌ os failed: {e}")

try:
    from urllib.parse import urljoin, urlparse
    print("✅ urllib.parse imported")
except ImportError as e:
    print(f"❌ urllib.parse failed: {e}")

try:
    import xml.etree.ElementTree as ET
    print("✅ xml.etree.ElementTree imported")
except ImportError as e:
    print(f"❌ xml.etree.ElementTree failed: {e}")

try:
    import threading
    print("✅ threading imported")
except ImportError as e:
    print(f"❌ threading failed: {e}")

try:
    from flask import Flask, jsonify
    print("✅ Flask imported")
except ImportError as e:
    print(f"❌ Flask failed: {e}")

try:
    from config import *
    print("✅ config imported")
except ImportError as e:
    print(f"❌ config failed: {e}")

try:
    from xbrl_parser import XBRLParser
    print("✅ XBRLParser imported")
except ImportError as e:
    print(f"❌ XBRLParser failed: {e}")

try:
    from email_sender import EmailSender
    print("✅ EmailSender imported")
except ImportError as e:
    print(f"❌ EmailSender failed: {e}")

try:
    from announcement_analyzer import AnnouncementAnalyzer
    print("✅ AnnouncementAnalyzer imported")
except ImportError as e:
    print(f"❌ AnnouncementAnalyzer failed: {e}")

print("\nAll import tests completed!") 