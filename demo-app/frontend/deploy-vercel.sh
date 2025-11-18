#!/bin/bash

# Deploy frontend to Vercel
# Usage: ./deploy-vercel.sh [API_URL]

set -e

API_URL=${1:-"http://localhost:8000"}

echo "=========================================="
echo "Deploying Frontend to Vercel"
echo "=========================================="
echo "API URL: ${API_URL}"
echo "=========================================="

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Update .env with production API URL
echo "VITE_API_BASE_URL=${API_URL}" > .env.production

# Build the project
echo "Building project..."
npm run build

# Deploy to Vercel
echo "Deploying to Vercel..."
vercel --prod

echo "=========================================="
echo "✅ Deployment complete!"
echo "=========================================="
echo ""
echo "Your app is now live on Vercel!"
echo "Check the URL above to access it."

