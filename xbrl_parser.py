import xml.etree.ElementTree as ET
import re
from typing import Dict, Optional, List
import logging

class XBRLParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common XBRL namespaces
        self.namespaces = {
            'xbrl': 'http://www.xbrl.org/2003/instance',
            'xbrli': 'http://www.xbrl.org/2003/instance',
            'xbrldi': 'http://xbrl.org/2006/xbrldi',
            'link': 'http://www.xbrl.org/2003/linkbase',
            'xlink': 'http://www.w3.org/1999/xlink',
            'schema': 'http://www.w3.org/2001/XMLSchema',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

    def parse(self, xbrl_content: str) -> Dict:
        """Parse XBRL content and extract relevant information."""
        try:
            root = ET.fromstring(xbrl_content)
            
            # Extract basic information
            parsed_data = {
                'announcement_text': self.extract_announcement_text(root),
                'financial_data': self.extract_financial_data(root),
                'company_info': self.extract_company_info(root),
                'dates': self.extract_dates(root),
                'amounts': self.extract_amounts(root),
                'percentages': self.extract_percentages(root)
            }
            
            return parsed_data
            
        except ET.ParseError as e:
            self.logger.error(f"Error parsing XBRL: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error parsing XBRL: {e}")
            return {}

    def extract_announcement_text(self, root) -> str:
        """Extract the main announcement text from XBRL."""
        text_elements = []
        
        # Look for text content in various XBRL elements
        for elem in root.iter():
            if elem.text and elem.text.strip():
                text = elem.text.strip()
                if len(text) > 20:  # Only meaningful text
                    text_elements.append(text)
        
        return ' '.join(text_elements[:5])  # Limit to first 5 meaningful texts

    def extract_financial_data(self, root) -> Dict:
        """Extract financial metrics from XBRL."""
        financial_data = {}
        
        # Common financial element patterns
        financial_patterns = [
            'revenue', 'profit', 'earnings', 'income', 'expense',
            'assets', 'liabilities', 'equity', 'cash', 'debt',
            'dividend', 'eps', 'pe', 'book_value', 'market_cap'
        ]
        
        for elem in root.iter():
            tag = elem.tag.lower()
            for pattern in financial_patterns:
                if pattern in tag:
                    value = elem.text
                    if value and value.strip():
                        try:
                            # Try to convert to number
                            num_value = float(value.replace(',', ''))
                            financial_data[pattern] = num_value
                        except ValueError:
                            financial_data[pattern] = value.strip()
        
        return financial_data

    def extract_company_info(self, root) -> Dict:
        """Extract company information from XBRL."""
        company_info = {}
        
        # Look for company identifiers and names
        for elem in root.iter():
            tag = elem.tag.lower()
            if any(keyword in tag for keyword in ['company', 'entity', 'name', 'identifier']):
                if elem.text and elem.text.strip():
                    company_info[tag.split('}')[-1]] = elem.text.strip()
        
        return company_info

    def extract_dates(self, root) -> List[str]:
        """Extract dates from XBRL."""
        dates = []
        
        # Date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
        ]
        
        for elem in root.iter():
            if elem.text:
                for pattern in date_patterns:
                    matches = re.findall(pattern, elem.text)
                    dates.extend(matches)
        
        return list(set(dates))  # Remove duplicates

    def extract_amounts(self, root) -> List[float]:
        """Extract monetary amounts from XBRL."""
        amounts = []
        
        # Amount patterns (with currency symbols and commas)
        amount_patterns = [
            r'₹\s*([\d,]+\.?\d*)',
            r'Rs\.\s*([\d,]+\.?\d*)',
            r'INR\s*([\d,]+\.?\d*)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:crore|cr|lakh|lk|million|mn)',
        ]
        
        for elem in root.iter():
            if elem.text:
                for pattern in amount_patterns:
                    matches = re.findall(pattern, elem.text, re.IGNORECASE)
                    for match in matches:
                        try:
                            # Clean and convert to float
                            clean_amount = match.replace(',', '')
                            amount = float(clean_amount)
                            amounts.append(amount)
                        except ValueError:
                            continue
        
        return amounts

    def extract_percentages(self, root) -> List[float]:
        """Extract percentage values from XBRL."""
        percentages = []
        
        # Percentage patterns
        percentage_patterns = [
            r'(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*percent',
            r'increase\s*of\s*(\d+\.?\d*)',
            r'growth\s*of\s*(\d+\.?\d*)',
        ]
        
        for elem in root.iter():
            if elem.text:
                for pattern in percentage_patterns:
                    matches = re.findall(pattern, elem.text, re.IGNORECASE)
                    for match in matches:
                        try:
                            percentage = float(match)
                            percentages.append(percentage)
                        except ValueError:
                            continue
        
        return percentages

    def extract_key_metrics(self, xbrl_content: str) -> Dict:
        """Extract key business metrics from XBRL."""
        try:
            root = ET.fromstring(xbrl_content)
            metrics = {}
            
            # Look for specific business metrics
            metric_patterns = {
                'order_value': [r'order.*?₹\s*([\d,]+)', r'contract.*?₹\s*([\d,]+)'],
                'growth_rate': [r'(\d+\.?\d*)\s*%.*?growth', r'(\d+\.?\d*)\s*%.*?increase'],
                'profit_margin': [r'profit.*?(\d+\.?\d*)\s*%', r'margin.*?(\d+\.?\d*)\s*%'],
                'revenue': [r'revenue.*?₹\s*([\d,]+)', r'turnover.*?₹\s*([\d,]+)'],
            }
            
            text_content = self.extract_announcement_text(root)
            
            for metric_name, patterns in metric_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, text_content, re.IGNORECASE)
                    if matches:
                        try:
                            value = float(matches[0].replace(',', ''))
                            metrics[metric_name] = value
                            break
                        except ValueError:
                            continue
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error extracting key metrics: {e}")
            return {} 