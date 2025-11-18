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

echo ""
echo "Setting Vercel environment variable..."
echo "VITE_API_BASE_URL=${API_URL}" | vercel env add VITE_API_BASE_URL production --force 2>/dev/null || echo "Note: Set env var manually in Vercel dashboard if this fails"

# Build the project
echo "Building project..."
npm run build

# Deploy to Vercel with environment variable
echo "Deploying to Vercel..."
vercel --prod --env VITE_API_BASE_URL="${API_URL}"

echo "=========================================="
echo "✅ Deployment complete!"
echo "=========================================="
echo ""
echo "Your app is now live on Vercel!"
echo "Check the URL above to access it."
echo ""
echo "⚠️  IMPORTANT: If the app doesn't work:"
echo "1. Go to Vercel Dashboard → Settings → Environment Variables"
echo "2. Add: VITE_API_BASE_URL = ${API_URL}"
echo "3. Redeploy from the Deployments tab"

