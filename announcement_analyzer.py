import re
from typing import Dict, List, Tuple
import logging
from textblob import TextBlob
from config import URGENCY_KEYWORDS, CONFIDENCE_WEIGHTS

class AnnouncementAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze(self, announcement: Dict) -> Dict:
        """Analyze an announcement and return analysis results."""
        try:
            # Combine all text content for analysis
            text_content = self.combine_text_content(announcement)
            
            # Extract keywords
            keywords = self.extract_keywords(text_content)
            
            # Generate flags
            flags = self.generate_flags(text_content)
            
            # Calculate urgency score
            urgency_score = self.calculate_urgency_score(text_content, flags)
            
            # Calculate confidence score
            confidence_score = self.calculate_confidence_score(announcement, keywords)
            
            # Extract key metrics
            key_metrics = self.extract_key_metrics(text_content)
            
            return {
                'keywords': keywords,
                'flags': flags,
                'urgency_score': urgency_score,
                'confidence_score': confidence_score,
                'key_metrics': key_metrics,
                'sentiment': self.analyze_sentiment(text_content)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing announcement: {e}")
            return {
                'keywords': [],
                'flags': [],
                'urgency_score': 0.0,
                'confidence_score': 0.0,
                'key_metrics': {},
                'sentiment': 'neutral'
            }

    def combine_text_content(self, announcement: Dict) -> str:
        """Combine all text content from the announcement."""
        text_parts = []
        
        # Add title
        if announcement.get('title'):
            text_parts.append(announcement['title'])
        
        # Add announcement text from XBRL
        if announcement.get('announcement_text'):
            text_parts.append(announcement['announcement_text'])
        
        # Add financial data as text
        if announcement.get('financial_data'):
            for key, value in announcement['financial_data'].items():
                text_parts.append(f"{key}: {value}")
        
        return ' '.join(text_parts).lower()

    def extract_keywords(self, text_content: str) -> List[str]:
        """Extract important keywords from the text."""
        keywords = []
        
        # Financial keywords
        financial_patterns = [
            r'₹\s*([\d,]+\.?\d*)',
            r'(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*(?:crore|cr|lakh|lk|million|mn)',
            r'(?:order|contract|deal|project)\s*(?:worth|value|of)\s*₹\s*([\d,]+)',
            r'(?:profit|revenue|earnings)\s*(?:of|worth)\s*₹\s*([\d,]+)',
            r'(?:growth|increase|surge)\s*of\s*(\d+\.?\d*)\s*%',
        ]
        
        for pattern in financial_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                keywords.append(match)
        
        # Business keywords
        business_keywords = [
            'MoD', 'defense', 'government', 'tender', 'bid', 'order win',
            'quarterly results', 'annual results', 'dividend', 'bonus',
            'merger', 'acquisition', 'investment', 'funding'
        ]
        
        for keyword in business_keywords:
            if keyword.lower() in text_content:
                keywords.append(keyword)
        
        # Remove duplicates and limit to top 10
        return list(set(keywords))[:10]

    def generate_flags(self, text_content: str) -> List[str]:
        """Generate flags based on keyword matches."""
        flags = []
        
        for flag_name, keywords in URGENCY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_content:
                    flags.append(flag_name)
                    break  # Only add each flag once
        
        return flags

    def calculate_urgency_score(self, text_content: str, flags: List[str]) -> float:
        """Calculate urgency score based on content analysis."""
        score = 0.0
        
        # Base score from flags
        score += len(flags) * 0.2
        
        # Financial impact indicators
        if re.search(r'₹\s*[\d,]+', text_content):
            score += 0.3
        
        # Percentage indicators
        if re.search(r'\d+\.?\d*\s*%', text_content):
            score += 0.2
        
        # Time-sensitive keywords
        urgent_keywords = ['urgent', 'immediate', 'breaking', 'important', 'critical']
        for keyword in urgent_keywords:
            if keyword in text_content:
                score += 0.2
        
        # Large numbers (crore/lakh)
        if re.search(r'\d+\s*(?:crore|cr|lakh|lk)', text_content):
            score += 0.2
        
        # Government/defense related
        if any(keyword in text_content for keyword in ['mod', 'defense', 'government']):
            score += 0.3
        
        return min(score, 1.0)  # Cap at 1.0

    def calculate_confidence_score(self, announcement: Dict, keywords: List[str]) -> float:
        """Calculate confidence score for the analysis."""
        score = 0.0
        
        # Keyword match confidence
        if keywords:
            score += CONFIDENCE_WEIGHTS['keyword_match']
        
        # Company size confidence (larger companies tend to have better structured data)
        company_name = announcement.get('company', '').lower()
        if any(large_company in company_name for large_company in ['ltd', 'limited', 'corporation']):
            score += CONFIDENCE_WEIGHTS['company_size']
        
        # Announcement type confidence
        category = announcement.get('category', '').lower()
        if category in ['financial results', 'board meeting', 'corporate action']:
            score += CONFIDENCE_WEIGHTS['announcement_type']
        
        # Time sensitivity confidence
        timestamp = announcement.get('timestamp', '')
        if timestamp and 'today' in timestamp.lower():
            score += CONFIDENCE_WEIGHTS['time_sensitivity']
        
        return min(score, 1.0)  # Cap at 1.0

    def extract_key_metrics(self, text_content: str) -> Dict:
        """Extract key business metrics from text."""
        metrics = {}
        
        # Order values
        order_matches = re.findall(r'order.*?₹\s*([\d,]+)', text_content, re.IGNORECASE)
        if order_matches:
            try:
                metrics['order_value'] = float(order_matches[0].replace(',', ''))
            except ValueError:
                pass
        
        # Growth percentages
        growth_matches = re.findall(r'(\d+\.?\d*)\s*%.*?(?:growth|increase)', text_content, re.IGNORECASE)
        if growth_matches:
            try:
                metrics['growth_rate'] = float(growth_matches[0])
            except ValueError:
                pass
        
        # Revenue amounts
        revenue_matches = re.findall(r'revenue.*?₹\s*([\d,]+)', text_content, re.IGNORECASE)
        if revenue_matches:
            try:
                metrics['revenue'] = float(revenue_matches[0].replace(',', ''))
            except ValueError:
                pass
        
        return metrics

    def analyze_sentiment(self, text_content: str) -> str:
        """Analyze sentiment of the announcement."""
        try:
            blob = TextBlob(text_content)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return 'neutral'

    def format_announcement_summary(self, announcement: Dict) -> str:
        """Format announcement data for email summary."""
        summary_parts = []
        
        # Company and timestamp
        summary_parts.append(f"**Company:** {announcement.get('company', 'Unknown')}")
        summary_parts.append(f"**Time:** {announcement.get('timestamp', 'Unknown')}")
        
        # Title
        if announcement.get('title'):
            summary_parts.append(f"**Title:** {announcement['title']}")
        
        # Flags
        if announcement.get('flags'):
            flags_text = ' '.join(announcement['flags'])
            summary_parts.append(f"**Flags:** {flags_text}")
        
        # Key metrics
        if announcement.get('key_metrics'):
            metrics_text = ', '.join([f"{k}: {v}" for k, v in announcement['key_metrics'].items()])
            summary_parts.append(f"**Key Metrics:** {metrics_text}")
        
        # Keywords
        if announcement.get('keywords'):
            keywords_text = ', '.join(announcement['keywords'][:5])  # Top 5 keywords
            summary_parts.append(f"**Keywords:** {keywords_text}")
        
        # Scores
        summary_parts.append(f"**Urgency Score:** {announcement.get('urgency_score', 0):.2f}")
        summary_parts.append(f"**Confidence Score:** {announcement.get('confidence_score', 0):.2f}")
        
        return '\n'.join(summary_parts) 