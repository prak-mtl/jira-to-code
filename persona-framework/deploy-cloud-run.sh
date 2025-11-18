#!/bin/bash

# Deploy persona-framework to Google Cloud Run
# Usage: ./deploy-cloud-run.sh [PROJECT_ID] [REGION]

set -e

# Configuration
PROJECT_ID=${1:-"jira-to-code"}
REGION=${2:-"europe-west1"}
SERVICE_NAME="persona-framework-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "=========================================="
echo "Deploying Persona Framework to Cloud Run"
echo "=========================================="
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo "=========================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY environment variable is not set"
    echo "You'll need to set it after deployment using:"
    echo "gcloud run services update ${SERVICE_NAME} --region ${REGION} --set-env-vars GEMINI_API_KEY=your-key"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Set project
echo "Setting project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable storage.googleapis.com

# Create storage bucket if it doesn't exist
BUCKET_NAME="persona-ai-artifacts-${PROJECT_ID}"
echo "Checking storage bucket..."
if ! gsutil ls -b gs://${BUCKET_NAME} &> /dev/null; then
    echo "Creating storage bucket: ${BUCKET_NAME}"
    gsutil mb -p ${PROJECT_ID} -l ${REGION} gs://${BUCKET_NAME}
else
    echo "Storage bucket already exists: ${BUCKET_NAME}"
fi

# Build container image
echo "Building container image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 2 \
    --min-instances 0 \
    --max-instances 10 \
    --timeout 900 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=${PROJECT_ID},STORAGE_BUCKET=${BUCKET_NAME},ENVIRONMENT=production \
    ${GEMINI_API_KEY:+--set-env-vars GEMINI_API_KEY=${GEMINI_API_KEY}}

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')

echo "=========================================="
echo "✅ Deployment complete!"
echo "=========================================="
echo "Service URL: ${SERVICE_URL}"
echo "API Docs: ${SERVICE_URL}/docs"
echo "Health check: ${SERVICE_URL}/"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test the API: curl ${SERVICE_URL}/"
echo "2. View API docs: open ${SERVICE_URL}/docs"
echo "3. Execute workflow:"
echo "   curl -X POST ${SERVICE_URL}/api/v1/workflow/execute \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"ticket_id\": \"TEST-001\", \"requirements\": \"Add user authentication\", \"auto_approve\": true}'"
echo ""
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Remember to set GEMINI_API_KEY:"
    echo "   gcloud run services update ${SERVICE_NAME} --region ${REGION} \\"
    echo "     --set-env-vars GEMINI_API_KEY=your-api-key"
fi
echo "=========================================="

