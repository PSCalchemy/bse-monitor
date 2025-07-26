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
        """Send email alert for all announcements with proper categorization."""
        try:
            # Check if this is meaningful announcement data
            company = announcement.get('company', '')
            title = announcement.get('title', '')
            
            # Skip if it's just template text
            if self.is_template_text(company) or self.is_template_text(title):
                self.logger.info(f"Skipping email for template text announcement: {company[:50]}...")
                return False
            
            # Check if we have meaningful content
            if not self.has_meaningful_content(announcement):
                self.logger.info(f"Skipping email for announcement with no meaningful content")
                return False
            
            # Always send emails now, but check categorization
            email_decision = announcement.get('email_alert_decision', {})
            categorization = email_decision.get('categorization', {})
            
            # Log the categorization
            category = categorization.get('type', 'unknown')
            priority = categorization.get('priority', 'routine')
            self.logger.info(f"Sending email for {category} announcement (priority: {priority}): {title[:50]}...")
            
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
            
            self.logger.info(f"Email sent for {category} announcement: {title[:50]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending announcement alert: {e}")
            raise
    
    def is_template_text(self, text: str) -> bool:
        """Check if text contains AngularJS template syntax."""
        if not text:
            return True
        return '{{' in text or '}}' in text or text.strip() in ['Security Code', 'Exchange Disseminated Time', 'Exchange Received Time']
    
    def has_meaningful_content(self, announcement: Dict) -> bool:
        """Check if announcement has meaningful content."""
        company = announcement.get('company', '')
        title = announcement.get('title', '')
        
        # Must have non-template company and title
        if self.is_template_text(company) or self.is_template_text(title):
            return False
        
        # Must have some actual content
        if len(title.strip()) < 10:
            return False
        
        return True

    def generate_subject(self, announcement: Dict) -> str:
        """Generate email subject line with categorization."""
        # Use the actual announcement structure
        company = announcement.get('company', 'Unknown Company')
        title = announcement.get('title', 'Unknown Title')
        urgency_score = announcement.get('urgency_score', 0)
        category = announcement.get('category', 'General')
        
        # Clean company name for subject
        if company and company != 'Unknown Company':
            # Try to extract a clean company name
            if '{{' in company:
                # If it's template text, use a generic name
                company = 'BSE Company'
            else:
                # Clean up the company name
                company = company.split()[0] if company else 'BSE Company'
        else:
            company = 'BSE Company'
        
        # Add category indicator to subject
        if urgency_score > 0.8:
            category_indicator = "🚨 CRITICAL: "
        elif urgency_score > 0.6:
            category_indicator = "⚠️ HIGH: "
        elif urgency_score > 0.4:
            category_indicator = "📈 MEDIUM: "
        elif category == 'General':
            category_indicator = "📋 ROUTINE: "
        else:
            category_indicator = "📊 "
        
        # Add flags to subject if available
        flags = announcement.get('flags', [])
        flag_text = ""
        if flags:
            flag_names = flags[:2]  # Limit to first 2 flags
            flag_text = f" [{', '.join(flag_names)}]"
        
        return f"{category_indicator}BSE Alert - {company}{flag_text}"

    def create_html_content(self, announcement: Dict) -> str:
        """Create enhanced HTML email content with categorization."""
        basic_info = announcement.get('basic_info', {})
        urgency_analysis = announcement.get('urgency_analysis', {})
        confidence_analysis = announcement.get('confidence_analysis', {})
        sentiment_analysis = announcement.get('sentiment_analysis', {})
        financial_analysis = announcement.get('financial_analysis', {})
        risk_assessment = announcement.get('risk_assessment', {})
        impact_analysis = announcement.get('impact_analysis', {})
        email_decision = announcement.get('email_alert_decision', {})
        categorization = email_decision.get('categorization', {})
        
        # Extract data
        title = basic_info.get('title', 'Unknown Title')
        extracted_text = basic_info.get('extracted_text', '')
        urgency_score = urgency_analysis.get('score', 0)
        confidence_score = confidence_analysis.get('score', 0)
        sentiment = sentiment_analysis.get('combined', {}).get('overall', 'neutral')
        risk_level = risk_assessment.get('risk_level', 'low')
        impact_level = impact_analysis.get('impact_level', 'neutral')
        category = categorization.get('type', 'unknown')
        priority = categorization.get('priority', 'routine')
        
        # Get urgency color and category styling
        urgency_color = self.get_urgency_color(urgency_score)
        category_style = self.get_category_style(category, priority)
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .alert-box {{ background: #f8f9fa; border-left: 4px solid {urgency_color}; 
                   padding: 15px; margin: 15px 0; border-radius: 4px; }}
        .category-badge {{ display: inline-block; padding: 8px 16px; border-radius: 20px; 
                         color: white; font-weight: bold; margin: 10px 0; {category_style} }}
        .score-box {{ display: inline-block; background: #e9ecef; 
                   padding: 8px 12px; border-radius: 4px; margin: 5px; }}
        .flag {{ display: inline-block; background: #28a745; color: white; 
               padding: 4px 8px; border-radius: 12px; margin: 2px; font-size: 12px; }}
        .keyword {{ display: inline-block; background: #17a2b8; color: white; 
                 padding: 3px 6px; border-radius: 10px; margin: 2px; font-size: 11px; }}
        .metric {{ background: #fff3cd; border: 1px solid #ffeaa7; 
                 padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .risk-high {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }}
        .risk-medium {{ background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }}
        .risk-low {{ background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }}
        .impact-high {{ background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }}
        .impact-medium {{ background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }}
        .impact-low {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; 
                 font-size: 12px; color: #6c757d; }}
        .filter-info {{ background: #e2e3e5; border: 1px solid #d6d8db; 
                      padding: 10px; border-radius: 4px; margin: 10px 0; font-size: 12px; }}
        .routine-notice {{ background: #f8f9fa; border: 1px solid #dee2e6; 
                         padding: 10px; border-radius: 4px; margin: 10px 0; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>📧 BSE Announcement Alert</h2>
            <p><strong>Company:</strong> {title.split()[0] if title else 'Unknown'}</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="category-badge">
            {self.get_category_icon(category)} {category.upper()} - {priority.upper()}
        </div>
        
        {self.get_routine_notice_html(category, priority)}
        
        <div class="alert-box">
            <h3>📋 Announcement Details</h3>
            <p><strong>Title:</strong> {title}</p>
            {f'<p><strong>Content:</strong> {extracted_text[:200]}{"..." if len(extracted_text) > 200 else ""}</p>' if extracted_text else ''}
        </div>
        
        <div class="metric">
            <h3>📊 Analysis Scores</h3>
            <div class="score-box">
                <strong>Urgency Score:</strong> {urgency_score:.2f}
            </div>
            <div class="score-box">
                <strong>Confidence Score:</strong> {confidence_score:.2f}
            </div>
            <div class="score-box">
                <strong>Sentiment:</strong> {sentiment.title()}
            </div>
            <div class="score-box risk-{risk_level}">
                <strong>Risk Level:</strong> {risk_level.title()}
            </div>
            <div class="score-box impact-{impact_level}">
                <strong>Market Impact:</strong> {impact_level.title()}
            </div>
        </div>
        
        {self.generate_flags_html(urgency_analysis)}
        {self.generate_financial_html(financial_analysis)}
        {self.generate_contributing_factors_html(urgency_analysis)}
        {self.generate_categorization_html(email_decision)}
        
        <div class="footer">
            <p><strong>BSE Monitor Service</strong></p>
            <p>This alert was automatically generated based on sophisticated analysis.</p>
            <p>Processing time: {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_template

    def create_text_content(self, announcement: Dict) -> str:
        """Create plain text email content."""
        company = announcement.get('company', 'Unknown Company')
        title = announcement.get('title', 'Unknown Title')
        
        # Clean up template text
        if '{{' in company:
            company = 'BSE Company'
        if '{{' in title:
            title = 'Announcement'
        
        text_content = f"""
BSE CORPORATE ANNOUNCEMENT ALERT
================================

Company: {company}
Time: {announcement.get('timestamp', 'Unknown')}
Category: {announcement.get('category', 'General')}

"""
        
        if title and title != 'Unknown Title':
            text_content += f"Title: {title}\n\n"
        
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

    def get_urgency_color(self, urgency_score: float) -> str:
        """Get color based on urgency score."""
        if urgency_score > 0.8:
            return "#dc3545"  # Red
        elif urgency_score > 0.6:
            return "#fd7e14"  # Orange
        elif urgency_score > 0.4:
            return "#ffc107"  # Yellow
        else:
            return "#28a745"  # Green

    def generate_flags_html(self, urgency_analysis: Dict) -> str:
        """Generate HTML for flags section."""
        flags = urgency_analysis.get('flags', [])
        if not flags:
            return ""
        
        flags_html = '<div class="metric"><h3>🚩 Detected Flags</h3>'
        for flag in flags:
            flag_name = flag.get('flag', '')
            flag_score = flag.get('score', 0)
            keywords = flag.get('keywords', [])
            flags_html += f'''
                <div class="flag">
                    {flag_name} (Score: {flag_score:.2f})
                    <br><small>Keywords: {', '.join(keywords[:3])}</small>
                </div>'''
        flags_html += '</div>'
        return flags_html

    def generate_financial_html(self, financial_analysis: Dict) -> str:
        """Generate HTML for financial data section."""
        structured_data = financial_analysis.get('structured_data', {})
        amounts = financial_analysis.get('amounts', [])
        
        if not structured_data and not amounts:
            return ""
        
        financial_html = '<div class="metric"><h3>💰 Financial Data</h3>'
        
        if structured_data:
            financial_html += '<h4>Structured Data:</h4>'
            for key, value in structured_data.items():
                if isinstance(value, (int, float)) and value > 0:
                    if value >= 10000000:  # 1 crore
                        formatted_value = f"₹{value/10000000:.2f} Cr"
                    elif value >= 100000:  # 1 lakh
                        formatted_value = f"₹{value/100000:.2f} L"
                    else:
                        formatted_value = f"₹{value:,.2f}"
                    financial_html += f'<div class="keyword">{key}: {formatted_value}</div>'
        
        if amounts:
            financial_html += '<h4>Extracted Amounts:</h4>'
            for amount_info in amounts[:5]:  # Limit to first 5
                value = amount_info.get('value', 0)
                currency = amount_info.get('currency', 'INR')
                if value > 0:
                    if value >= 10000000:  # 1 crore
                        formatted_value = f"₹{value/10000000:.2f} Cr"
                    elif value >= 100000:  # 1 lakh
                        formatted_value = f"₹{value/100000:.2f} L"
                    else:
                        formatted_value = f"₹{value:,.2f}"
                    financial_html += f'<div class="keyword">{formatted_value} ({currency})</div>'
        
        financial_html += '</div>'
        return financial_html

    def generate_contributing_factors_html(self, urgency_analysis: Dict) -> str:
        """Generate HTML for contributing factors section."""
        factors = urgency_analysis.get('contributing_factors', [])
        if not factors:
            return ""
        
        factors_html = '<div class="metric"><h3>🔍 Contributing Factors</h3>'
        for factor in factors:
            factors_html += f'<div class="keyword">{factor}</div>'
        factors_html += '</div>'
        return factors_html

    def generate_categorization_html(self, email_decision: Dict) -> str:
        """Generate HTML for categorization information."""
        categorization = email_decision.get('categorization', {})
        reasons = email_decision.get('reasons', {})
        
        if not categorization:
            return ""
        
        category = categorization.get('type', 'unknown')
        priority = categorization.get('priority', 'routine')
        should_highlight = categorization.get('should_highlight', False)
        
        cat_html = f'<div class="filter-info"><h3>🏷️ Announcement Categorization</h3>'
        
        # Show category and priority
        cat_html += f'<p><strong>Category:</strong> {category.title()}</p>'
        cat_html += f'<p><strong>Priority:</strong> {priority.replace("_", " ").title()}</p>'
        
        if should_highlight:
            cat_html += '<p><strong>💡 Highlight:</strong> This announcement may require immediate attention</p>'
        
        # Show classification reasons
        cat_html += '<h4>Classification Factors:</h4>'
        for reason, is_true in reasons.items():
            if reason.startswith('is_'):
                status = "✅" if is_true else "❌"
                reason_name = reason.replace('is_', '').replace('_', ' ').title()
                cat_html += f'<div>{status} {reason_name}</div>'
        
        cat_html += '</div>'
        return cat_html
    
    def get_category_style(self, category: str, priority: str = None) -> str:
        """Get CSS style for category."""
        styles = {
            'important': 'background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;',
            'routine': 'background-color: #e2e3e5; color: #383d41; border: 1px solid #d6d8db;',
            'technical': 'background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb;',
            'administrative': 'background-color: #fff3cd; color: #856404; border: 1px solid #ffeaa7;',
            'unknown': 'background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;'
        }
        return styles.get(category, styles['unknown'])
    
    def get_category_icon(self, category: str) -> str:
        """Get icon for category."""
        icons = {
            'important': '🚨',
            'routine': '📋',
            'technical': '🔧',
            'administrative': '📝',
            'unknown': '📊'
        }
        return icons.get(category, '📊')
    
    def get_routine_notice_html(self, category: str, priority: str) -> str:
        """Get HTML for routine notice."""
        if category == 'routine' and priority == 'routine':
            return '''
            <div class="routine-notice">
                <strong>📋 Routine Notice:</strong> This is a routine announcement that may not require immediate action.
            </div>
            '''
        return "" 