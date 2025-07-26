#!/usr/bin/env python3
"""
BSE Monitor - Web Service Version for Render.com
Includes web server for health checks and background monitoring
"""

import requests
import json
import time
import logging
import schedule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
import os
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import threading
from flask import Flask, jsonify

# Optional Selenium imports for advanced scraping
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Add debug logging at startup
print("🚀 Starting BSE Monitor Web Service...")
print(f"📁 Current directory: {os.getcwd()}")
print(f"🔧 Environment: {os.environ.get('RENDER_ENVIRONMENT', 'unknown')}")
print(f"🌐 Port: {os.environ.get('PORT', '8080')}")

from config import *
from xbrl_parser import XBRLParser
from email_sender import EmailSender
from announcement_analyzer import AnnouncementAnalyzer

# Create Flask app for web service
app = Flask(__name__)

print("✅ Flask app created successfully")

# Global variables for monitoring
# Initialize with IST timestamps
from datetime import datetime
import pytz
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(ist)

monitor_status = {
    'last_check': 'Never',
    'total_announcements': 0,
    'last_announcement': None,
    'service_started': current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST'),
    'status': 'running',
    'last_heartbeat': current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST'),
    'monitoring_active': True
}

@app.route('/health')
def health():
    """Health check endpoint"""
    print("🏥 Health check endpoint called")
    
    # Convert to IST
    from datetime import datetime
    import pytz
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist)
    
    return jsonify({
        'status': 'healthy',
        'service': 'BSE Monitor',
        'timestamp': current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST'),
        'timestamp_utc': datetime.now().isoformat(),
        'email': '9ranjal@gmail.com',
        'last_check': monitor_status['last_check'],
        'total_announcements': monitor_status['total_announcements'],
        'service_started': monitor_status['service_started']
    })

@app.route('/')
def home():
    """Home page endpoint"""
    print("🏠 Home endpoint called")
    
    # Convert to IST
    from datetime import datetime
    import pytz
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist)
    
    return jsonify({
        'message': 'BSE Monitor is running',
        'status': 'active',
        'email': '9ranjal@gmail.com',
        'last_check': monitor_status['last_check'],
        'total_announcements': monitor_status['total_announcements'],
        'last_announcement': monitor_status['last_announcement'],
        'current_time_ist': current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST')
    })



@app.route('/check-now')
def check_now():
    """Manually trigger an announcement check"""
    print("🔍 Manual check triggered")
    
    # Convert to IST
    from datetime import datetime
    import pytz
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist)
    
    try:
        # Create monitor instance and run check
        monitor = BSEMonitor()
        monitor.check_for_new_announcements()
        
        return jsonify({
            'message': 'Manual check completed',
            'timestamp_ist': current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST'),
            'timestamp_utc': datetime.now().isoformat(),
            'last_check': monitor_status['last_check']
        })
    except Exception as e:
        return jsonify({
            'error': f'Manual check failed: {e}',
            'timestamp_ist': current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST'),
            'timestamp_utc': datetime.now().isoformat()
        }), 500

@app.route('/status')
def status():
    """Detailed status endpoint"""
    print("📊 Status endpoint called")
    
    # Add memory monitoring
    import psutil
    memory_info = {}
    try:
        process = psutil.Process()
        memory_info = {
            'memory_percent': process.memory_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent()
        }
    except:
        memory_info = {'error': 'Could not get memory info'}
    

    
    return jsonify({
        'service': 'BSE Monitor',
        'status': monitor_status['status'],
        'started': monitor_status['service_started'],
        'last_check': monitor_status['last_check'],
        'last_heartbeat': monitor_status['last_heartbeat'],
        'monitoring_active': monitor_status['monitoring_active'],
        'total_announcements': monitor_status['total_announcements'],
        'last_announcement': monitor_status['last_announcement'],
        'email_recipient': '9ranjal@gmail.com',
        'check_interval_minutes': CHECK_INTERVAL_MINUTES,
        'system_info': memory_info
    })

print("✅ Flask routes registered successfully")

class BSEMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.processed_announcements = self.load_processed_announcements()
        self.xbrl_parser = XBRLParser()
        self.email_sender = EmailSender()
        self.analyzer = AnnouncementAnalyzer()
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()  # Only console logging for Render
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_processed_announcements(self) -> set:
        """Load previously processed announcement IDs from file."""
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
        except Exception as e:
            self.logger.error(f"Error loading processed announcements: {e}")
        return set()

    def save_processed_announcements(self):
        """Save processed announcement IDs to file."""
        try:
            data = {
                'processed_ids': list(self.processed_announcements),
                'last_updated': datetime.now().isoformat()
            }
            with open(DB_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving processed announcements: {e}")

    def fetch_announcements_page(self) -> Optional[str]:
        """Fetch the BSE announcements page."""
        try:
            self.logger.info(f"Fetching BSE announcements from: {BSE_ANNOUNCEMENTS_URL}")
            response = self.session.get(BSE_ANNOUNCEMENTS_URL, timeout=30)
            response.raise_for_status()
            self.logger.info(f"BSE page fetched successfully, content length: {len(response.text)}")
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching BSE page: {e}")
            return None
    
    def fetch_announcements_selenium(self) -> Optional[List[Dict]]:
        """Fetch announcements using Selenium to handle dynamic content."""
        if not SELENIUM_AVAILABLE:
            self.logger.warning("Selenium not available, skipping Selenium scraping")
            return None
        
        try:
            self.logger.info("Attempting Selenium-based scraping...")
            
            # Setup Chrome options for headless browsing
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            driver = None
            try:
                # Try to use webdriver-manager to get Chrome driver
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            except Exception as e:
                self.logger.warning(f"Could not use webdriver-manager: {e}")
                # Fallback to system Chrome
                try:
                    driver = webdriver.Chrome(options=chrome_options)
                except Exception as e2:
                    self.logger.error(f"Could not initialize Chrome driver: {e2}")
                    return None
            
            if not driver:
                return None
            
            try:
                # Navigate to the BSE announcements page
                self.logger.info("Navigating to BSE announcements page...")
                driver.get(BSE_ANNOUNCEMENTS_URL)
                
                # Wait for the page to load
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Wait a bit more for JavaScript to load
                time.sleep(5)
                
                # Look for announcement elements
                announcements = []
                
                # Try to find announcement table rows
                try:
                    # Look for table rows that might contain announcements
                    rows = driver.find_elements(By.TAG_NAME, "tr")
                    self.logger.info(f"Found {len(rows)} table rows with Selenium")
                    
                    # Wait a bit more for JavaScript to fully render
                    time.sleep(3)
                    
                    # Try to find actual announcement data in the page
                    page_text = driver.page_source
                    
                    # Look for patterns that indicate actual announcement data
                    # The page contains AngularJS templates, but we need to find the actual rendered content
                    
                    # Try to find elements that might contain actual announcement data
                    announcement_elements = driver.find_elements(By.CSS_SELECTOR, "td.tdcolumngrey")
                    
                    if announcement_elements:
                        self.logger.info(f"Found {len(announcement_elements)} announcement elements")
                        
                        # Process each announcement element
                        for i, element in enumerate(announcement_elements[:20]):  # Limit to first 20
                            try:
                                element_text = element.text.strip()
                                
                                # Skip if it's just template text or empty
                                if not element_text or '{{' in element_text or '}}' in element_text:
                                    continue
                                
                                # Try to extract meaningful data
                                lines = element_text.split('\n')
                                if len(lines) >= 2:
                                    # First line might be company name, second line might be title
                                    company_line = lines[0].strip()
                                    title_line = lines[1].strip() if len(lines) > 1 else ""
                                    
                                    # Clean up the data
                                    company = self.clean_company_name(company_line)
                                    title = self.clean_title(title_line)
                                    
                                    if company and title and len(title) > 10:
                                        announcement = {
                                            'id': f"selenium_announcement_{i}_{hash(element_text)}",
                                            'company': company,
                                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                            'title': title,
                                            'category': 'General',
                                            'xbrl_url': None,
                                            'attachment_url': None
                                        }
                                        
                                        announcements.append(announcement)
                                        self.logger.info(f"Extracted Selenium announcement {i+1}: {company} - {title[:50]}...")
                                        
                            except Exception as e:
                                self.logger.error(f"Error processing Selenium element {i}: {e}")
                                continue
                    
                    # If no announcements found, try a different approach
                    if not announcements:
                        self.logger.info("No announcements found with tdcolumngrey, trying alternative approach...")
                        
                        # Look for any text that looks like company announcements
                        all_text = driver.find_element(By.TAG_NAME, "body").text
                        
                        # Split by lines and look for patterns
                        lines = all_text.split('\n')
                        current_company = None
                        
                        for line in lines:
                            line = line.strip()
                            if not line or len(line) < 5:
                                continue
                                
                            # Look for company patterns (usually in caps, contains "Ltd", "Limited", etc.)
                            if any(keyword in line.upper() for keyword in ['LTD', 'LIMITED', 'CORPORATION', 'COMPANY']):
                                current_company = line
                                continue
                                
                            # Look for announcement patterns
                            if current_company and any(keyword in line.lower() for keyword in ['announcement', 'board', 'meeting', 'result', 'dividend', 'agm']):
                                if len(line) > 10:
                                    announcement = {
                                        'id': f"selenium_text_announcement_{hash(line)}",
                                        'company': current_company,
                                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        'title': line,
                                        'category': 'General',
                                        'xbrl_url': None,
                                        'attachment_url': None
                                    }
                                    
                                    announcements.append(announcement)
                                    self.logger.info(f"Extracted text announcement: {current_company} - {line[:50]}...")
                                    break  # Only take first meaningful announcement per company
                    
                    self.logger.info(f"Total Selenium announcements extracted: {len(announcements)}")
                    
                except Exception as e:
                    self.logger.error(f"Error extracting announcements with Selenium: {e}")
                
                return announcements
                
            finally:
                driver.quit()
                
        except Exception as e:
            self.logger.error(f"Error in Selenium scraping: {e}")
            return None

    def fetch_announcements_api(self) -> Optional[dict]:
        """Fetch announcements from BSE API with proper parameters."""
        try:
            # Try the correct API endpoint with parameters
            api_url = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"
            self.logger.info(f"Fetching BSE announcements from API: {api_url}")
            
            # Get today's date in DD/MM/YYYY format
            from datetime import datetime
            today = datetime.now()
            date_str = today.strftime("%d/%m/%Y")
            
            # Parameters based on the JavaScript controller
            params = {
                'strScrip': '',  # Empty for all companies
                'strCat': '-1',  # All categories
                'strPrevDate': date_str,
                'strToDate': date_str,
                'strSearch': 'P',  # Period search
                'strType': 'C',    # Corporate announcements
                'pageno': '1',     # First page
                'subcategory': '-1'  # All subcategories
            }
            
            # Add required headers for API
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.bseindia.com/corporates/ann.html',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            response = self.session.get(api_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"BSE API response received, Table length: {len(data.get('Table', []))}")
            
            # If API returns empty, try the original endpoint as fallback
            if not data.get('Table') or len(data.get('Table', [])) == 0:
                self.logger.info("Primary API returned empty, trying fallback endpoint...")
                fallback_url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w"
                response = self.session.get(fallback_url, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
                self.logger.info(f"Fallback API response received, Table length: {len(data.get('Table', []))}")
            
            return data
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching BSE API: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing BSE API JSON: {e}")
            return None

    def extract_announcements(self, html_content: str) -> List[Dict]:
        """Extract announcement data from the HTML page."""
        announcements = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        self.logger.info(f"Parsing HTML content, length: {len(html_content)}")
        
        # Look for AngularJS data patterns in the HTML
        # The announcements are rendered via AngularJS, so we need to look for patterns
        self.logger.info("Looking for AngularJS announcement patterns...")
        
        # Try to find any text that looks like announcement data
        # Look for patterns like company names, dates, etc.
        text_content = soup.get_text()
        
        # Look for table structures that might contain announcements
        tables = soup.find_all('table')
        self.logger.info(f"Found {len(tables)} tables in HTML")
        
        # Look for specific patterns that indicate announcements
        announcement_indicators = [
            'NEWSSUB', 'SCRIP_CD', 'SLONGNAME', 'NEWS_DT', 'CATEGORYNAME',
            'Corporate Announcement', 'Announcement', 'Company', 'Security Code'
        ]
        
        found_indicators = []
        for indicator in announcement_indicators:
            if indicator in text_content:
                found_indicators.append(indicator)
        
        self.logger.info(f"Found announcement indicators: {found_indicators}")
        
        # Since the content is dynamic, let's try to extract any structured data
        # Look for table rows with multiple cells that might contain announcement data
        all_rows = soup.find_all('tr')
        self.logger.info(f"Found {len(all_rows)} total table rows")
        
        # Look for rows that might contain announcement-like data
        potential_announcement_rows = []
        for row in all_rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                cell_text = ' '.join([cell.get_text(strip=True) for cell in cells])
                # Look for patterns that suggest this is an announcement row
                if any(keyword in cell_text.lower() for keyword in ['announcement', 'corporate', 'company', 'news', 'date']):
                    potential_announcement_rows.append(row)
        
        self.logger.info(f"Found {len(potential_announcement_rows)} potential announcement rows")
        
        # Try to extract data from potential announcement rows
        for i, row in enumerate(potential_announcement_rows):
            try:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # Extract basic information
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    # Try to identify company name, date, title from cell contents
                    announcement = {
                        'id': f"html_announcement_{i}_{hash(str(cell_texts))}",
                        'company': self.extract_company_name_from_text(cell_texts),
                        'timestamp': self.extract_timestamp_from_text(cell_texts),
                        'title': self.extract_title_from_text(cell_texts),
                        'category': 'General',
                        'xbrl_url': self.extract_xbrl_url(row),
                        'attachment_url': self.extract_attachment_url(row)
                    }
                    
                    # Only add if we have meaningful data
                    if announcement['title'] and announcement['title'] != 'No Title':
                        announcements.append(announcement)
                        self.logger.info(f"Extracted HTML announcement {i+1}: {announcement['company']} - {announcement['title'][:50]}...")
            except Exception as e:
                self.logger.error(f"Error extracting HTML announcement {i+1}: {e}")
                continue
        
        self.logger.info(f"Total HTML announcements extracted: {len(announcements)}")
        return announcements
    
    def extract_company_name_from_text(self, cell_texts: List[str]) -> str:
        """Extract company name from cell text content."""
        for text in cell_texts:
            # Look for patterns that suggest company names
            if len(text) > 3 and any(char.isupper() for char in text) and not text.isdigit():
                # Avoid common non-company text
                if text.lower() not in ['announcement', 'corporate', 'news', 'date', 'time', 'category']:
                    return text
        return "Unknown Company"
    
    def extract_timestamp_from_text(self, cell_texts: List[str]) -> str:
        """Extract timestamp from cell text content."""
        for text in cell_texts:
            # Look for date patterns
            if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text):
                return text
            elif re.search(r'\d{1,2}:\d{2}', text):
                return text
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def extract_title_from_text(self, cell_texts: List[str]) -> str:
        """Extract announcement title from cell text content."""
        for text in cell_texts:
            if len(text) > 10 and not text.isdigit():
                # Avoid common non-title text
                if text.lower() not in ['announcement', 'corporate', 'news', 'date', 'time', 'category', 'company']:
                    return text
        return "No Title"
    
    def clean_company_name(self, text: str) -> str:
        """Clean company name from text."""
        if not text:
            return "Unknown Company"
        
        # Remove common prefixes/suffixes
        text = text.strip()
        text = text.replace('Ltd', 'Ltd').replace('Limited', 'Ltd')
        
        # Extract first part (usually company name)
        parts = text.split('-')
        if len(parts) > 1:
            return parts[0].strip()
        
        return text
    
    def clean_title(self, text: str) -> str:
        """Clean announcement title from text."""
        if not text:
            return "No Title"
        
        # Remove AngularJS template text
        if '{{' in text or '}}' in text:
            return "No Title"
        
        # Remove common noise
        text = text.strip()
        text = text.replace('Exchange Received Time', '').replace('Exchange Disseminated Time', '')
        text = text.replace('Time Taken', '').replace('Read More..', '').replace('Read less..', '')
        
        # Clean up extra whitespace
        text = ' '.join(text.split())
        
        if len(text) < 5:
            return "No Title"
        
        return text

    def extract_announcements_api(self, api_data: dict) -> List[Dict]:
        """Extract announcement data from the API response."""
        announcements = []
        
        if not api_data or 'Table' not in api_data:
            self.logger.warning("No Table data in API response")
            return announcements
        
        table_data = api_data['Table']
        if not isinstance(table_data, list):
            self.logger.warning("Table data is not a list")
            return announcements
        
        self.logger.info(f"Processing {len(table_data)} announcements from API")
        
        for i, item in enumerate(table_data):
            try:
                # Extract data from API response
                announcement = {
                    'id': f"{item.get('SCRIP_CD', '')}_{item.get('NEWS_DT', '')}",
                    'company': item.get('SLONGNAME', 'Unknown Company'),
                    'timestamp': item.get('NEWS_DT', ''),
                    'title': item.get('NEWSSUB', 'No Title'),
                    'category': item.get('CATEGORYNAME', 'General'),
                    'xbrl_url': item.get('XML_NAME', None),
                    'attachment_url': item.get('ATTACHMENTNAME', None),
                    'security_code': item.get('SCRIP_CD', ''),
                    'news_id': item.get('NEWSID', ''),
                    'submission_time': item.get('News_submission_dt', ''),
                    'dissemination_time': item.get('DissemDT', ''),
                }
                
                announcements.append(announcement)
                self.logger.info(f"Extracted API announcement {i+1}: {announcement['company']} - {announcement['title'][:50]}...")
                
            except Exception as e:
                self.logger.error(f"Error extracting API announcement {i+1}: {e}")
                continue
        
        self.logger.info(f"Total API announcements extracted: {len(announcements)}")
        return announcements

    def generate_announcement_id(self, row) -> str:
        """Generate a unique ID for the announcement."""
        timestamp = self.extract_timestamp_from_row(row)
        company = self.extract_company_name_from_row(row)
        return f"{company}_{timestamp}".replace(" ", "_").replace(":", "")

    def extract_company_name(self, cells) -> str:
        """Extract company name from table cells."""
        if len(cells) > 0:
            return cells[0].get_text(strip=True)
        return "Unknown Company"

    def extract_timestamp(self, cells) -> str:
        """Extract timestamp from table cells."""
        if len(cells) > 1:
            return cells[1].get_text(strip=True)
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def extract_title(self, cells) -> str:
        """Extract announcement title from table cells."""
        if len(cells) > 2:
            return cells[2].get_text(strip=True)
        return "No Title"

    def extract_category(self, cells) -> str:
        """Extract announcement category from table cells."""
        if len(cells) > 3:
            return cells[3].get_text(strip=True)
        return "General"

    def extract_xbrl_url(self, row) -> Optional[str]:
        """Extract XBRL URL from the row."""
        links = row.find_all('a', href=True)
        for link in links:
            href = link['href']
            if '.xml' in href.lower() or 'xbrl' in href.lower():
                return urljoin(BSE_BASE_URL, href)
        return None

    def extract_attachment_url(self, row) -> Optional[str]:
        """Extract attachment URL from the row."""
        links = row.find_all('a', href=True)
        for link in links:
            href = link['href']
            if any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx']):
                return urljoin(BSE_BASE_URL, href)
        return None

    def extract_timestamp_from_row(self, row) -> str:
        """Extract timestamp from row for ID generation."""
        cells = row.find_all('td')
        return self.extract_timestamp(cells)

    def extract_company_name_from_row(self, row) -> str:
        """Extract company name from row for ID generation."""
        cells = row.find_all('td')
        return self.extract_company_name(cells)

    def fetch_xbrl_content(self, xbrl_url: str) -> Optional[str]:
        """Fetch XBRL content from URL."""
        try:
            response = self.session.get(xbrl_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching XBRL content: {e}")
            return None

    def process_announcement(self, announcement: Dict) -> Optional[Dict]:
        """Process a single announcement and return enriched data."""
        if announcement['id'] in self.processed_announcements:
            return None

        # Fetch XBRL content if available
        xbrl_content = None
        if announcement['xbrl_url']:
            xbrl_content = self.fetch_xbrl_content(announcement['xbrl_url'])
            if xbrl_content:
                parsed_data = self.xbrl_parser.parse(xbrl_content)
                announcement.update(parsed_data)

        # Analyze the announcement
        try:
            analysis = self.analyzer.analyze_announcement(
                title=announcement.get('title', ''),
                content=announcement.get('title', ''),  # Use title as content for now
                xbrl_content=xbrl_content,
                company_info={'company_name': announcement.get('company', '')}
            )
            announcement.update(analysis)
        except Exception as e:
            self.logger.error(f"Error analyzing announcement: {e}")
            # Add basic analysis if analyzer fails
            announcement.update({
                'urgency_score': 0.5,
                'confidence_score': 0.5,
                'category': 'general'
            })

        # Mark as processed
        self.processed_announcements.add(announcement['id'])

        return announcement

    def check_for_new_announcements(self):
        """Main method to check for new announcements."""
        try:
            self.logger.info("Checking for new BSE announcements...")
            
            # Store timestamp in IST
            from datetime import datetime
            import pytz
            ist = pytz.timezone('Asia/Kolkata')
            current_time_ist = datetime.now(ist)
            monitor_status['last_check'] = current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST')
            
            # Try API first
            api_data = self.fetch_announcements_api()
            announcements = []
            
            if api_data and api_data.get('Table'):
                announcements = self.extract_announcements_api(api_data)
                self.logger.info(f"Extracted {len(announcements)} total announcements from BSE API")
            else:
                self.logger.warning("API returned no data, trying HTML scraping as fallback...")
                # Try HTML scraping as fallback
                html_content = self.fetch_announcements_page()
                if html_content:
                    announcements = self.extract_announcements(html_content)
                    self.logger.info(f"Extracted {len(announcements)} total announcements from HTML scraping")
                    
                    # If HTML scraping also failed, try Selenium as final fallback
                    if not announcements:
                        self.logger.warning("HTML scraping returned no data, trying Selenium as final fallback...")
                        selenium_announcements = self.fetch_announcements_selenium()
                        if selenium_announcements:
                            announcements = selenium_announcements
                            self.logger.info(f"Extracted {len(announcements)} total announcements from Selenium scraping")
                else:
                    self.logger.error("HTML scraping failed, trying Selenium as final fallback...")
                    selenium_announcements = self.fetch_announcements_selenium()
                    if selenium_announcements:
                        announcements = selenium_announcements
                        self.logger.info(f"Extracted {len(announcements)} total announcements from Selenium scraping")
                    else:
                        self.logger.error("All scraping methods failed")
                        return
            
            new_announcements = []
            processed_count = 0

            for i, announcement in enumerate(announcements):
                try:
                    self.logger.info(f"Processing announcement {i+1}/{len(announcements)}: {announcement['company']} - {announcement['timestamp']}")
                    processed = self.process_announcement(announcement)
                    if processed:
                        new_announcements.append(processed)
                        self.logger.info(f"NEW ANNOUNCEMENT FOUND: {processed['company']} - {processed['title'][:50]}...")
                    else:
                        self.logger.info(f"Announcement already processed: {announcement['company']}")
                    processed_count += 1
                except Exception as e:
                    self.logger.error(f"Error processing announcement {i+1}: {e}")
                    continue

            self.logger.info(f"Processed {processed_count} announcements, found {len(new_announcements)} new ones")

            if new_announcements:
                self.logger.info(f"Found {len(new_announcements)} new announcements")
                self.send_alerts(new_announcements)
                self.save_processed_announcements()
                
                # Update global status
                monitor_status['total_announcements'] += len(new_announcements)
                monitor_status['last_announcement'] = new_announcements[0]['company']
            else:
                self.logger.info("No new announcements found")
                    
        except Exception as e:
            self.logger.error(f"Error in check_for_new_announcements: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")

    def send_alerts(self, announcements: List[Dict]):
        """Send email alerts for new announcements."""
        for announcement in announcements:
            try:
                self.email_sender.send_announcement_alert(announcement)
                self.logger.info(f"Alert sent for announcement: {announcement['company']}")
            except Exception as e:
                self.logger.error(f"Error sending alert for {announcement['company']}: {e}")

    def run_monitor(self):
        """Run the monitoring service in background."""
        self.logger.info("Starting BSE Announcement Monitor...")
        
        # Run immediately on startup
        try:
            self.logger.info("Running initial announcement check...")
            self.check_for_new_announcements()
            self.logger.info("Initial check completed successfully")
        except Exception as e:
            self.logger.error(f"Error in initial check: {e}")
            import traceback
            self.logger.error(f"Initial check traceback: {traceback.format_exc()}")
        
        # Schedule regular checks
        self.logger.info(f"Scheduling checks every {CHECK_INTERVAL_MINUTES} minutes")
        schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(self.check_for_new_announcements)
        
        loop_count = 0
        while True:
            try:
                loop_count += 1
                
                # Update heartbeat in IST
                from datetime import datetime
                import pytz
                ist = pytz.timezone('Asia/Kolkata')
                current_time_ist = datetime.now(ist)
                monitor_status['last_heartbeat'] = current_time_ist.strftime('%Y-%m-%d %H:%M:%S IST')
                
                if loop_count % 10 == 0:  # Log every 10 minutes
                    self.logger.info(f"Monitoring loop iteration {loop_count} - checking for scheduled tasks")
                
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
            except Exception as e:
                self.logger.error(f"Error in monitoring loop iteration {loop_count}: {e}")
                import traceback
                self.logger.error(f"Monitoring loop traceback: {traceback.format_exc()}")
                monitor_status['monitoring_active'] = False
                time.sleep(60)  # Continue after error

def run_flask():
    """Run Flask app for web service."""
    try:
        port = int(os.environ.get('PORT', 8080))
        print(f"🌐 Starting Flask server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")
        raise

if __name__ == "__main__":
    try:
        print("🔧 Creating BSE Monitor instance...")
        # Create monitor instance
        monitor = BSEMonitor()
        
        print("🔄 Starting monitor in background thread...")
        # Start monitor in background thread
        monitor_thread = threading.Thread(target=monitor.run_monitor, daemon=True)
        monitor_thread.start()
        
        print("🚀 Starting Flask web service...")
        # Start Flask app for web service
        run_flask()
    except Exception as e:
        print(f"❌ Fatal error during startup: {e}")
        import traceback
        traceback.print_exc()
        raise 