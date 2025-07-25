import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from textblob import TextBlob
import config
from xbrl_parser import XBRLParser

class AnnouncementAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.xbrl_parser = XBRLParser()
        
    def analyze_announcement(self, title: str, content: str, xbrl_content: str = None, 
                           company_info: Dict = None) -> Dict:
        """
        Comprehensive analysis of BSE announcement with enhanced XBRL parsing and filtering.
        
        Args:
            title: Announcement title
            content: Raw announcement content
            xbrl_content: XBRL content if available
            company_info: Company information dictionary
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        try:
            # Parse XBRL content if available
            xbrl_data = {}
            if xbrl_content:
                xbrl_data = self.xbrl_parser.parse(xbrl_content)
            
            # Combine all text content for analysis
            text_content = self.combine_text_content(title, content, xbrl_data)
            
            # Perform comprehensive analysis
            analysis_result = {
                'basic_info': self.extract_basic_info(title, content, xbrl_data),
                'financial_analysis': self.analyze_financial_data(xbrl_data, text_content),
                'keyword_analysis': self.analyze_keywords(text_content),
                'urgency_analysis': self.calculate_urgency_score(text_content, xbrl_data),
                'confidence_analysis': self.calculate_confidence_score(title, xbrl_data, company_info),
                'sentiment_analysis': self.analyze_sentiment(text_content),
                'business_events': self.extract_business_events(xbrl_data, text_content),
                'risk_assessment': self.assess_risks(text_content, xbrl_data),
                'impact_analysis': self.analyze_market_impact(text_content, xbrl_data),
                'metadata': self.extract_metadata(title, content, xbrl_data)
            }
            
            # Calculate overall scores
            analysis_result['overall_scores'] = self.calculate_overall_scores(analysis_result)
            
            # Add priority classification
            analysis_result['priority_classification'] = self.classify_announcement_priority(analysis_result)
            
            # Determine if email alert should be sent
            analysis_result['email_alert_decision'] = self.should_send_email_alert(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error analyzing announcement: {e}")
            return self.get_default_analysis()

    def combine_text_content(self, title: str, content: str, xbrl_data: Dict) -> str:
        """Combine all text content for comprehensive analysis."""
        text_parts = [title, content]
        
        # Add XBRL text content
        if xbrl_data.get('announcement_text'):
            text_parts.append(xbrl_data['announcement_text'])
        
        # Add financial data as text
        financial_text = self.convert_financial_data_to_text(xbrl_data.get('financial_data', {}))
        if financial_text:
            text_parts.append(financial_text)
        
        return ' '.join(text_parts)

    def convert_financial_data_to_text(self, financial_data: Dict) -> str:
        """Convert financial data to searchable text."""
        text_parts = []
        
        for key, value in financial_data.items():
            if isinstance(value, (int, float)):
                if value >= 10000000:  # 1 crore
                    text_parts.append(f"{key} ₹{value/10000000:.2f} crore")
                elif value >= 100000:  # 1 lakh
                    text_parts.append(f"{key} ₹{value/100000:.2f} lakh")
                else:
                    text_parts.append(f"{key} ₹{value:,.2f}")
        
        return ' '.join(text_parts)

    def extract_basic_info(self, title: str, content: str, xbrl_data: Dict) -> Dict:
        """Extract basic announcement information."""
        basic_info = {
            'title': title,
            'content_length': len(content),
            'has_xbrl_data': bool(xbrl_data),
            'announcement_type': self.classify_announcement_type(title, content),
            'company_info': xbrl_data.get('company_info', {}),
            'dates': xbrl_data.get('dates', []),
            'extracted_text': xbrl_data.get('announcement_text', '')
        }
        
        return basic_info

    def classify_announcement_type(self, title: str, content: str) -> str:
        """Classify the type of announcement."""
        text = f"{title} {content}".lower()
        
        type_patterns = {
            'quarterly_results': ['quarterly', 'q1', 'q2', 'q3', 'q4', 'quarter'],
            'annual_results': ['annual', 'yearly', 'financial year', 'fy'],
            'order_win': ['order', 'contract', 'win', 'award', 'project'],
            'dividend': ['dividend', 'dps', 'dividend per share'],
            'bonus': ['bonus', 'bonus issue', 'bonus shares'],
            'rights_issue': ['rights', 'rights issue', 'rights shares'],
            'buyback': ['buyback', 'buy back', 'share buyback'],
            'merger_acquisition': ['merger', 'acquisition', 'takeover', 'amalgamation'],
            'investment': ['investment', 'funding', 'capital'],
            'regulatory': ['regulatory', 'compliance', 'sebi', 'rbi'],
            'management_change': ['ceo', 'md', 'director', 'appointment', 'resignation']
        }
        
        for announcement_type, patterns in type_patterns.items():
            if any(pattern in text for pattern in patterns):
                return announcement_type
        
        return 'general'

    def analyze_financial_data(self, xbrl_data: Dict, text_content: str) -> Dict:
        """Analyze financial data from XBRL and text."""
        financial_analysis = {
            'structured_data': xbrl_data.get('financial_data', {}),
            'amounts': xbrl_data.get('amounts', []),
            'percentages': xbrl_data.get('percentages', []),
            'derived_metrics': xbrl_data.get('derived_metrics', {}),
            'extracted_patterns': self.extract_financial_patterns(text_content),
            'data_quality': self.assess_financial_data_quality(xbrl_data)
        }
        
        return financial_analysis

    def extract_financial_patterns(self, text_content: str) -> Dict:
        """Extract financial patterns from text using enhanced patterns."""
        patterns = config.FINANCIAL_PATTERNS
        extracted = {
            'currencies': [],
            'percentages': [],
            'dates': []
        }
        
        # Extract currency amounts
        for pattern in patterns['currency_patterns']:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    value_str, unit = match
                else:
                    value_str = match
                    unit = None
                
                try:
                    value = float(value_str.replace(',', ''))
                    extracted['currencies'].append({
                        'value': value,
                        'unit': unit,
                        'pattern': pattern
                    })
                except ValueError:
                    continue
        
        # Extract percentages
        for pattern in patterns['percentage_patterns']:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                try:
                    percentage = float(match)
                    extracted['percentages'].append({
                        'value': percentage,
                        'pattern': pattern
                    })
                except ValueError:
                    continue
        
        # Extract dates
        for pattern in patterns['date_patterns']:
            matches = re.findall(pattern, text_content)
            extracted['dates'].extend(matches)
        
        return extracted

    def assess_financial_data_quality(self, xbrl_data: Dict) -> str:
        """Assess the quality of financial data."""
        if not xbrl_data:
            return 'no_financial_data'
        
        financial_data = xbrl_data.get('financial_data', {})
        amounts = xbrl_data.get('amounts', [])
        percentages = xbrl_data.get('percentages', [])
        
        if financial_data and len(financial_data) > 5:
            return 'structured_xbrl'
        elif amounts or percentages:
            return 'partial_data'
        elif xbrl_data.get('announcement_text'):
            return 'unstructured_text'
        else:
            return 'no_financial_data'

    def analyze_keywords(self, text_content: str) -> Dict:
        """Analyze keywords using enhanced configuration."""
        keyword_analysis = {
            'flags': [],
            'keyword_matches': {},
            'financial_keywords': [],
            'business_keywords': []
        }
        
        text_lower = text_content.lower()
        
        # Analyze urgency keywords
        for flag_name, flag_config in config.URGENCY_KEYWORDS.items():
            keywords = flag_config['keywords']
            matches = []
            
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matches.append(keyword)
            
            if matches:
                keyword_analysis['flags'].append({
                    'flag': flag_name,
                    'keywords': matches,
                    'weight': flag_config['weight'],
                    'threshold': flag_config['financial_threshold']
                })
                keyword_analysis['keyword_matches'][flag_name] = matches
        
        # Extract financial keywords
        financial_patterns = [
            r'₹\s*([\d,]+\.?\d*)',
            r'(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*(crore|cr|lakh|lk|million|mn)'
        ]
        
        for pattern in financial_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            keyword_analysis['financial_keywords'].extend(matches)
        
        return keyword_analysis

    def calculate_urgency_score(self, text_content: str, xbrl_data: Dict) -> Dict:
        """Calculate urgency score using sophisticated algorithm with routine filtering."""
        urgency_analysis = {
            'score': 0.0,
            'flags': [],
            'contributing_factors': [],
            'financial_impact': 0.0,
            'routine_filters_applied': [],
            'high_value_boosts': []
        }
        
        # Calculate base urgency from keyword matches
        keyword_analysis = self.analyze_keywords(text_content)
        base_score = 0.0
        
        for flag_info in keyword_analysis['flags']:
            flag_score = len(flag_info['keywords']) * flag_info['weight'] * 0.1
            base_score += flag_score
            
            urgency_analysis['flags'].append({
                'flag': flag_info['flag'],
                'score': flag_score,
                'keywords': flag_info['keywords']
            })
        
        # Calculate financial impact
        financial_impact = self.calculate_financial_impact(xbrl_data, keyword_analysis)
        urgency_analysis['financial_impact'] = financial_impact
        
        # Adjust score based on financial thresholds
        for flag_info in keyword_analysis['flags']:
            if financial_impact >= flag_info['threshold']:
                base_score += flag_info['weight'] * 0.3
        
        # Apply routine announcement filters (reduce urgency)
        routine_reduction = self.apply_routine_filters(text_content)
        if routine_reduction['reduction'] > 0:
            base_score *= (1 - routine_reduction['reduction'])
            urgency_analysis['routine_filters_applied'] = routine_reduction['applied_filters']
        
        # Apply high-value indicators (increase urgency)
        high_value_boost = self.apply_high_value_indicators(text_content, financial_impact)
        if high_value_boost['boost'] > 0:
            base_score += high_value_boost['boost']
            urgency_analysis['high_value_boosts'] = high_value_boost['applied_boosts']
        
        # Normalize score
        urgency_analysis['score'] = min(1.0, max(0.0, base_score))
        
        # Add contributing factors
        if financial_impact > 0:
            urgency_analysis['contributing_factors'].append(f"Financial impact: ₹{financial_impact:,.2f}")
        
        if len(keyword_analysis['flags']) > 0:
            urgency_analysis['contributing_factors'].append(f"Keyword matches: {len(keyword_analysis['flags'])} flags")
        
        if routine_reduction['reduction'] > 0:
            urgency_analysis['contributing_factors'].append(f"Routine reduction: {routine_reduction['reduction']:.1%}")
        
        if high_value_boost['boost'] > 0:
            urgency_analysis['contributing_factors'].append(f"High-value boost: {high_value_boost['boost']:.2f}")
        
        return urgency_analysis

    def calculate_financial_impact(self, xbrl_data: Dict, keyword_analysis: Dict) -> float:
        """Calculate the financial impact of the announcement."""
        total_impact = 0.0
        
        # Sum up all financial amounts
        amounts = xbrl_data.get('amounts', [])
        for amount_info in amounts:
            total_impact += amount_info['value']
        
        # Add structured financial data
        financial_data = xbrl_data.get('financial_data', {})
        for key, value in financial_data.items():
            if isinstance(value, (int, float)) and value > 0:
                total_impact += value
        
        return total_impact

    def calculate_confidence_score(self, title: str, xbrl_data: Dict, company_info: Dict) -> Dict:
        """Calculate confidence score using enhanced algorithm."""
        confidence_analysis = {
            'score': 0.0,
            'factors': {},
            'overall_confidence': 'low'
        }
        
        weights = config.CONFIDENCE_WEIGHTS
        
        # Keyword match confidence
        keyword_match = self.calculate_keyword_match_confidence(title, xbrl_data)
        confidence_analysis['factors']['keyword_match'] = keyword_match
        
        # Company size confidence
        company_size = self.calculate_company_size_confidence(company_info)
        confidence_analysis['factors']['company_size'] = company_size
        
        # Announcement type confidence
        announcement_type = self.calculate_announcement_type_confidence(title)
        confidence_analysis['factors']['announcement_type'] = announcement_type
        
        # Time sensitivity confidence
        time_sensitivity = self.calculate_time_sensitivity_confidence()
        confidence_analysis['factors']['time_sensitivity'] = time_sensitivity
        
        # Financial data quality confidence
        financial_quality = self.calculate_financial_quality_confidence(xbrl_data)
        confidence_analysis['factors']['financial_data_quality'] = financial_quality
        
        # Source reliability confidence
        source_reliability = self.calculate_source_reliability_confidence()
        confidence_analysis['factors']['source_reliability'] = source_reliability
        
        # Data completeness confidence
        data_completeness = self.calculate_data_completeness_confidence(xbrl_data)
        confidence_analysis['factors']['data_completeness'] = data_completeness
        
        # Calculate weighted score
        total_score = 0.0
        for factor, score in confidence_analysis['factors'].items():
            total_score += score * weights.get(factor, 0.1)
        
        confidence_analysis['score'] = min(1.0, total_score)
        
        # Determine overall confidence level
        if confidence_analysis['score'] >= config.ANALYSIS_THRESHOLDS['high_confidence']:
            confidence_analysis['overall_confidence'] = 'high'
        elif confidence_analysis['score'] >= config.ANALYSIS_THRESHOLDS['medium_confidence']:
            confidence_analysis['overall_confidence'] = 'medium'
        else:
            confidence_analysis['overall_confidence'] = 'low'
        
        return confidence_analysis

    def calculate_keyword_match_confidence(self, title: str, xbrl_data: Dict) -> float:
        """Calculate confidence based on keyword matches."""
        text_content = f"{title} {xbrl_data.get('announcement_text', '')}"
        keyword_analysis = self.analyze_keywords(text_content)
        
        total_matches = sum(len(matches) for matches in keyword_analysis['keyword_matches'].values())
        return min(1.0, total_matches * 0.1)

    def calculate_company_size_confidence(self, company_info: Dict) -> float:
        """Calculate confidence based on company size."""
        # This would typically use market cap data
        # For now, return a default value
        return 0.7

    def calculate_announcement_type_confidence(self, title: str) -> str:
        """Calculate confidence based on announcement type."""
        announcement_type = self.classify_announcement_type(title, "")
        return config.ANNOUNCEMENT_TYPE_SCORES.get(announcement_type, 0.3)

    def calculate_time_sensitivity_confidence(self) -> float:
        """Calculate confidence based on time sensitivity."""
        # For now, assume normal sensitivity
        return config.TIME_SENSITIVITY_SCORES['normal']

    def calculate_financial_quality_confidence(self, xbrl_data: Dict) -> float:
        """Calculate confidence based on financial data quality."""
        quality = self.assess_financial_data_quality(xbrl_data)
        return config.FINANCIAL_DATA_QUALITY_INDICATORS.get(quality, 0.1)

    def calculate_source_reliability_confidence(self) -> float:
        """Calculate confidence based on source reliability."""
        return config.SOURCE_RELIABILITY_SCORES['bse_official']

    def calculate_data_completeness_confidence(self, xbrl_data: Dict) -> float:
        """Calculate confidence based on data completeness."""
        if not xbrl_data:
            return config.DATA_COMPLETENESS_SCORES['incomplete']
        
        required_fields = ['announcement_text', 'financial_data', 'company_info']
        present_fields = sum(1 for field in required_fields if xbrl_data.get(field))
        
        if present_fields == len(required_fields):
            return config.DATA_COMPLETENESS_SCORES['complete']
        elif present_fields >= 2:
            return config.DATA_COMPLETENESS_SCORES['partial']
        elif present_fields >= 1:
            return config.DATA_COMPLETENESS_SCORES['minimal']
        else:
            return config.DATA_COMPLETENESS_SCORES['incomplete']

    def analyze_sentiment(self, text_content: str) -> Dict:
        """Analyze sentiment using TextBlob and keyword analysis."""
        sentiment_config = config.SENTIMENT_CONFIG
        
        # TextBlob sentiment analysis
        blob = TextBlob(text_content)
        textblob_sentiment = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'overall': 'positive' if blob.sentiment.polarity > 0.1 else 'negative' if blob.sentiment.polarity < -0.1 else 'neutral'
        }
        
        # Keyword-based sentiment analysis
        text_lower = text_content.lower()
        positive_count = sum(1 for keyword in sentiment_config['positive_keywords'] if keyword in text_lower)
        negative_count = sum(1 for keyword in sentiment_config['negative_keywords'] if keyword in text_lower)
        neutral_count = sum(1 for keyword in sentiment_config['neutral_keywords'] if keyword in text_lower)
        
        keyword_sentiment = {
            'positive_keywords': positive_count,
            'negative_keywords': negative_count,
            'neutral_keywords': neutral_count,
            'overall': 'positive' if positive_count > negative_count else 'negative' if negative_count > positive_count else 'neutral'
        }
        
        return {
            'textblob': textblob_sentiment,
            'keyword_based': keyword_sentiment,
            'combined': self.combine_sentiment_analysis(textblob_sentiment, keyword_sentiment)
        }

    def combine_sentiment_analysis(self, textblob: Dict, keyword: Dict) -> Dict:
        """Combine different sentiment analysis methods."""
        # Weight TextBlob more heavily for overall sentiment
        textblob_weight = 0.7
        keyword_weight = 0.3
        
        # Convert sentiment to numeric scores
        sentiment_scores = {'positive': 1, 'neutral': 0, 'negative': -1}
        
        textblob_score = sentiment_scores[textblob['overall']] * textblob_weight
        keyword_score = sentiment_scores[keyword['overall']] * keyword_weight
        
        combined_score = textblob_score + keyword_score
        
        if combined_score > 0.3:
            overall_sentiment = 'positive'
        elif combined_score < -0.3:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'score': combined_score,
            'overall': overall_sentiment,
            'confidence': abs(combined_score)
        }

    def extract_business_events(self, xbrl_data: Dict, text_content: str) -> List[Dict]:
        """Extract business events from XBRL and text."""
        events = []
        
        # Extract from XBRL business events
        xbrl_events = xbrl_data.get('business_events', [])
        events.extend(xbrl_events)
        
        # Extract from text patterns
        text_events = self.extract_business_events_from_text(text_content)
        events.extend(text_events)
        
        return events

    def extract_business_events_from_text(self, text_content: str) -> List[Dict]:
        """Extract business events from text using pattern matching."""
        events = []
        
        event_patterns = {
            'order_win': [r'order.*?₹\s*([\d,]+)', r'contract.*?₹\s*([\d,]+)', r'win.*?₹\s*([\d,]+)'],
            'investment': [r'investment.*?₹\s*([\d,]+)', r'funding.*?₹\s*([\d,]+)'],
            'acquisition': [r'acquisition.*?₹\s*([\d,]+)', r'merger.*?₹\s*([\d,]+)'],
            'dividend': [r'dividend.*?₹\s*([\d,]+)', r'dps.*?₹\s*([\d,]+)'],
            'expansion': [r'expansion.*?₹\s*([\d,]+)', r'new.*?plant.*?₹\s*([\d,]+)']
        }
        
        for event_type, patterns in event_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match.replace(',', ''))
                        events.append({
                            'type': event_type,
                            'value': value,
                            'source': 'text_pattern'
                        })
                    except ValueError:
                        continue
        
        return events

    def assess_risks(self, text_content: str, xbrl_data: Dict) -> Dict:
        """Assess potential risks in the announcement."""
        risk_analysis = {
            'risk_level': 'low',
            'risk_factors': [],
            'risk_score': 0.0
        }
        
        risk_keywords = {
            'high': ['penalty', 'fine', 'litigation', 'dispute', 'investigation', 'probe', 'enquiry'],
            'medium': ['delay', 'postponed', 'cancelled', 'suspended', 'review', 'audit'],
            'low': ['caution', 'warning', 'notice', 'compliance']
        }
        
        text_lower = text_content.lower()
        total_risk_score = 0.0
        
        for risk_level, keywords in risk_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    risk_analysis['risk_factors'].append({
                        'factor': keyword,
                        'level': risk_level
                    })
                    
                    if risk_level == 'high':
                        total_risk_score += 0.3
                    elif risk_level == 'medium':
                        total_risk_score += 0.2
                    else:
                        total_risk_score += 0.1
        
        risk_analysis['risk_score'] = min(1.0, total_risk_score)
        
        if risk_analysis['risk_score'] >= 0.6:
            risk_analysis['risk_level'] = 'high'
        elif risk_analysis['risk_score'] >= 0.3:
            risk_analysis['risk_level'] = 'medium'
        else:
            risk_analysis['risk_level'] = 'low'
        
        return risk_analysis

    def analyze_market_impact(self, text_content: str, xbrl_data: Dict) -> Dict:
        """Analyze potential market impact of the announcement."""
        impact_analysis = {
            'impact_level': 'neutral',
            'impact_factors': [],
            'impact_score': 0.0
        }
        
        # Analyze based on financial magnitude
        financial_impact = self.calculate_financial_impact(xbrl_data, {})
        
        if financial_impact > 1000000000:  # 100 crore
            impact_analysis['impact_factors'].append('High financial magnitude')
            impact_analysis['impact_score'] += 0.4
        elif financial_impact > 100000000:  # 10 crore
            impact_analysis['impact_factors'].append('Medium financial magnitude')
            impact_analysis['impact_score'] += 0.2
        
        # Analyze based on announcement type
        announcement_type = self.classify_announcement_type("", text_content)
        if announcement_type in ['quarterly_results', 'annual_results', 'order_win']:
            impact_analysis['impact_factors'].append('High impact announcement type')
            impact_analysis['impact_score'] += 0.3
        
        # Analyze based on sentiment
        sentiment = self.analyze_sentiment(text_content)
        if sentiment['combined']['overall'] == 'positive':
            impact_analysis['impact_factors'].append('Positive sentiment')
            impact_analysis['impact_score'] += 0.2
        elif sentiment['combined']['overall'] == 'negative':
            impact_analysis['impact_factors'].append('Negative sentiment')
            impact_analysis['impact_score'] -= 0.2
        
        # Determine overall impact level
        if impact_analysis['impact_score'] >= 0.5:
            impact_analysis['impact_level'] = 'high'
        elif impact_analysis['impact_score'] >= 0.2:
            impact_analysis['impact_level'] = 'medium'
        elif impact_analysis['impact_score'] <= -0.2:
            impact_analysis['impact_level'] = 'negative'
        else:
            impact_analysis['impact_level'] = 'neutral'
        
        return impact_analysis

    def extract_metadata(self, title: str, content: str, xbrl_data: Dict) -> Dict:
        """Extract metadata from the announcement."""
        metadata = {
            'processing_timestamp': datetime.now().isoformat(),
            'content_length': len(content),
            'word_count': len(content.split()),
            'has_xbrl': bool(xbrl_data),
            'xbrl_metadata': xbrl_data.get('metadata', {}),
            'context_info': xbrl_data.get('context_info', {})
        }
        
        return metadata

    def calculate_overall_scores(self, analysis_result: Dict) -> Dict:
        """Calculate overall scores for the announcement."""
        urgency_score = analysis_result['urgency_analysis']['score']
        confidence_score = analysis_result['confidence_analysis']['score']
        
        # Calculate composite score
        composite_score = (urgency_score * 0.6) + (confidence_score * 0.4)
        
        # Determine priority level
        if composite_score >= 0.8:
            priority = 'high'
        elif composite_score >= 0.6:
            priority = 'medium'
        else:
            priority = 'low'
        
        return {
            'composite_score': composite_score,
            'priority_level': priority,
            'urgency_score': urgency_score,
            'confidence_score': confidence_score
        }

    def get_default_analysis(self) -> Dict:
        """Return default analysis when processing fails."""
        return {
            'basic_info': {'title': '', 'content_length': 0, 'has_xbrl_data': False},
            'financial_analysis': {'structured_data': {}, 'data_quality': 'no_financial_data'},
            'keyword_analysis': {'flags': [], 'keyword_matches': {}},
            'urgency_analysis': {'score': 0.0, 'flags': []},
            'confidence_analysis': {'score': 0.0, 'overall_confidence': 'low'},
            'sentiment_analysis': {'combined': {'overall': 'neutral', 'score': 0.0}},
            'business_events': [],
            'risk_assessment': {'risk_level': 'low', 'risk_score': 0.0},
            'impact_analysis': {'impact_level': 'neutral', 'impact_score': 0.0},
            'metadata': {'processing_timestamp': datetime.now().isoformat()},
            'overall_scores': {'composite_score': 0.0, 'priority_level': 'low'}
        } 

    def apply_routine_filters(self, text_content: str) -> Dict:
        """Apply filters to reduce urgency for routine announcements."""
        text_lower = text_content.lower()
        total_reduction = 0.0
        applied_filters = []
        
        for filter_type, filter_config in config.ROUTINE_ANNOUNCEMENTS.items():
            # Check if any keywords match
            keyword_matches = []
            for keyword in filter_config['keywords']:
                if keyword.lower() in text_lower:
                    keyword_matches.append(keyword)
            
            if keyword_matches:
                # Check for exceptions that would override the filter
                has_exception = False
                for exception in filter_config['exceptions']:
                    if exception.lower() in text_lower:
                        has_exception = True
                        break
                
                if not has_exception:
                    # Apply the reduction
                    reduction = filter_config['urgency_reduction']
                    total_reduction += reduction
                    applied_filters.append({
                        'type': filter_type,
                        'keywords_matched': keyword_matches,
                        'reduction': reduction
                    })
        
        # Cap total reduction at 90% to avoid completely eliminating urgency
        total_reduction = min(0.9, total_reduction)
        
        return {
            'reduction': total_reduction,
            'applied_filters': applied_filters
        }

    def apply_high_value_indicators(self, text_content: str, financial_impact: float) -> Dict:
        """Apply high-value indicators to boost urgency scores."""
        text_lower = text_content.lower()
        total_boost = 0.0
        applied_boosts = []
        
        for indicator_type, indicator_config in config.HIGH_VALUE_INDICATORS.items():
            # Check if any keywords match
            keyword_matches = []
            for keyword in indicator_config['keywords']:
                if keyword.lower() in text_lower:
                    keyword_matches.append(keyword)
            
            if keyword_matches:
                # Check if threshold is met (for financial magnitude)
                if indicator_config['threshold'] > 0:
                    if financial_impact >= indicator_config['threshold']:
                        boost = indicator_config['urgency_boost']
                        total_boost += boost
                        applied_boosts.append({
                            'type': indicator_type,
                            'keywords_matched': keyword_matches,
                            'boost': boost,
                            'threshold_met': True
                        })
                else:
                    # No threshold required
                    boost = indicator_config['urgency_boost']
                    total_boost += boost
                    applied_boosts.append({
                        'type': indicator_type,
                        'keywords_matched': keyword_matches,
                        'boost': boost,
                        'threshold_met': True
                    })
        
        return {
            'boost': total_boost,
            'applied_boosts': applied_boosts
        }

    def should_send_email_alert(self, analysis_result: Dict) -> Dict:
        """Determine if an email alert should be sent - now always sends but with categorization."""
        thresholds = config.EMAIL_ALERT_THRESHOLDS
        
        urgency_score = analysis_result['urgency_analysis']['score']
        confidence_score = analysis_result['confidence_analysis']['score']
        composite_score = analysis_result['overall_scores']['composite_score']
        financial_impact = analysis_result['urgency_analysis']['financial_impact']
        
        # Check basic thresholds (now always true since thresholds are 0)
        meets_urgency = urgency_score >= thresholds['urgency_score']
        meets_confidence = confidence_score >= thresholds['confidence_score']
        meets_composite = composite_score >= thresholds['composite_score']
        meets_financial = financial_impact >= thresholds['financial_impact']
        
        # Check announcement types for categorization
        is_routine = self.is_routine_announcement(analysis_result)
        is_technical = self.is_technical_announcement(analysis_result)
        is_administrative = self.is_administrative_announcement(analysis_result)
        
        # Always send emails, but categorize them
        should_send = True
        
        # Determine announcement category
        if is_technical:
            category = "technical"
        elif is_administrative:
            category = "administrative"
        elif is_routine:
            category = "routine"
        else:
            category = "important"
        
        return {
            'should_send': should_send,
            'category': category,
            'reasons': {
                'urgency_threshold_met': meets_urgency,
                'confidence_threshold_met': meets_confidence,
                'composite_threshold_met': meets_composite,
                'financial_threshold_met': meets_financial,
                'is_routine': is_routine,
                'is_technical': is_technical,
                'is_administrative': is_administrative
            },
            'scores': {
                'urgency': urgency_score,
                'confidence': confidence_score,
                'composite': composite_score,
                'financial_impact': financial_impact
            },
            'thresholds': thresholds,
            'categorization': {
                'type': category,
                'priority': self.get_priority_level(urgency_score, category),
                'should_highlight': category == 'important' and urgency_score > 0.6
            }
        }

    def get_priority_level(self, urgency_score: float, category: str) -> str:
        """Get priority level based on urgency score and category."""
        if category == 'important' and urgency_score > 0.8:
            return 'critical'
        elif category == 'important' and urgency_score > 0.6:
            return 'high'
        elif category == 'important' and urgency_score > 0.4:
            return 'medium'
        elif category == 'routine' and urgency_score > 0.3:
            return 'routine_important'
        elif category in ['technical', 'administrative']:
            return 'low'
        else:
            return 'routine'

    def is_routine_announcement(self, analysis_result: Dict) -> bool:
        """Check if this is a routine announcement."""
        text_content = f"{analysis_result['basic_info']['title']} {analysis_result['basic_info'].get('extracted_text', '')}"
        text_lower = text_content.lower()
        
        # Check for routine keywords
        routine_keywords = [
            'board meeting', 'compliance', 'filing', 'submission', 'disclosure',
            'intimation', 'notice', 'update', 'information', 'clarification',
            'correction', 'amendment', 'revision', 'modification'
        ]
        
        return any(keyword in text_lower for keyword in routine_keywords)

    def is_technical_announcement(self, analysis_result: Dict) -> bool:
        """Check if this is a technical announcement."""
        text_content = f"{analysis_result['basic_info']['title']} {analysis_result['basic_info'].get('extracted_text', '')}"
        text_lower = text_content.lower()
        
        technical_keywords = [
            'technical', 'system', 'website', 'portal', 'online', 'digital',
            'IT', 'maintenance', 'upgrade', 'patch', 'fix', 'glitch'
        ]
        
        return any(keyword in text_lower for keyword in technical_keywords)

    def is_administrative_announcement(self, analysis_result: Dict) -> bool:
        """Check if this is an administrative announcement."""
        text_content = f"{analysis_result['basic_info']['title']} {analysis_result['basic_info'].get('extracted_text', '')}"
        text_lower = text_content.lower()
        
        administrative_keywords = [
            'administrative', 'procedural', 'process', 'procedure', 'formality',
            'routine', 'regular', 'periodic', 'scheduled', 'planned'
        ]
        
        return any(keyword in text_lower for keyword in administrative_keywords)

    def classify_announcement_priority(self, analysis_result: Dict) -> str:
        """Classify announcement priority based on type and content."""
        announcement_type = analysis_result['basic_info']['announcement_type']
        
        # Check if it's in high priority types
        if announcement_type in config.ANNOUNCEMENT_TYPES['high_priority']:
            return 'high'
        
        # Check if it's in low priority types
        if announcement_type in config.ANNOUNCEMENT_TYPES['low_priority']:
            return 'low'
        
        # Check financial impact for medium priority
        financial_impact = analysis_result['urgency_analysis']['financial_impact']
        if financial_impact > 10000000:  # 1 crore
            return 'high'
        elif financial_impact > 1000000:  # 10 lakh
            return 'medium'
        else:
            return 'low' 