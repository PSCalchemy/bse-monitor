import xml.etree.ElementTree as ET
import re
from typing import Dict, Optional, List, Any
import logging
from datetime import datetime
import json

class XBRLParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Enhanced XBRL namespaces for Indian market
        self.namespaces = {
            'xbrl': 'http://www.xbrl.org/2003/instance',
            'xbrli': 'http://www.xbrl.org/2003/instance',
            'xbrldi': 'http://xbrl.org/2006/xbrldi',
            'link': 'http://www.xbrl.org/2003/linkbase',
            'xlink': 'http://www.w3.org/1999/xlink',
            'schema': 'http://www.w3.org/2001/XMLSchema',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'ind-as': 'http://www.xbrl.org/in/2017/ind-as',
            'ind': 'http://www.xbrl.org/in/2017/ind',
            'dei': 'http://xbrl.sec.gov/dei/2014-01-31',
            'us-gaap': 'http://fasb.org/us-gaap/2017-01-31'
        }
        
        # Indian XBRL taxonomy elements
        self.indian_taxonomy = {
            'financial_metrics': [
                'RevenueFromOperations', 'TotalRevenue', 'ProfitBeforeTax', 'ProfitAfterTax',
                'EarningsPerShare', 'BookValuePerShare', 'NetWorth', 'TotalAssets',
                'TotalLiabilities', 'CashAndCashEquivalents', 'NetCashFlow',
                'DividendPerShare', 'MarketCapitalization', 'DebtToEquityRatio'
            ],
            'business_events': [
                'OrderReceived', 'ContractAwarded', 'ProjectCompletion', 'InvestmentMade',
                'AcquisitionAnnounced', 'MergerAnnounced', 'DividendDeclared',
                'BonusIssue', 'RightsIssue', 'BuybackAnnounced'
            ],
            'company_identifiers': [
                'EntityRegistrantName', 'EntityCentralIndexKey', 'EntityFilerCategory',
                'TradingSymbol', 'ISIN', 'CIN', 'PAN'
            ]
        }

    def parse(self, xbrl_content: str) -> Dict:
        """Enhanced XBRL parsing with schema awareness and better accuracy."""
        try:
            root = ET.fromstring(xbrl_content)
            
            # Extract comprehensive information
            parsed_data = {
                'announcement_text': self.extract_announcement_text(root),
                'financial_data': self.extract_financial_data_enhanced(root),
                'company_info': self.extract_company_info_enhanced(root),
                'dates': self.extract_dates_enhanced(root),
                'amounts': self.extract_amounts_enhanced(root),
                'percentages': self.extract_percentages_enhanced(root),
                'business_events': self.extract_business_events(root),
                'context_info': self.extract_context_info(root),
                'metadata': self.extract_metadata(root)
            }
            
            # Add derived metrics
            parsed_data['derived_metrics'] = self.calculate_derived_metrics(parsed_data)
            
            return parsed_data
            
        except ET.ParseError as e:
            self.logger.error(f"Error parsing XBRL: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error parsing XBRL: {e}")
            return {}

    def extract_announcement_text(self, root) -> str:
        """Enhanced text extraction with better filtering and context."""
        text_elements = []
        
        # Priority elements for announcement text
        priority_elements = [
            './/*[contains(local-name(), "Description")]',
            './/*[contains(local-name(), "Text")]',
            './/*[contains(local-name(), "Narrative")]',
            './/*[contains(local-name(), "Note")]',
            './/*[contains(local-name(), "Disclosure")]'
        ]
        
        # Extract from priority elements first
        for xpath in priority_elements:
            for elem in root.xpath(xpath, namespaces=self.namespaces):
                if elem.text and elem.text.strip():
                    text = elem.text.strip()
                    if len(text) > 30:  # More meaningful threshold
                        text_elements.append(text)
        
        # Fallback to general text extraction
        if not text_elements:
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    text = elem.text.strip()
                    if len(text) > 30 and not self.is_technical_xbrl_text(text):
                        text_elements.append(text)
        
        return ' '.join(text_elements[:3])  # Limit to most relevant texts

    def is_technical_xbrl_text(self, text: str) -> bool:
        """Filter out technical XBRL metadata text."""
        technical_patterns = [
            r'^[A-Z]{2,10}$',  # Short codes
            r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',  # Dates only
            r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$',  # ISIN patterns
            r'^[A-Z]{3}[0-9]{6}[A-Z]{1}$',  # CIN patterns
        ]
        
        for pattern in technical_patterns:
            if re.match(pattern, text):
                return True
        return False

    def extract_financial_data_enhanced(self, root) -> Dict:
        """Enhanced financial data extraction with taxonomy awareness."""
        financial_data = {}
        
        # Look for taxonomy-specific elements
        for metric in self.indian_taxonomy['financial_metrics']:
            # Search with different namespace prefixes
            for ns_prefix in ['ind-as', 'ind', 'us-gaap', '']:
                xpath_patterns = [
                    f'.//*[local-name()="{metric}"]',
                    f'.//*[contains(local-name(), "{metric}")]',
                    f'.//*[contains(local-name(), "{metric.lower()}")]'
                ]
                
                for xpath in xpath_patterns:
                    elements = root.xpath(xpath, namespaces=self.namespaces)
                    for elem in elements:
                        value = self.extract_numeric_value(elem)
                        if value is not None:
                            financial_data[metric] = value
                            break
        
        # Fallback to pattern-based extraction
        if not financial_data:
            financial_data = self.extract_financial_data_patterns(root)
        
        return financial_data

    def extract_numeric_value(self, elem) -> Optional[float]:
        """Extract and validate numeric values from XBRL elements."""
        if not elem.text:
            return None
            
        text = elem.text.strip()
        
        # Handle different number formats
        number_patterns = [
            r'^([+-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)$',  # Standard numbers
            r'^([+-]?\d+(?:\.\d+)?)\s*(?:crore|cr|lakh|lk|million|mn|thousand|k)?$',  # With units
            r'^([+-]?\d+(?:\.\d+)?)\s*%$',  # Percentages
        ]
        
        for pattern in number_patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1).replace(',', ''))
                    
                    # Apply unit multipliers
                    if 'crore' in text.lower() or 'cr' in text.lower():
                        value *= 10000000
                    elif 'lakh' in text.lower() or 'lk' in text.lower():
                        value *= 100000
                    elif 'million' in text.lower() or 'mn' in text.lower():
                        value *= 1000000
                    elif 'thousand' in text.lower() or 'k' in text.lower():
                        value *= 1000
                    
                    return value
                except ValueError:
                    continue
        
        return None

    def extract_financial_data_patterns(self, root) -> Dict:
        """Fallback pattern-based financial data extraction."""
        financial_data = {}
        
        # Enhanced financial patterns with context
        financial_patterns = {
            'revenue': ['revenue', 'turnover', 'sales', 'income'],
            'profit': ['profit', 'earnings', 'net_income', 'PAT', 'EBITDA'],
            'assets': ['assets', 'total_assets', 'current_assets', 'fixed_assets'],
            'liabilities': ['liabilities', 'debt', 'borrowings', 'payables'],
            'equity': ['equity', 'shareholders_equity', 'net_worth'],
            'cash': ['cash', 'cash_equivalents', 'bank_balance'],
            'dividend': ['dividend', 'dividend_per_share', 'DPS'],
            'eps': ['eps', 'earnings_per_share', 'basic_eps', 'diluted_eps'],
            'book_value': ['book_value', 'book_value_per_share', 'BVPS'],
            'market_cap': ['market_cap', 'market_capitalization', 'market_value']
        }
        
        for category, patterns in financial_patterns.items():
            for elem in root.iter():
                tag = elem.tag.lower()
                for pattern in patterns:
                    if pattern in tag:
                        value = self.extract_numeric_value(elem)
                        if value is not None:
                            financial_data[category] = value
                            break
                if category in financial_data:
                    break
        
        return financial_data

    def extract_company_info_enhanced(self, root) -> Dict:
        """Enhanced company information extraction."""
        company_info = {}
        
        # Look for taxonomy-specific company identifiers
        for identifier in self.indian_taxonomy['company_identifiers']:
            xpath_patterns = [
                f'.//*[local-name()="{identifier}"]',
                f'.//*[contains(local-name(), "{identifier}")]'
            ]
            
            for xpath in xpath_patterns:
                elements = root.xpath(xpath, namespaces=self.namespaces)
                for elem in elements:
                    if elem.text and elem.text.strip():
                        company_info[identifier] = elem.text.strip()
                        break
        
        # Fallback to general company info extraction
        if not company_info:
            company_info = self.extract_company_info_general(root)
        
        return company_info

    def extract_company_info_general(self, root) -> Dict:
        """General company information extraction."""
        company_info = {}
        
        company_keywords = ['company', 'entity', 'name', 'identifier', 'symbol', 'isin', 'cin']
        
        for elem in root.iter():
            tag = elem.tag.lower()
            if any(keyword in tag for keyword in company_keywords):
                if elem.text and elem.text.strip():
                    clean_tag = tag.split('}')[-1] if '}' in tag else tag
                    company_info[clean_tag] = elem.text.strip()
        
        return company_info

    def extract_dates_enhanced(self, root) -> List[Dict]:
        """Enhanced date extraction with context."""
        dates = []
        
        # Look for specific date elements
        date_elements = [
            'DocumentPeriodEndDate', 'DocumentFilingDate', 'PeriodEndDate',
            'BalanceSheetDate', 'StatementDate', 'AnnouncementDate'
        ]
        
        for date_elem in date_elements:
            xpath_patterns = [
                f'.//*[local-name()="{date_elem}"]',
                f'.//*[contains(local-name(), "{date_elem}")]'
            ]
            
            for xpath in xpath_patterns:
                elements = root.xpath(xpath, namespaces=self.namespaces)
                for elem in elements:
                    if elem.text and elem.text.strip():
                        date_str = elem.text.strip()
                        parsed_date = self.parse_date(date_str)
                        if parsed_date:
                            dates.append({
                                'type': date_elem,
                                'value': date_str,
                                'parsed': parsed_date.isoformat()
                            })
        
        return dates

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats."""
        date_patterns = [
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%d-%m-%y',
            '%d/%m/%y'
        ]
        
        for pattern in date_patterns:
            try:
                return datetime.strptime(date_str, pattern)
            except ValueError:
                continue
        
        return None

    def extract_amounts_enhanced(self, root) -> List[Dict]:
        """Enhanced amount extraction with context."""
        amounts = []
        
        # Enhanced amount patterns
        amount_patterns = [
            (r'₹\s*([\d,]+\.?\d*)', 'INR'),
            (r'Rs\.\s*([\d,]+\.?\d*)', 'INR'),
            (r'INR\s*([\d,]+\.?\d*)', 'INR'),
            (r'USD\s*([\d,]+\.?\d*)', 'USD'),
            (r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(crore|cr)', 'INR_CRORE'),
            (r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(lakh|lk)', 'INR_LAKH'),
            (r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(million|mn)', 'USD_MILLION'),
        ]
        
        for elem in root.iter():
            if elem.text:
                for pattern, currency in amount_patterns:
                    matches = re.findall(pattern, elem.text, re.IGNORECASE)
                    for match in matches:
                        try:
                            if isinstance(match, tuple):
                                value_str, unit = match
                            else:
                                value_str = match
                                unit = None
                            
                            clean_amount = value_str.replace(',', '')
                            amount = float(clean_amount)
                            
                            # Apply unit multipliers
                            if currency == 'INR_CRORE':
                                amount *= 10000000
                                currency = 'INR'
                            elif currency == 'INR_LAKH':
                                amount *= 100000
                                currency = 'INR'
                            elif currency == 'USD_MILLION':
                                amount *= 1000000
                                currency = 'USD'
                            
                            amounts.append({
                                'value': amount,
                                'currency': currency,
                                'unit': unit,
                                'context': elem.tag
                            })
                        except ValueError:
                            continue
        
        return amounts

    def extract_percentages_enhanced(self, root) -> List[Dict]:
        """Enhanced percentage extraction with context."""
        percentages = []
        
        # Enhanced percentage patterns
        percentage_patterns = [
            (r'(\d+\.?\d*)\s*%', 'standard'),
            (r'(\d+\.?\d*)\s*percent', 'standard'),
            (r'increase\s*of\s*(\d+\.?\d*)', 'increase'),
            (r'growth\s*of\s*(\d+\.?\d*)', 'growth'),
            (r'decrease\s*of\s*(\d+\.?\d*)', 'decrease'),
            (r'decline\s*of\s*(\d+\.?\d*)', 'decline'),
            (r'(\d+\.?\d*)\s*%\s*increase', 'increase'),
            (r'(\d+\.?\d*)\s*%\s*decrease', 'decrease'),
        ]
        
        for elem in root.iter():
            if elem.text:
                for pattern, ptype in percentage_patterns:
                    matches = re.findall(pattern, elem.text, re.IGNORECASE)
                    for match in matches:
                        try:
                            percentage = float(match)
                            percentages.append({
                                'value': percentage,
                                'type': ptype,
                                'context': elem.tag
                            })
                        except ValueError:
                            continue
        
        return percentages

    def extract_business_events(self, root) -> List[Dict]:
        """Extract business events from XBRL."""
        events = []
        
        for event in self.indian_taxonomy['business_events']:
            xpath_patterns = [
                f'.//*[local-name()="{event}"]',
                f'.//*[contains(local-name(), "{event}")]'
            ]
            
            for xpath in xpath_patterns:
                elements = root.xpath(xpath, namespaces=self.namespaces)
                for elem in elements:
                    if elem.text and elem.text.strip():
                        events.append({
                            'type': event,
                            'value': elem.text.strip(),
                            'context': elem.tag
                        })
        
        return events

    def extract_context_info(self, root) -> Dict:
        """Extract XBRL context information."""
        context_info = {}
        
        # Look for context elements
        context_elements = root.findall('.//xbrli:context', namespaces=self.namespaces)
        
        for context in context_elements:
            context_id = context.get('id', 'unknown')
            period_elem = context.find('.//xbrli:period', namespaces=self.namespaces)
            
            if period_elem is not None:
                start_date = period_elem.find('.//xbrli:startDate', namespaces=self.namespaces)
                end_date = period_elem.find('.//xbrli:endDate', namespaces=self.namespaces)
                
                context_info[context_id] = {
                    'start_date': start_date.text if start_date is not None else None,
                    'end_date': end_date.text if end_date is not None else None
                }
        
        return context_info

    def extract_metadata(self, root) -> Dict:
        """Extract XBRL metadata."""
        metadata = {}
        
        # Extract schema information
        schema_ref = root.find('.//link:schemaRef', namespaces=self.namespaces)
        if schema_ref is not None:
            metadata['schema_href'] = schema_ref.get('{http://www.w3.org/1999/xlink}href')
        
        # Extract namespace information
        metadata['namespaces'] = root.nsmap if hasattr(root, 'nsmap') else {}
        
        return metadata

    def calculate_derived_metrics(self, parsed_data: Dict) -> Dict:
        """Calculate derived financial metrics."""
        derived = {}
        financial = parsed_data.get('financial_data', {})
        
        # Calculate ratios if we have the required data
        if 'revenue' in financial and 'profit' in financial and financial['revenue'] > 0:
            derived['profit_margin'] = (financial['profit'] / financial['revenue']) * 100
        
        if 'assets' in financial and 'liabilities' in financial and financial['assets'] > 0:
            derived['debt_to_assets'] = financial['liabilities'] / financial['assets']
        
        if 'equity' in financial and 'liabilities' in financial and financial['equity'] > 0:
            derived['debt_to_equity'] = financial['liabilities'] / financial['equity']
        
        return derived

    def extract_key_metrics(self, xbrl_content: str) -> Dict:
        """Enhanced key metrics extraction."""
        try:
            parsed_data = self.parse(xbrl_content)
            metrics = {}
            
            # Extract from structured financial data
            financial_data = parsed_data.get('financial_data', {})
            for key, value in financial_data.items():
                if isinstance(value, (int, float)):
                    metrics[key] = value
            
            # Extract from amounts
            amounts = parsed_data.get('amounts', [])
            for amount_info in amounts:
                if amount_info['value'] > 0:
                    metrics[f"amount_{len(metrics)}"] = amount_info['value']
            
            # Extract from percentages
            percentages = parsed_data.get('percentages', [])
            for pct_info in percentages:
                if pct_info['value'] > 0:
                    metrics[f"percentage_{len(metrics)}"] = pct_info['value']
            
            # Add derived metrics
            derived = parsed_data.get('derived_metrics', {})
            metrics.update(derived)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error extracting key metrics: {e}")
            return {} 