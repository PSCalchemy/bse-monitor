import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict
from datetime import datetime
import os

from config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, 
    SENDER_EMAIL, RECIPIENT_EMAILS
)

class EmailSender:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = SMTP_USERNAME
        self.password = SMTP_PASSWORD
        self.sender_email = SENDER_EMAIL
        self.recipient_emails = [email.strip() for email in RECIPIENT_EMAILS if email.strip()]

    def send_announcement_alert(self, announcement: Dict):
        """Send email alert for a new announcement."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.generate_subject(announcement)
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            
            # Create HTML content
            html_content = self.create_html_content(announcement)
            msg.attach(MIMEText(html_content, 'html'))
            
            # Create plain text content as fallback
            text_content = self.create_text_content(announcement)
            msg.attach(MIMEText(text_content, 'plain'))
            
            # Send email
            self.send_email(msg)
            
        except Exception as e:
            self.logger.error(f"Error sending announcement alert: {e}")
            raise

    def generate_subject(self, announcement: Dict) -> str:
        """Generate email subject line."""
        company = announcement.get('company', 'Unknown Company')
        urgency_score = announcement.get('urgency_score', 0)
        
        # Add urgency indicator to subject
        if urgency_score > 0.8:
            urgency_indicator = "🚨 URGENT: "
        elif urgency_score > 0.6:
            urgency_indicator = "⚠️ HIGH: "
        elif urgency_score > 0.4:
            urgency_indicator = "📈 MEDIUM: "
        else:
            urgency_indicator = "📊 "
        
        # Add flags to subject if available
        flags = announcement.get('flags', [])
        flag_text = ""
        if flags:
            flag_text = f" [{', '.join(flags[:2])}]"  # Limit to first 2 flags
        
        return f"{urgency_indicator}BSE Alert - {company}{flag_text}"

    def create_html_content(self, announcement: Dict) -> str:
        """Create HTML email content."""
        html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .alert-box { background: #f8f9fa; border-left: 4px solid #007bff; 
                   padding: 15px; margin: 15px 0; border-radius: 4px; }
        .score-box { display: inline-block; background: #e9ecef; 
                   padding: 8px 12px; border-radius: 4px; margin: 5px; }
        .flag { display: inline-block; background: #28a745; color: white; 
               padding: 4px 8px; border-radius: 12px; margin: 2px; font-size: 12px; }
        .keyword { display: inline-block; background: #17a2b8; color: white; 
                 padding: 3px 6px; border-radius: 10px; margin: 2px; font-size: 11px; }
        .metric { background: #fff3cd; border: 1px solid #ffeaa7; 
                 padding: 10px; border-radius: 4px; margin: 10px 0; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; 
                 font-size: 12px; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 BSE Corporate Announcement Alert</h1>
            <p>New announcement detected and analyzed</p>
        </div>
        
        <div class="alert-box">
            <h2>{company}</h2>
            <p><strong>Time:</strong> {timestamp}</p>
            <p><strong>Category:</strong> {category}</p>
        </div>
        
        {title_section}
        
        <div class="metric">
            <h3>📊 Analysis Scores</h3>
            <div class="score-box">Urgency: {urgency_score}</div>
            <div class="score-box">Confidence: {confidence_score}</div>
            <div class="score-box">Sentiment: {sentiment}</div>
        </div>
        
        {flags_section}
        
        {keywords_section}
        
        {metrics_section}
        
        {announcement_text_section}
        
        <div class="footer">
            <p>This alert was generated automatically by the BSE Monitor system.</p>
            <p>Generated at: {generated_time}</p>
        </div>
    </div>
</body>
</html>"""
        
        # Prepare content sections
        title_section = ""
        if announcement.get('title'):
            title_section = f'<div class="alert-box"><h3>📋 Title</h3><p>{announcement["title"]}</p></div>'
        
        flags_section = ""
        flags = announcement.get('flags', [])
        if flags:
            flag_html = ''.join([f'<span class="flag">{flag}</span>' for flag in flags])
            flags_section = f'<div class="metric"><h3>🚩 Flags</h3>{flag_html}</div>'
        
        keywords_section = ""
        keywords = announcement.get('keywords', [])
        if keywords:
            keyword_html = ''.join([f'<span class="keyword">{keyword}</span>' for keyword in keywords[:8]])
            keywords_section = f'<div class="metric"><h3>🔍 Keywords</h3>{keyword_html}</div>'
        
        metrics_section = ""
        key_metrics = announcement.get('key_metrics', {})
        if key_metrics:
            metrics_html = ''.join([f'<p><strong>{k}:</strong> {v}</p>' for k, v in key_metrics.items()])
            metrics_section = f'<div class="metric"><h3>📈 Key Metrics</h3>{metrics_html}</div>'
        
        announcement_text_section = ""
        announcement_text = announcement.get('announcement_text', '')
        if announcement_text:
            # Truncate if too long
            if len(announcement_text) > 500:
                announcement_text = announcement_text[:500] + "..."
            announcement_text_section = f'<div class="metric"><h3>📄 Announcement Text</h3><p>{announcement_text}</p></div>'
        
        return html_template.format(
            company=announcement.get('company', 'Unknown Company'),
            timestamp=announcement.get('timestamp', 'Unknown'),
            category=announcement.get('category', 'General'),
            title_section=title_section,
            urgency_score=f"{announcement.get('urgency_score', 0):.2f}",
            confidence_score=f"{announcement.get('confidence_score', 0):.2f}",
            sentiment=announcement.get('sentiment', 'neutral').title(),
            flags_section=flags_section,
            keywords_section=keywords_section,
            metrics_section=metrics_section,
            announcement_text_section=announcement_text_section,
            generated_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def create_text_content(self, announcement: Dict) -> str:
        """Create plain text email content."""
        text_content = f"""
BSE CORPORATE ANNOUNCEMENT ALERT
================================

Company: {announcement.get('company', 'Unknown Company')}
Time: {announcement.get('timestamp', 'Unknown')}
Category: {announcement.get('category', 'General')}

"""
        
        if announcement.get('title'):
            text_content += f"Title: {announcement['title']}\n\n"
        
        text_content += f"""
Analysis Scores:
- Urgency Score: {announcement.get('urgency_score', 0):.2f}
- Confidence Score: {announcement.get('confidence_score', 0):.2f}
- Sentiment: {announcement.get('sentiment', 'neutral').title()}

"""
        
        flags = announcement.get('flags', [])
        if flags:
            text_content += f"Flags: {', '.join(flags)}\n\n"
        
        keywords = announcement.get('keywords', [])
        if keywords:
            text_content += f"Keywords: {', '.join(keywords[:8])}\n\n"
        
        key_metrics = announcement.get('key_metrics', {})
        if key_metrics:
            text_content += "Key Metrics:\n"
            for k, v in key_metrics.items():
                text_content += f"- {k}: {v}\n"
            text_content += "\n"
        
        announcement_text = announcement.get('announcement_text', '')
        if announcement_text:
            if len(announcement_text) > 500:
                announcement_text = announcement_text[:500] + "..."
            text_content += f"Announcement Text:\n{announcement_text}\n\n"
        
        text_content += f"""
---
Generated by BSE Monitor System
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return text_content

    def send_email(self, msg):
        """Send email using SMTP."""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully to {len(self.recipient_emails)} recipients")
            
        except smtplib.SMTPAuthenticationError:
            self.logger.error("SMTP authentication failed. Check username and password.")
            raise
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error occurred: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            raise

    def test_email_configuration(self):
        """Test email configuration by sending a test email."""
        try:
            test_announcement = {
                'company': 'Test Company Ltd.',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'title': 'Test Announcement',
                'category': 'Test',
                'urgency_score': 0.75,
                'confidence_score': 0.85,
                'flags': ['📈 Earnings Spike', '🛠️ Order Win'],
                'keywords': ['test', '300% increase', '₹150 cr order'],
                'key_metrics': {'order_value': 1500000000, 'growth_rate': 300},
                'sentiment': 'positive',
                'announcement_text': 'This is a test announcement to verify email configuration.'
            }
            
            self.send_announcement_alert(test_announcement)
            return True
            
        except Exception as e:
            self.logger.error(f"Email configuration test failed: {e}")
            return False 