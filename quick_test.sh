#!/bin/bash
# Quick test script for BSE Monitor endpoints

echo "🚀 BSE Monitor Quick Test"
echo "========================"

echo ""
echo "📋 Instructions:"
echo "1. Go to https://render.com"
echo "2. Find your 'bse-monitor' service"
echo "3. Copy the URL (should look like: https://bse-monitor-xxxxx.onrender.com)"
echo "4. Paste it below"
echo ""

read -p "Enter your service URL: " SERVICE_URL

if [ -z "$SERVICE_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

echo ""
echo "🎯 Testing service at: $SERVICE_URL"
echo ""

# Test health endpoint
echo "🔍 Testing Health Check..."
curl -s "$SERVICE_URL/health" | jq '.' 2>/dev/null || curl -s "$SERVICE_URL/health"
echo ""

# Test home page
echo "🔍 Testing Home Page..."
curl -s "$SERVICE_URL/" | jq '.' 2>/dev/null || curl -s "$SERVICE_URL/"
echo ""

# Test status page
echo "🔍 Testing Status Page..."
curl -s "$SERVICE_URL/status" | jq '.' 2>/dev/null || curl -s "$SERVICE_URL/status"
echo ""

echo "✅ Test completed!"
echo "📧 If working, email alerts will be sent to: 9ranjal@gmail.com" 