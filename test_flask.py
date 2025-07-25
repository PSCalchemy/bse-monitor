#!/usr/bin/env python3
"""
Simple Flask test app for Render deployment
"""

from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'BSE Monitor Test',
        'timestamp': datetime.now().isoformat(),
        'message': 'Flask app is running successfully'
    })

@app.route('/')
def home():
    """Home page endpoint"""
    return jsonify({
        'message': 'BSE Monitor Test is running',
        'status': 'active',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'message': 'Test endpoint working',
        'environment': os.environ.get('RENDER_ENVIRONMENT', 'unknown'),
        'port': os.environ.get('PORT', '8080')
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 