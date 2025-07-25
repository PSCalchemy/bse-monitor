import os
from dotenv import load_dotenv

# Only load .env file if it exists (for local development)
# In production (Render), environment variables are set directly
if os.path.exists('.env'):
    load_dotenv()

# BSE Configuration
BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"
BSE_BASE_URL = "https://www.bseindia.com"
CHECK_INTERVAL_MINUTES = 5  # How often to check for new announcements

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

# Recipient emails (comma-separated in .env file)
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS', '').split(',')

# Keywords for flagging announcements
URGENCY_KEYWORDS = {
    "📈 Earnings Spike": [
        "profit", "earnings", "revenue", "growth", "increase", "surge", "jump",
        "quarterly results", "annual results", "financial results", "PAT", "EBITDA"
    ],
    "🛠️ Order Win": [
        "order", "contract", "win", "award", "project", "deal", "agreement",
        "MoD", "defense", "government", "tender", "bid"
    ],
    "💰 Financial": [
        "dividend", "bonus", "rights issue", "buyback", "merger", "acquisition",
        "investment", "funding", "capital", "debt", "loan"
    ],
    "⚡ Breaking": [
        "urgent", "immediate", "breaking", "important", "critical", "emergency",
        "resignation", "appointment", "change", "restructuring"
    ]
}

# Confidence scoring weights
CONFIDENCE_WEIGHTS = {
    "keyword_match": 0.4,
    "company_size": 0.2,
    "announcement_type": 0.3,
    "time_sensitivity": 0.1
}

# Database file for tracking processed announcements
DB_FILE = "processed_announcements.json"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FILE = "bse_monitor.log" 