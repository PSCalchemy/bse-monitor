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
monitor_status = {
    'last_check': 'Never',
    'total_announcements': 0,
    'last_announcement': None,
    'service_started': datetime.now().isoformat(),
    'status': 'running'
}

@app.route('/health')
def health():
    """Health check endpoint"""
    print("🏥 Health check endpoint called")
    return jsonify({
        'status': 'healthy',
        'service': 'BSE Monitor',
        'timestamp': datetime.now().isoformat(),
        'email': '9ranjal@gmail.com',
        'last_check': monitor_status['last_check'],
        'total_announcements': monitor_status['total_announcements'],
        'service_started': monitor_status['service_started']
    })

@app.route('/')
def home():
    """Home page endpoint"""
    print("🏠 Home endpoint called")
    return jsonify({
        'message': 'BSE Monitor is running',
        'status': 'active',
        'email': '9ranjal@gmail.com',
        'last_check': monitor_status['last_check'],
        'total_announcements': monitor_status['total_announcements'],
        'last_announcement': monitor_status['last_announcement']
    })

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
            response = self.session.get(BSE_ANNOUNCEMENTS_URL, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching BSE page: {e}")
            return None

    def extract_announcements(self, html_content: str) -> List[Dict]:
        """Extract announcement data from the HTML page."""
        announcements = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for announcement tables/rows
        # The actual structure may need adjustment based on BSE's HTML
        announcement_rows = soup.find_all('tr', class_=re.compile(r'announcement|corporate'))
        
        for row in announcement_rows:
            try:
                # Extract announcement details
                cells = row.find_all('td')
                if len(cells) >= 3:
                    announcement = {
                        'id': self.generate_announcement_id(row),
                        'company': self.extract_company_name(cells),
                        'timestamp': self.extract_timestamp(cells),
                        'title': self.extract_title(cells),
                        'category': self.extract_category(cells),
                        'xbrl_url': self.extract_xbrl_url(row),
                        'attachment_url': self.extract_attachment_url(row)
                    }
                    announcements.append(announcement)
            except Exception as e:
                self.logger.error(f"Error extracting announcement: {e}")
                continue
        
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
        analysis = self.analyzer.analyze(announcement)
        announcement.update(analysis)

        # Mark as processed
        self.processed_announcements.add(announcement['id'])

        return announcement

    def check_for_new_announcements(self):
        """Main method to check for new announcements."""
        try:
            self.logger.info("Checking for new BSE announcements...")
            monitor_status['last_check'] = datetime.now().isoformat()
            
            html_content = self.fetch_announcements_page()
            if not html_content:
                self.logger.warning("Could not fetch announcements page")
                return

            announcements = self.extract_announcements(html_content)
            new_announcements = []

            for announcement in announcements:
                try:
                    processed = self.process_announcement(announcement)
                    if processed:
                        new_announcements.append(processed)
                except Exception as e:
                    self.logger.error(f"Error processing announcement: {e}")
                    continue

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
            self.check_for_new_announcements()
        except Exception as e:
            self.logger.error(f"Error in initial check: {e}")
        
        # Schedule regular checks
        schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(self.check_for_new_announcements)
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
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