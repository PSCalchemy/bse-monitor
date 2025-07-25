FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py ./
COPY .env ./

# Create non-root user
RUN useradd -m -u 1000 bseuser && chown -R bseuser:bseuser /app
USER bseuser

# Run the monitor
CMD ["python", "bse_monitor.py"]
