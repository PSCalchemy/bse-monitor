# BSE Monitor

A Python-based monitoring system that tracks Bombay Stock Exchange (BSE) corporate announcements in real-time and sends email alerts with structured analysis.

## 🚀 **Live Deployment**

**Status**: ✅ **Running on Render.com**
- **Service**: 24/7 BSE announcement monitoring
- **Email Alerts**: Sent to `9ranjal@gmail.com`
- **Monitoring**: Every 5 minutes
- **Repository**: https://github.com/PSCalchemy/bse-monitor

## ✨ **Features**

- **Real-time Monitoring**: Tracks BSE corporate announcements page
- **XBRL Parsing**: Extracts structured data from XBRL files
- **Content Analysis**: Analyzes announcements for urgency and keywords
- **Email Alerts**: Multi-user email notifications with detailed analysis
- **Structured Data**: JSON-formatted alerts with:
  - Company information
  - Timestamp and announcement text
  - Urgency and confidence scores
  - Keyword extraction and flags
  - Financial data parsing

## 📁 **Project Structure**

```
bse-monitor/
├── bse_monitor_simple.py    # Main monitoring service (Render deployment)
├── config.py               # Configuration and environment variables
├── xbrl_parser.py          # XBRL file parsing and data extraction
├── announcement_analyzer.py # Content analysis and scoring
├── email_sender.py         # Email alert system
├── requirements.txt        # Python dependencies
├── render.yaml            # Render.com deployment configuration
├── Procfile               # Process file for deployment
├── Dockerfile             # Docker configuration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 **Core Components**

### **bse_monitor_simple.py**
- Main monitoring service
- Fetches BSE announcements page
- Processes new announcements
- Sends email alerts
- Runs continuously in background

### **config.py**
- Environment variable configuration
- Email settings (SMTP, recipients)
- BSE URLs and monitoring intervals
- Keyword lists for analysis
- Confidence scoring weights

### **xbrl_parser.py**
- Parses XBRL XML files
- Extracts financial data, dates, amounts
- Handles structured corporate data
- Error handling for malformed files

### **announcement_analyzer.py**
- Content analysis and scoring
- Keyword extraction and flagging
- Urgency and confidence calculation
- Sentiment analysis using TextBlob

### **email_sender.py**
- Multi-user email alerts
- HTML and plain text formatting
- SMTP configuration
- Error handling and retry logic

## 📧 **Email Alert Format**

```json
{
  "company": "ABC Ltd.",
  "timestamp": "2025-07-25 13:05",
  "announcement_text": "...",
  "flags": ["📈 Earnings Spike", "🛠️ Order Win"],
  "urgency_score": 0.87,
  "confidence_score": 0.91,
  "keywords": ["300% increase", "₹150 cr order", "MoD"]
}
```

## 🚀 **Deployment**

### **Current Deployment (Render.com)**
- **Status**: ✅ Active
- **URL**: https://render.com (dashboard)
- **Environment**: Python 3.11
- **Auto-restart**: Enabled
- **Monitoring**: 24/7

### **Configuration**
- **Email**: `9ranjal@gmail.com`
- **Check Interval**: 5 minutes
- **SMTP**: Gmail with App Password
- **Environment Variables**: Set via render.yaml

## 📊 **Monitoring**

### **Service Health**
- **Status**: Running continuously
- **Logs**: Available in Render dashboard
- **Auto-restart**: On failure
- **Email Alerts**: Active

### **Expected Behavior**
- Checks BSE every 5 minutes
- Parses new announcements
- Sends email alerts for new content
- Logs all activities

## 🔍 **Troubleshooting**

### **Common Issues**
1. **No email alerts**: Check SMTP configuration
2. **Service not running**: Check Render dashboard logs
3. **Build failures**: Verify requirements.txt

### **Logs**
- **Render Dashboard**: Real-time service logs
- **Email Delivery**: Check recipient inbox
- **Error Handling**: Automatic retry logic

## 📝 **Development**

### **Local Testing**
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (requires .env file)
python bse_monitor_simple.py
```

### **Environment Variables**
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=your_email@gmail.com
RECIPIENT_EMAILS=recipient1@gmail.com,recipient2@gmail.com
```

## 📄 **License**

This project is for educational and personal use. Please respect BSE's terms of service.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Last Updated**: July 25, 2025
**Status**: ✅ Production Ready
**Deployment**: Render.com 