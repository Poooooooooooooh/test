#!/bin/bash
# Quick deploy script for Google Cloud Run

# Set your project ID
PROJECT_ID="YOUR_PROJECT_ID"
SERVICE_NAME="piggy-expense-tracker"
REGION="us-central1"

# Build and deploy
echo "Building container..."
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}

echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image gcr.io/${PROJECT_ID}/${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json \
  --memory 512Mi \
  --timeout 300

echo "Deployment complete!"
echo "Your app URL will be shown above."

