#!/usr/bin/env python3
"""
BSE Monitor - Simple Version for Render.com
No Flask, just the monitoring service
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

from config import *
from xbrl_parser import XBRLParser
from email_sender import EmailSender
from announcement_analyzer import AnnouncementAnalyzer

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
        self.logger.info("Checking for new BSE announcements...")
        
        html_content = self.fetch_announcements_page()
        if not html_content:
            return

        announcements = self.extract_announcements(html_content)
        new_announcements = []

        for announcement in announcements:
            processed = self.process_announcement(announcement)
            if processed:
                new_announcements.append(processed)

        if new_announcements:
            self.logger.info(f"Found {len(new_announcements)} new announcements")
            self.send_alerts(new_announcements)
            self.save_processed_announcements()
        else:
            self.logger.info("No new announcements found")

    def send_alerts(self, announcements: List[Dict]):
        """Send email alerts for new announcements."""
        for announcement in announcements:
            try:
                self.email_sender.send_announcement_alert(announcement)
                self.logger.info(f"Alert sent for announcement: {announcement['company']}")
            except Exception as e:
                self.logger.error(f"Error sending alert for {announcement['company']}: {e}")

    def run(self):
        """Start the monitoring service."""
        self.logger.info("Starting BSE Announcement Monitor...")
        
        # Run immediately on startup
        self.check_for_new_announcements()
        
        # Schedule regular checks
        schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(self.check_for_new_announcements)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled tasks

if __name__ == "__main__":
    monitor = BSEMonitor()
    monitor.run() 