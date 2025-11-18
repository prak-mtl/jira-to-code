# Deployment Guide

This guide covers deploying the Developer Productivity Dashboard to production.

## Architecture

- **Backend**: Google Cloud Run (containerized FastAPI)
- **Frontend**: Vercel (static React app)
- **Database**: DynamoDB (optional, for full features)

## Prerequisites

### Backend Deployment
- Google Cloud account
- `gcloud` CLI installed
- Docker installed (for local testing)
- Project ID from Google Cloud Console

### Frontend Deployment
- Vercel account (free tier works)
- Node.js 18+ installed

## Quick Deployment

### 1. Deploy Backend to Cloud Run

```bash
cd demo-app/backend

# Make script executable
chmod +x deploy-cloud-run.sh

# Deploy (replace with your project ID)
./deploy-cloud-run.sh your-project-id us-central1
```

This will:
- Build a Docker container
- Push to Google Container Registry
- Deploy to Cloud Run
- Output the service URL

**Example output:**
```
Service URL: https://dev-productivity-api-xxxxx-uc.a.run.app
```

### 2. Deploy Frontend to Vercel

```bash
cd demo-app/frontend

# Make script executable
chmod +x deploy-vercel.sh

# Deploy (use the Cloud Run URL from step 1)
./deploy-vercel.sh https://dev-productivity-api-xxxxx-uc.a.run.app
```

This will:
- Build the React app
- Deploy to Vercel
- Output the deployment URL

## Manual Deployment

### Backend (Cloud Run)

1. **Build Docker image:**
```bash
cd demo-app/backend
docker build -t dev-productivity-api .
```

2. **Test locally:**
```bash
docker run -p 8000:8000 dev-productivity-api
curl http://localhost:8000/health
```

3. **Push to GCR:**
```bash
gcloud auth configure-docker
docker tag dev-productivity-api gcr.io/YOUR_PROJECT_ID/dev-productivity-api
docker push gcr.io/YOUR_PROJECT_ID/dev-productivity-api
```

4. **Deploy to Cloud Run:**
```bash
gcloud run deploy dev-productivity-api \
  --image gcr.io/YOUR_PROJECT_ID/dev-productivity-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

### Frontend (Vercel)

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Set environment variable:**
```bash
cd demo-app/frontend
echo "VITE_API_BASE_URL=https://your-backend-url.run.app" > .env.production
```

4. **Deploy:**
```bash
vercel --prod
```

## Alternative: Deploy Frontend to Firebase Hosting

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting

# Build
npm run build

# Deploy
firebase deploy --only hosting
```

## Environment Variables

### Backend
No environment variables required for basic demo.

For full features, add:
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `GITLAB_CLIENT_ID`
- `GITLAB_CLIENT_SECRET`
- `JWT_SECRET`
- `GEMINI_API_KEY`

### Frontend
- `VITE_API_BASE_URL` - Backend API URL

## Testing Deployment

### Backend
```bash
curl https://your-backend-url.run.app/health
curl "https://your-backend-url.run.app/metrics/pr_analytics?team_id=demo"
```

### Frontend
Open in browser: `https://your-frontend-url.vercel.app`

## Costs

### Google Cloud Run
- Free tier: 2 million requests/month
- Estimated: $0-5/month for demo usage

### Vercel
- Free tier: Unlimited bandwidth for personal projects
- Estimated: $0/month

## Troubleshooting

### Backend won't start
- Check logs: `gcloud run logs read --service dev-productivity-api`
- Verify Docker image builds locally
- Check port configuration (must be 8000)

### Frontend can't reach backend
- Verify CORS is enabled in backend
- Check `VITE_API_BASE_URL` in `.env.production`
- Verify backend is publicly accessible

### CORS errors
Backend already has CORS configured for common origins. If you need to add more:
```python
# In simple_main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.vercel.app"],
    ...
)
```

## Next Steps

After deployment:
1. Test all API endpoints
2. Verify charts render correctly
3. Set up monitoring (Cloud Monitoring, Vercel Analytics)
4. Configure custom domain (optional)
5. Set up CI/CD (GitHub Actions)

