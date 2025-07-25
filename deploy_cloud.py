#!/usr/bin/env python3
"""
Cloud Deployment Script for BSE Monitor
Deploy to Google Cloud Platform for 24/7 operation
"""

import os
import json

def create_dockerfile():
    """Create Dockerfile for containerization"""
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
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
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    print("✅ Created Dockerfile")

def create_docker_compose():
    """Create docker-compose.yml for easy deployment"""
    compose_content = """version: '3.8'

services:
  bse-monitor:
    build: .
    container_name: bse-monitor
    restart: unless-stopped
    environment:
      - TZ=Asia/Kolkata
    volumes:
      - ./logs:/app/logs
    networks:
      - bse-network

networks:
  bse-network:
    driver: bridge
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)
    print("✅ Created docker-compose.yml")

def create_cloud_run_config():
    """Create Cloud Run configuration"""
    cloud_run_content = """apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: bse-monitor
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-environment: gen2
    spec:
      containers:
      - image: gcr.io/YOUR_PROJECT_ID/bse-monitor
        env:
        - name: TZ
          value: "Asia/Kolkata"
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "0.5"
            memory: "256Mi"
"""
    
    with open('cloud-run.yaml', 'w') as f:
        f.write(cloud_run_content)
    print("✅ Created cloud-run.yaml")

def create_deployment_script():
    """Create deployment script for Google Cloud"""
    script_content = """#!/bin/bash
# BSE Monitor Cloud Deployment Script

echo "🚀 Deploying BSE Monitor to Google Cloud Platform..."

# Set your project ID
PROJECT_ID="your-project-id"
REGION="us-central1"

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Build and push Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/bse-monitor

# Deploy to Cloud Run
gcloud run deploy bse-monitor \\
  --image gcr.io/$PROJECT_ID/bse-monitor \\
  --platform managed \\
  --region $REGION \\
  --allow-unauthenticated \\
  --memory 512Mi \\
  --cpu 1 \\
  --max-instances 1 \\
  --timeout 3600 \\
  --set-env-vars TZ=Asia/Kolkata

echo "✅ BSE Monitor deployed successfully!"
echo "🌐 Service URL: https://bse-monitor-xxxxx-uc.a.run.app"
"""
    
    with open('deploy.sh', 'w') as f:
        f.write(script_content)
    os.chmod('deploy.sh', 0o755)
    print("✅ Created deploy.sh")

def create_github_actions():
    """Create GitHub Actions for automated deployment"""
    actions_content = """name: Deploy BSE Monitor

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v0
      with:
        project_id: ${{ secrets.GCP_PROJECT_ID }}
        service_account_key: ${{ secrets.GCP_SA_KEY }}
    
    - name: Build and Deploy
      run: |
        gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/bse-monitor
        gcloud run deploy bse-monitor \\
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/bse-monitor \\
          --platform managed \\
          --region us-central1 \\
          --allow-unauthenticated \\
          --memory 512Mi \\
          --cpu 1 \\
          --max-instances 1
"""
    
    os.makedirs('.github/workflows', exist_ok=True)
    with open('.github/workflows/deploy.yml', 'w') as f:
        f.write(actions_content)
    print("✅ Created GitHub Actions workflow")

def main():
    """Create all deployment files"""
    print("🚀 Creating Cloud Deployment Files")
    print("=" * 50)
    
    create_dockerfile()
    create_docker_compose()
    create_cloud_run_config()
    create_deployment_script()
    create_github_actions()
    
    print("\n📋 Deployment Options:")
    print("1. 🐳 Docker Compose (Local/Server)")
    print("2. ☁️  Google Cloud Run (Recommended)")
    print("3. 🐙 GitHub Actions (Automated)")
    print("4. 📱 Heroku (Alternative)")
    
    print("\n🔧 Quick Start (Google Cloud):")
    print("1. Install Google Cloud SDK")
    print("2. Run: gcloud auth login")
    print("3. Run: ./deploy.sh")
    print("4. Monitor will run 24/7 in the cloud!")

if __name__ == "__main__":
    main() 