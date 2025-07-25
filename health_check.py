#!/usr/bin/env python3
# Health check endpoint for Railway
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'BSE Monitor',
        'timestamp': datetime.now().isoformat(),
        'email': '9ranjal@gmail.com'
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'BSE Monitor is running',
        'status': 'active',
        'email': '9ranjal@gmail.com'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
