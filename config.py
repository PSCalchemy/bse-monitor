import os
from dotenv import load_dotenv

# Only load .env file if it exists (for local development)
# In production (Render), environment variables are set directly
if os.path.exists('.env'):
    load_dotenv()

# BSE Configuration
BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"
BSE_BASE_URL = "https://www.bseindia.com"
CHECK_INTERVAL_MINUTES = 15  # How often to check for new announcements (increased to reduce resource usage)

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

# Recipient emails (comma-separated in .env file)
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS', '').split(',')

# Enhanced Keywords for flagging announcements with weights
URGENCY_KEYWORDS = {
    "📈 Earnings Spike": {
        "keywords": [
            "profit", "earnings", "revenue", "growth", "increase", "surge", "jump",
            "quarterly results", "annual results", "financial results", "PAT", "EBITDA",
            "net profit", "operating profit", "gross profit", "profit after tax",
            "earnings per share", "EPS", "EBIT", "operating income"
        ],
        "weight": 0.8,
        "financial_threshold": 10000000  # 1 crore minimum for high urgency
    },
    "🛠️ Order Win": {
        "keywords": [
            "order", "contract", "win", "award", "project", "deal", "agreement",
            "MoD", "defense", "government", "tender", "bid", "work order",
            "purchase order", "service contract", "maintenance contract",
            "construction contract", "supply order", "procurement"
        ],
        "weight": 0.9,
        "financial_threshold": 50000000  # 5 crore minimum for high urgency
    },
    "💰 Financial": {
        "keywords": [
            "dividend", "bonus", "rights issue", "buyback", "merger", "acquisition",
            "investment", "funding", "capital", "debt", "loan", "FPO", "IPO",
            "QIP", "preferential allotment", "warrants", "convertible bonds",
            "capital restructuring", "share split", "stock dividend"
        ],
        "weight": 0.7,
        "financial_threshold": 25000000  # 2.5 crore minimum for high urgency
    },
    "⚡ Breaking": {
        "keywords": [
            "urgent", "immediate", "breaking", "important", "critical", "emergency",
            "resignation", "appointment", "change", "restructuring", "CEO", "MD",
            "board change", "management change", "strategic", "partnership",
            "joint venture", "subsidiary", "disinvestment", "delisting"
        ],
        "weight": 0.6,
        "financial_threshold": 0  # No financial threshold for breaking news
    },
    "🏭 Business Expansion": {
        "keywords": [
            "expansion", "new plant", "new facility", "capacity increase",
            "production increase", "market expansion", "geographic expansion",
            "new product", "new service", "R&D", "research", "development",
            "innovation", "technology", "digital transformation", "automation"
        ],
        "weight": 0.5,
        "financial_threshold": 50000000  # 5 crore minimum for high urgency
    },
    "📊 Regulatory": {
        "keywords": [
            "SEBI", "RBI", "regulatory", "compliance", "audit", "inspection",
            "penalty", "fine", "settlement", "legal", "litigation", "court",
            "arbitration", "dispute", "investigation", "enquiry", "probe"
        ],
        "weight": 0.4,
        "financial_threshold": 0  # No financial threshold for regulatory news
    }
}

# Routine/Compliance announcement filters - these reduce urgency scores
ROUTINE_ANNOUNCEMENTS = {
    "board_meeting": {
        "keywords": [
            "board meeting", "board of directors meeting", "board meeting intimation",
            "board meeting notice", "board meeting schedule", "board meeting date",
            "board meeting agenda", "board meeting outcome", "board meeting results"
        ],
        "urgency_reduction": 0.5,  # Reduce urgency by 50%
        "exceptions": [
            "board meeting outcome", "board meeting results", "board meeting decision",
            "strategic", "merger", "acquisition", "dividend", "bonus", "rights"
        ]
    },
    "compliance": {
        "keywords": [
            "compliance", "regulatory compliance", "statutory compliance",
            "filing", "submission", "disclosure", "intimation", "notice",
            "regulatory filing", "statutory filing", "periodic filing",
            "quarterly filing", "annual filing", "monthly filing"
        ],
        "urgency_reduction": 0.6,  # Reduce urgency by 60%
        "exceptions": [
            "penalty", "fine", "violation", "breach", "investigation", "enquiry",
            "settlement", "legal action", "litigation"
        ]
    },
    "routine_updates": {
        "keywords": [
            "update", "information", "clarification", "correction", "amendment",
            "revision", "modification", "change in", "update on", "status update",
            "progress update", "development update", "quarterly update"
        ],
        "urgency_reduction": 0.4,  # Reduce urgency by 40%
        "exceptions": [
            "significant", "major", "important", "material", "substantial",
            "strategic", "financial", "operational"
        ]
    },
    "administrative": {
        "keywords": [
            "administrative", "procedural", "process", "procedure", "formality",
            "routine", "regular", "periodic", "scheduled", "planned",
            "appointment", "resignation", "change in", "designation"
        ],
        "urgency_reduction": 0.7,  # Reduce urgency by 70%
        "exceptions": [
            "CEO", "MD", "director", "key management", "senior management",
            "strategic", "important", "significant"
        ]
    },
    "technical": {
        "keywords": [
            "technical", "technical glitch", "technical issue", "system",
            "website", "portal", "online", "digital", "IT", "information technology",
            "maintenance", "upgrade", "update", "patch", "fix"
        ],
        "urgency_reduction": 0.8,  # Reduce urgency by 80%
        "exceptions": [
            "security", "breach", "hack", "cyber", "data", "privacy"
        ]
    }
}

# High-value announcement indicators - these increase urgency scores
HIGH_VALUE_INDICATORS = {
    "financial_magnitude": {
        "keywords": [
            "crore", "cr", "lakh", "million", "billion", "thousand crore",
            "hundred crore", "fifty crore", "twenty crore", "ten crore"
        ],
        "urgency_boost": 0.3,  # Increase urgency by 30%
        "threshold": 10000000  # 1 crore minimum
    },
    "strategic_importance": {
        "keywords": [
            "strategic", "strategic decision", "strategic initiative", "strategic plan",
            "strategic partnership", "strategic alliance", "strategic investment",
            "game changer", "transformational", "milestone", "landmark"
        ],
        "urgency_boost": 0.4,  # Increase urgency by 40%
        "threshold": 0
    },
    "market_impact": {
        "keywords": [
            "market", "stock", "share", "trading", "exchange", "listing",
            "delisting", "suspension", "trading halt", "circuit breaker"
        ],
        "urgency_boost": 0.2,  # Increase urgency by 20%
        "threshold": 0
    },
    "government_related": {
        "keywords": [
            "government", "ministry", "department", "authority", "regulatory",
            "policy", "regulation", "law", "act", "bill", "order"
        ],
        "urgency_boost": 0.3,  # Increase urgency by 30%
        "threshold": 0
    }
}

# Announcement type classification for better filtering
ANNOUNCEMENT_TYPES = {
    "high_priority": [
        "quarterly_results", "annual_results", "order_win", "merger_acquisition",
        "dividend", "bonus", "rights_issue", "buyback", "investment",
        "expansion", "strategic_partnership", "management_change"
    ],
    "medium_priority": [
        "regulatory", "compliance_important", "financial_update", "operational_update"
    ],
    "low_priority": [
        "board_meeting", "compliance_routine", "administrative", "technical",
        "routine_update", "clarification", "correction"
    ]
}

# Minimum thresholds for email alerts - Modified to send all emails
EMAIL_ALERT_THRESHOLDS = {
    "urgency_score": 0.0,      # Send emails for all urgency levels
    "confidence_score": 0.0,    # Send emails for all confidence levels
    "composite_score": 0.0,     # Send emails for all composite scores
    "financial_impact": 0,      # Send emails regardless of financial impact
    "exclude_routine": False,   # Don't exclude routine announcements
    "exclude_technical": False, # Don't exclude technical announcements
    "exclude_administrative": False  # Don't exclude administrative announcements
}

# Enhanced Confidence scoring weights with more sophisticated algorithm
CONFIDENCE_WEIGHTS = {
    "keyword_match": 0.25,
    "company_size": 0.15,
    "announcement_type": 0.20,
    "time_sensitivity": 0.10,
    "financial_data_quality": 0.15,
    "source_reliability": 0.10,
    "data_completeness": 0.05
}

# Company size categories for scoring
COMPANY_SIZE_CATEGORIES = {
    "large_cap": {
        "market_cap_range": (20000, float('inf')),  # 20,000+ crore
        "weight": 1.0
    },
    "mid_cap": {
        "market_cap_range": (5000, 20000),  # 5,000-20,000 crore
        "weight": 0.8
    },
    "small_cap": {
        "market_cap_range": (500, 5000),  # 500-5,000 crore
        "weight": 0.6
    },
    "micro_cap": {
        "market_cap_range": (0, 500),  # 0-500 crore
        "weight": 0.4
    }
}

# Announcement type scoring
ANNOUNCEMENT_TYPE_SCORES = {
    "quarterly_results": 0.9,
    "annual_results": 0.9,
    "order_win": 0.8,
    "dividend": 0.7,
    "bonus": 0.7,
    "rights_issue": 0.6,
    "buyback": 0.6,
    "merger_acquisition": 0.8,
    "investment": 0.6,
    "regulatory": 0.5,
    "management_change": 0.4,
    "board_meeting": 0.2,  # Low score for routine board meetings
    "compliance": 0.3,     # Low score for routine compliance
    "administrative": 0.1, # Very low score for administrative
    "technical": 0.1,      # Very low score for technical
    "general": 0.3
}

# Time sensitivity scoring
TIME_SENSITIVITY_SCORES = {
    "immediate": 1.0,      # Within 1 hour
    "urgent": 0.8,         # Within 4 hours
    "high": 0.6,           # Within 24 hours
    "normal": 0.4,         # Within 1 week
    "low": 0.2             # Beyond 1 week
}

# Financial data quality indicators
FINANCIAL_DATA_QUALITY_INDICATORS = {
    "structured_xbrl": 1.0,
    "unstructured_text": 0.6,
    "partial_data": 0.4,
    "no_financial_data": 0.1
}

# Source reliability scoring
SOURCE_RELIABILITY_SCORES = {
    "bse_official": 1.0,
    "company_website": 0.9,
    "regulatory_body": 0.8,
    "news_agency": 0.6,
    "social_media": 0.3
}

# Data completeness scoring
DATA_COMPLETENESS_SCORES = {
    "complete": 1.0,       # All required fields present
    "partial": 0.7,        # Most fields present
    "minimal": 0.4,        # Basic fields only
    "incomplete": 0.1      # Missing critical data
}

# Enhanced analysis thresholds
ANALYSIS_THRESHOLDS = {
    "high_urgency": 0.8,
    "medium_urgency": 0.6,
    "low_urgency": 0.4,
    "high_confidence": 0.8,
    "medium_confidence": 0.6,
    "low_confidence": 0.4
}

# Financial pattern recognition
FINANCIAL_PATTERNS = {
    "currency_patterns": [
        r'₹\s*([\d,]+\.?\d*)',
        r'Rs\.\s*([\d,]+\.?\d*)',
        r'INR\s*([\d,]+\.?\d*)',
        r'USD\s*([\d,]+\.?\d*)',
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(crore|cr)',
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(lakh|lk)',
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(million|mn)'
    ],
    "percentage_patterns": [
        r'(\d+\.?\d*)\s*%',
        r'(\d+\.?\d*)\s*percent',
        r'increase\s*of\s*(\d+\.?\d*)',
        r'growth\s*of\s*(\d+\.?\d*)',
        r'decrease\s*of\s*(\d+\.?\d*)',
        r'decline\s*of\s*(\d+\.?\d*)'
    ],
    "date_patterns": [
        r'\d{4}-\d{2}-\d{2}',
        r'\d{2}-\d{2}-\d{4}',
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2}/\d{2}/\d{2}'
    ]
}

# Sentiment analysis configuration
SENTIMENT_CONFIG = {
    "positive_keywords": [
        "profit", "growth", "increase", "surge", "jump", "win", "award",
        "success", "positive", "strong", "robust", "excellent", "outstanding"
    ],
    "negative_keywords": [
        "loss", "decline", "decrease", "fall", "drop", "penalty", "fine",
        "negative", "weak", "poor", "disappointing", "concern", "risk"
    ],
    "neutral_keywords": [
        "announce", "declare", "inform", "notify", "update", "report",
        "submit", "file", "comply", "regulatory", "routine"
    ]
}

# Email template configuration
EMAIL_CONFIG = {
    "max_subject_length": 100,
    "max_body_length": 5000,
    "include_attachments": False,
    "html_template": True,
    "plain_text_fallback": True,
    "urgency_colors": {
        "high": "#FF4444",      # Red
        "medium": "#FF8800",    # Orange
        "low": "#44AA44"        # Green
    }
}

# Database file for tracking processed announcements
DB_FILE = "processed_announcements.json"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FILE = "bse_monitor.log"

# Performance monitoring
PERFORMANCE_CONFIG = {
    "enable_metrics": True,
    "log_processing_time": True,
    "cache_duration_minutes": 30,
    "max_retries": 3,
    "retry_delay_seconds": 5
} 