#!/bin/bash
# BSE Monitor Cloud Deployment Script

echo "🚀 Deploying BSE Monitor to Google Cloud Platform..."

# Set your project ID
PROJECT_ID="bse-monitor-1753456512"
REGION="us-central1"

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Build and push Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/bse-monitor

# Deploy to Cloud Run
gcloud run deploy bse-monitor \
  --image gcr.io/$PROJECT_ID/bse-monitor \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 1 \
  --timeout 3600 \
  --set-env-vars TZ=Asia/Kolkata

echo "✅ BSE Monitor deployed successfully!"
echo "🌐 Service URL: https://bse-monitor-xxxxx-uc.a.run.app"
