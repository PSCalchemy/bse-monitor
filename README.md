# BSE Corporate Announcement Monitor

A real-time monitoring system for BSE (Bombay Stock Exchange) corporate announcements that automatically parses XBRL files, analyzes content, and sends email alerts to multiple recipients.

## Features

- 🔍 **Real-time Monitoring**: Continuously monitors BSE announcements page
- 📊 **XBRL Parsing**: Extracts structured data from XBRL files
- 🎯 **Smart Analysis**: Analyzes announcements for urgency, keywords, and sentiment
- 📧 **Multi-user Alerts**: Sends formatted email alerts to multiple recipients
- 🚨 **Urgency Scoring**: Intelligent scoring system for announcement importance
- 🏷️ **Flagging System**: Automatic flagging of earnings spikes, order wins, etc.
- 📈 **Key Metrics Extraction**: Extracts financial metrics and business data

## Email Alert Format

Each email alert includes:
- Company name and timestamp
- Urgency and confidence scores
- Relevant flags (📈 Earnings Spike, 🛠️ Order Win, etc.)
- Extracted keywords and key metrics
- Parsed announcement text
- Sentiment analysis

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` with your email configuration:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   SENDER_EMAIL=your_email@gmail.com
   RECIPIENT_EMAILS=user1@example.com,user2@example.com,user3@example.com
   ```

4. **For Gmail users**: 
   - Enable 2-factor authentication
   - Generate an App Password
   - Use the App Password in `SMTP_PASSWORD`

## Usage

### Testing the System

Before running the monitor, test your configuration:

```bash
python test_monitor.py
```

This will test:
- Email configuration
- XBRL parsing
- Announcement analysis
- Send a test email

### Running the Monitor

Start the monitoring service:

```bash
python bse_monitor.py
```

The system will:
- Check for new announcements every 5 minutes (configurable)
- Parse XBRL files when available
- Analyze announcements for urgency and relevance
- Send email alerts to all configured recipients

### Configuration Options

Edit `config.py` to customize:

- **Monitoring interval**: `CHECK_INTERVAL_MINUTES`
- **Urgency keywords**: `URGENCY_KEYWORDS`
- **Confidence weights**: `CONFIDENCE_WEIGHTS`
- **Logging settings**: `LOG_LEVEL`, `LOG_FILE`

## File Structure

```
bse-monitor/
├── bse_monitor.py          # Main monitoring script
├── config.py              # Configuration settings
├── xbrl_parser.py         # XBRL file parser
├── announcement_analyzer.py # Content analysis engine
├── email_sender.py        # Email alert system
├── test_monitor.py        # System testing script
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
└── .env                  # Your configuration (create this)
```

## How It Works

1. **Web Scraping**: Monitors the BSE announcements page for new entries
2. **XBRL Processing**: Downloads and parses XBRL files for structured data
3. **Content Analysis**: Analyzes text for keywords, urgency indicators, and sentiment
4. **Scoring**: Calculates urgency and confidence scores based on multiple factors
5. **Alert Generation**: Creates formatted email alerts with analysis results
6. **Multi-user Delivery**: Sends alerts to all configured recipients

## Urgency Scoring

The system calculates urgency scores based on:
- Presence of financial keywords (₹ amounts, percentages)
- Government/defense related content (MoD, defense orders)
- Time-sensitive indicators (urgent, immediate, breaking)
- Large monetary values (crore/lakh amounts)
- Number of relevant flags triggered

## Flagging System

Automatic flags are generated for:
- 📈 **Earnings Spike**: Profit, revenue, growth announcements
- 🛠️ **Order Win**: Contract wins, project awards, MoD orders
- 💰 **Financial**: Dividends, mergers, investments
- ⚡ **Breaking**: Urgent, important, critical announcements

## Troubleshooting

### Common Issues

1. **Email not sending**:
   - Check SMTP credentials in `.env`
   - For Gmail, ensure App Password is used
   - Verify recipient emails are correct

2. **No announcements found**:
   - Check internet connection
   - Verify BSE website accessibility
   - Review logs for scraping errors

3. **XBRL parsing errors**:
   - Some announcements may not have XBRL files
   - Check logs for specific parsing errors

### Logs

Monitor the system logs:
- `bse_monitor.log`: Main application logs
- Console output: Real-time status updates

## Security Notes

- Store sensitive credentials in `.env` file (not in version control)
- Use App Passwords for Gmail instead of regular passwords
- Regularly update dependencies for security patches

## Customization

### Adding New Keywords

Edit `URGENCY_KEYWORDS` in `config.py`:

```python
URGENCY_KEYWORDS = {
    "📈 Earnings Spike": [
        "profit", "earnings", "revenue", "growth", "increase",
        # Add your keywords here
    ],
    # Add new flag categories
}
```

### Modifying Email Templates

Edit `email_sender.py` to customize email formatting and content.

### Adjusting Scoring

Modify scoring algorithms in `announcement_analyzer.py` to match your requirements.

## Support

For issues or questions:
1. Check the logs for error messages
2. Run `test_monitor.py` to verify configuration
3. Review this README for common solutions

## License

This project is for educational and personal use. Please respect BSE's terms of service and rate limiting policies. 