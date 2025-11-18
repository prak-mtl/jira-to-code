# Deploy Now - Step by Step Guide

**Project**: jira-to-code  
**Region**: europe-west1  
**Estimated Time**: 30 minutes

---

## Prerequisites Check

```bash
# 1. Check if gcloud is installed
gcloud --version

# 2. Login to Google Cloud
gcloud auth login

# 3. Set your project
gcloud config set project jira-to-code

# 4. Enable required APIs (run once)
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

---

## Deploy Backend to Cloud Run

```bash
# Navigate to backend directory
cd /Users/pmittal/Desktop/Code/hackathon/demo-app/backend

# Deploy using the script
./deploy-cloud-run.sh jira-to-code europe-west1
```

**This will**:
- Build Docker container
- Push to Google Container Registry
- Deploy to Cloud Run
- Output your backend URL

**Expected Output**:
```
Service URL: https://dev-productivity-api-xxxxx-ew.a.run.app
```

**Save this URL!** You'll need it for frontend deployment.

---

## Deploy Frontend to Vercel

### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI if not installed
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to frontend
cd /Users/pmittal/Desktop/Code/hackathon/demo-app/frontend

# Set the backend URL (use the URL from Cloud Run deployment)
export BACKEND_URL="https://dev-productivity-api-xxxxx-ew.a.run.app"

# Update .env.production
echo "VITE_API_BASE_URL=$BACKEND_URL" > .env.production

# Deploy to Vercel
vercel --prod
```

### Option B: Using Vercel Dashboard (Alternative)

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import from Git (connect your GitHub repo)
4. Set environment variable:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://dev-productivity-api-xxxxx-ew.a.run.app`
5. Click "Deploy"

---

## Update CORS in Backend

After deploying frontend, you need to update CORS settings:

1. Get your Vercel URL (e.g., `https://your-app.vercel.app`)

2. Edit `backend/simple_main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-app.vercel.app"  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Redeploy backend:
```bash
cd backend
./deploy-cloud-run.sh jira-to-code europe-west1
```

---

## Test Deployment

### Test Backend
```bash
# Replace with your actual Cloud Run URL
curl https://dev-productivity-api-xxxxx-ew.a.run.app/health

# Test metrics endpoint
curl "https://dev-productivity-api-xxxxx-ew.a.run.app/metrics/pr_analytics?team_id=demo"
```

### Test Frontend
1. Open your Vercel URL in browser
2. Verify dashboard loads
3. Check that charts display data
4. Open browser console - should be no errors

---

## Troubleshooting

### Backend deployment fails
```bash
# Check logs
gcloud run logs read --service dev-productivity-api --region europe-west1

# Verify Docker builds locally
cd backend
docker build -t test-build .
docker run -p 8000:8000 test-build
```

### Frontend can't reach backend
1. Check CORS settings in `simple_main.py`
2. Verify `VITE_API_BASE_URL` in Vercel environment variables
3. Check browser console for CORS errors

### Cloud Run cold starts
- First request may take 3-5 seconds
- Subsequent requests will be fast
- This is normal for serverless

---

## Save Your URLs

After successful deployment, save these:

```
Backend URL: https://dev-productivity-api-xxxxx-ew.a.run.app
Frontend URL: https://your-app.vercel.app
API Docs: https://dev-productivity-api-xxxxx-ew.a.run.app/docs
```

Update these in:
- [ ] `demo-app/README.md`
- [ ] `demo-app/PROJECT_STATUS.md`
- [ ] Blog post (when writing)
- [ ] Hackathon submission

---

## Estimated Costs

**Cloud Run**:
- Free tier: 2 million requests/month
- Expected: $0-2/month for demo

**Vercel**:
- Free tier: Unlimited for personal projects
- Expected: $0/month

**Total**: ~$0-2/month

---

## Next Steps After Deployment

1. ✅ Test both URLs thoroughly
2. ✅ Take screenshots of live demo
3. ✅ Update documentation with live URLs
4. ✅ Proceed to blog post writing
5. ✅ Submit to hackathon with live demo link

---

**Ready to deploy!** Start with the backend deployment script. 🚀

