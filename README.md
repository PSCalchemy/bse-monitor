# 🚨 BSE Monitor - Intelligent Corporate Announcement Alert System

A sophisticated real-time monitoring system for BSE (Bombay Stock Exchange) corporate announcements with intelligent XBRL parsing, advanced analysis, and smart email categorization.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [System Components](#system-components)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Email Alert System](#email-alert-system)
- [XBRL Analysis](#xbrl-analysis)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

BSE Monitor is an enterprise-grade system that:

- **Monitors BSE announcements 24/7** with configurable intervals
- **Parses XBRL data** using Indian market taxonomy
- **Analyzes announcements** with multi-factor scoring
- **Categorizes content** (Important/Routine/Technical/Administrative)
- **Sends intelligent email alerts** with visual prioritization
- **Provides web interface** for monitoring and control

### Key Capabilities

- **Schema-aware XBRL parsing** with fallback mechanisms
- **Sophisticated content analysis** with urgency and confidence scoring
- **Smart categorization** of announcements by type and priority
- **Financial impact assessment** with unit conversion
- **Risk and sentiment analysis** using multiple algorithms
- **Real-time monitoring** with web dashboard
- **Comprehensive logging** and error handling

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   BSE Website   │    │   Web Interface │    │   Email Client  │
│   (Data Source) │    │   (Dashboard)   │    │   (Alerts)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BSE Monitor System                          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  BSE Monitor    │  Announcement   │  Email Sender              │
│  (Web Scraper)  │  Analyzer       │  (Alert Generator)         │
├─────────────────┼─────────────────┼─────────────────────────────┤
│  XBRL Parser    │  Content        │  HTML/Text                 │
│  (Data Extractor)│  Analysis       │  Templates                 │
├─────────────────┼─────────────────┼─────────────────────────────┤
│  Configuration  │  Risk Assessment│  SMTP Client               │
│  Management     │  & Sentiment    │  (Email Delivery)          │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

### Data Flow

1. **BSE Monitor** scrapes announcements from BSE website
2. **XBRL Parser** extracts structured data from XBRL files
3. **Announcement Analyzer** performs comprehensive analysis
4. **Email Sender** generates and sends categorized alerts
5. **Web Interface** provides monitoring and control dashboard

## ✨ Features

### 🔍 Intelligent Monitoring
- **Real-time scraping** of BSE announcements
- **Duplicate detection** to avoid processing same announcement
- **Configurable intervals** (default: 5 minutes)
- **Error handling** with retry mechanisms

### 📊 Advanced XBRL Parsing
- **Indian XBRL taxonomy** support (ind-as, ind namespaces)
- **Schema-aware parsing** with fallback to pattern matching
- **Financial data extraction** with unit conversion
- **Business event detection** from structured data
- **Context preservation** and metadata extraction

### 🧠 Sophisticated Analysis
- **Multi-factor urgency scoring** with weighted algorithms
- **Confidence assessment** based on 7 different factors
- **Sentiment analysis** using TextBlob and keyword matching
- **Risk assessment** with severity classification
- **Market impact prediction** based on financial magnitude

### 📧 Smart Email Categorization
- **All announcements** get email alerts
- **Visual categorization** with color-coded badges
- **Priority levels** (Critical/High/Medium/Routine/Low)
- **Subject line indicators** for easy filtering
- **Rich HTML templates** with comprehensive information

### 🌐 Web Interface
- **Real-time dashboard** showing system status
- **Announcement history** with search and filtering
- **Configuration management** through web interface
- **Performance metrics** and monitoring data

## 🔧 System Components

### Core Modules

#### 1. **BSE Monitor** (`bse_monitor_web.py`)
```python
# Main monitoring system with web interface
- Scrapes BSE announcements
- Manages processing queue
- Provides web dashboard
- Handles system configuration
```

#### 2. **XBRL Parser** (`xbrl_parser.py`)
```python
# Enhanced XBRL parsing with Indian taxonomy
- Schema-aware data extraction
- Financial metrics parsing
- Business event detection
- Unit conversion and validation
```

#### 3. **Announcement Analyzer** (`announcement_analyzer.py`)
```python
# Comprehensive content analysis
- Multi-factor scoring algorithms
- Categorization logic
- Risk and sentiment analysis
- Email decision making
```

#### 4. **Email Sender** (`email_sender.py`)
```python
# Intelligent email generation
- Categorized email templates
- Visual indicators and badges
- HTML and plain text support
- SMTP configuration management
```

#### 5. **Configuration** (`config.py`)
```python
# Centralized configuration
- Email settings
- Analysis parameters
- Thresholds and weights
- Categorization rules
```

### Supporting Files

- **`requirements.txt`** - Python dependencies
- **`Dockerfile`** - Container configuration
- **`render.yaml`** - Deployment configuration
- **`Procfile`** - Process management
- **`test_endpoints.py`** - API testing

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- Gmail account with App Password
- Internet connection for BSE access

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd bse-monitor
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file**
```bash
cp .env.example .env
# Edit .env with your email credentials
```

5. **Configure email settings**
```bash
# In .env file:
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=your-email@gmail.com
RECIPIENT_EMAILS=recipient1@email.com,recipient2@email.com
```

6. **Run the system**
```bash
python bse_monitor_web.py
```

### Production Deployment

#### Using Render (Recommended)

1. **Fork the repository** to your GitHub account
2. **Connect to Render** and create a new Web Service
3. **Configure environment variables** in Render dashboard
4. **Deploy automatically** from GitHub

#### Using Docker

```bash
# Build image
docker build -t bse-monitor .

# Run container
docker run -p 8000:8000 --env-file .env bse-monitor
```

## ⚙️ Configuration

### Email Configuration

```python
# config.py
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@gmail.com'
SMTP_PASSWORD = 'your-app-password'
SENDER_EMAIL = 'your-email@gmail.com'
RECIPIENT_EMAILS = ['recipient1@email.com', 'recipient2@email.com']
```

### Monitoring Settings

```python
# config.py
BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"
CHECK_INTERVAL_MINUTES = 5  # How often to check for new announcements
```

### Analysis Configuration

```python
# config.py
URGENCY_KEYWORDS = {
    "📈 Earnings Spike": {
        "keywords": ["profit", "earnings", "revenue", "growth"],
        "weight": 0.8,
        "financial_threshold": 10000000  # 1 crore
    },
    # ... more categories
}

CONFIDENCE_WEIGHTS = {
    "keyword_match": 0.25,
    "company_size": 0.15,
    "announcement_type": 0.20,
    # ... more factors
}
```

## 📖 Usage

### Starting the System

```bash
# Start with web interface
python bse_monitor_web.py

# Access dashboard at http://localhost:8000
```

### Web Dashboard

- **Status Page**: System health and monitoring status
- **Announcements**: Recent announcements with analysis
- **Configuration**: Update settings through web interface
- **Logs**: Real-time system logs

### API Endpoints

```bash
# System status
GET /api/status

# Recent announcements
GET /api/announcements

# Manual check
POST /api/check-now

# Configuration
GET /api/config
PUT /api/config
```

### Email Alerts

The system automatically sends email alerts for all announcements with:

- **Subject line categorization** (🚨 CRITICAL, ⚠️ HIGH, etc.)
- **Visual badges** indicating priority and type
- **Comprehensive analysis** including financial impact
- **Classification reasoning** showing why it was categorized

## 📧 Email Alert System

### Email Categories

| Category | Subject Prefix | Priority | Description |
|----------|----------------|----------|-------------|
| Critical | 🚨 CRITICAL | Highest | Urgent business events |
| High | ⚠️ HIGH | High | Important announcements |
| Medium | 📈 MEDIUM | Medium | Significant updates |
| Routine | 📋 ROUTINE | Low | Regular compliance |
| Technical | 🔧 TECHNICAL | Low | System updates |
| Admin | 📝 ADMIN | Low | Administrative |

### Email Content

Each email includes:

1. **Category Badge** - Visual indicator of priority
2. **Announcement Details** - Title and content summary
3. **Analysis Scores** - Urgency, confidence, sentiment
4. **Financial Data** - Extracted amounts and metrics
5. **Flags & Keywords** - Detected business events
6. **Categorization** - Why it was classified this way

### Email Client Filtering

Set up filters in your email client:

```
🚨 CRITICAL: → High Priority Folder
⚠️ HIGH: → Important Folder
📈 MEDIUM: → Medium Priority Folder
📋 ROUTINE: → Routine Folder
🔧 TECHNICAL: → Technical Folder
📝 ADMIN: → Administrative Folder
```

## 📊 XBRL Analysis

### What is XBRL?

XBRL (eXtensible Business Reporting Language) is a standardized format for financial reporting used by BSE companies.

### Parsing Capabilities

#### Schema-Aware Parsing
```python
# Indian XBRL taxonomy elements
indian_taxonomy = {
    'financial_metrics': [
        'RevenueFromOperations', 'TotalRevenue', 'ProfitBeforeTax',
        'EarningsPerShare', 'BookValuePerShare', 'NetWorth'
    ],
    'business_events': [
        'OrderReceived', 'ContractAwarded', 'DividendDeclared'
    ],
    'company_identifiers': [
        'EntityRegistrantName', 'TradingSymbol', 'ISIN', 'CIN'
    ]
}
```

#### Data Extraction
- **Financial metrics** with unit conversion
- **Business events** with context
- **Company information** and identifiers
- **Dates and periods** with validation
- **Amounts and percentages** with formatting

#### Fallback Mechanisms
- **Pattern matching** when taxonomy fails
- **Text extraction** for unstructured content
- **Validation** to ensure data quality
- **Error handling** with graceful degradation

### Analysis Pipeline

1. **XBRL Download** - Fetch XBRL file from BSE
2. **Schema Parsing** - Extract structured data
3. **Pattern Matching** - Fallback for missing data
4. **Unit Conversion** - Normalize financial amounts
5. **Validation** - Ensure data quality
6. **Analysis** - Apply business logic

## 🌐 API Endpoints

### System Status

```bash
GET /api/status
```

Response:
```json
{
  "status": "running",
  "last_check": "2025-01-25T10:30:00Z",
  "announcements_processed": 150,
  "emails_sent": 45,
  "uptime": "2 days, 5 hours"
}
```

### Recent Announcements

```bash
GET /api/announcements?limit=10&category=important
```

Response:
```json
{
  "announcements": [
    {
      "title": "Quarterly Results",
      "category": "important",
      "urgency_score": 0.85,
      "financial_impact": 500000000,
      "timestamp": "2025-01-25T10:30:00Z"
    }
  ]
}
```

### Manual Check

```bash
POST /api/check-now
```

Response:
```json
{
  "status": "success",
  "announcements_found": 3,
  "emails_sent": 2,
  "processing_time": "2.5 seconds"
}
```

### Configuration

```bash
GET /api/config
PUT /api/config
```

## 🚀 Deployment

### Render Deployment

1. **Fork repository** to GitHub
2. **Create Render account** and connect GitHub
3. **Create Web Service** with these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bse_monitor_web.py`
   - **Environment**: Python 3.8+

4. **Set Environment Variables**:
   ```
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SENDER_EMAIL=your-email@gmail.com
   RECIPIENT_EMAILS=recipient1@email.com,recipient2@email.com
   ```

5. **Deploy** - Render will automatically deploy from GitHub

### Docker Deployment

```bash
# Build image
docker build -t bse-monitor .

# Run with environment file
docker run -d \
  --name bse-monitor \
  -p 8000:8000 \
  --env-file .env \
  bse-monitor

# Or with Docker Compose
docker-compose up -d
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SMTP_USERNAME` | Gmail username | Yes |
| `SMTP_PASSWORD` | Gmail app password | Yes |
| `SENDER_EMAIL` | From email address | Yes |
| `RECIPIENT_EMAILS` | Comma-separated recipient emails | Yes |
| `CHECK_INTERVAL_MINUTES` | Monitoring interval | No (default: 5) |
| `LOG_LEVEL` | Logging level | No (default: INFO) |

## 🔧 Troubleshooting

### Common Issues

#### Email Not Sending

1. **Check Gmail App Password**
   - Enable 2-factor authentication
   - Generate app password for this application
   - Use app password, not regular password

2. **Verify SMTP Settings**
   ```python
   SMTP_SERVER = 'smtp.gmail.com'
   SMTP_PORT = 587
   ```

3. **Test Email Configuration**
   ```bash
   python -c "from email_sender import EmailSender; EmailSender().test_email_configuration()"
   ```

#### No Announcements Found

1. **Check BSE Website Access**
   - Verify internet connection
   - Check if BSE website is accessible
   - Monitor logs for scraping errors

2. **Verify URL Configuration**
   ```python
   BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"
   ```

#### High CPU/Memory Usage

1. **Adjust Check Interval**
   ```python
   CHECK_INTERVAL_MINUTES = 10  # Increase interval
   ```

2. **Monitor Logs**
   - Check for infinite loops
   - Verify error handling
   - Monitor memory usage

### Log Analysis

```bash
# View real-time logs
tail -f bse_monitor.log

# Search for errors
grep "ERROR" bse_monitor.log

# Check email sending
grep "Email sent" bse_monitor.log
```

### Performance Optimization

1. **Database Optimization**
   - Use SQLite for small deployments
   - Consider PostgreSQL for large scale
   - Implement data archiving

2. **Caching**
   - Cache processed announcements
   - Implement request caching
   - Use Redis for session storage

3. **Monitoring**
   - Set up health checks
   - Monitor response times
   - Track error rates

## 📈 Monitoring & Analytics

### System Metrics

- **Uptime** - System availability
- **Processing Time** - Announcement analysis speed
- **Email Delivery Rate** - Success rate of email sending
- **Error Rate** - System error frequency

### Business Metrics

- **Announcements Processed** - Total announcements analyzed
- **Important Alerts** - Critical and high-priority announcements
- **Financial Impact** - Total financial value of announcements
- **Category Distribution** - Breakdown by announcement type

### Dashboard Features

- **Real-time Status** - Current system state
- **Historical Data** - Trends and patterns
- **Configuration Management** - Update settings
- **Log Viewer** - Real-time log monitoring

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes** with proper testing
4. **Submit pull request**

### Code Standards

- **Python PEP 8** compliance
- **Type hints** for all functions
- **Docstrings** for all classes and methods
- **Unit tests** for new features

### Testing

```bash
# Run tests
python -m pytest tests/

# Test specific module
python -m pytest tests/test_analyzer.py

# Coverage report
python -m pytest --cov=.
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help

1. **Check Documentation** - This README and inline comments
2. **Review Logs** - System logs for error details
3. **Test Configuration** - Verify email and monitoring settings
4. **Create Issue** - Report bugs or request features

### Common Questions

**Q: How often should I check for announcements?**
A: Default is 5 minutes, but you can adjust based on your needs. More frequent checks may hit rate limits.

**Q: Can I filter out certain types of announcements?**
A: Yes, the system categorizes all announcements but you can set up email filters based on subject prefixes.

**Q: What if BSE changes their website?**
A: The system has fallback mechanisms, but you may need to update scraping logic if major changes occur.

**Q: How do I add more recipients?**
A: Update the `RECIPIENT_EMAILS` environment variable with comma-separated email addresses.

---

**Built with ❤️ for intelligent financial monitoring** 