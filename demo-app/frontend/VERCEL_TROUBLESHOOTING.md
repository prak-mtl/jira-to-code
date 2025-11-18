# Vercel Deployment Troubleshooting

## Issue: App Not Working / Language Issues After Deployment

### Symptoms
- App loads but shows errors
- API calls fail
- Console shows "undefined" for API URL
- Language/locale issues

### Root Cause
Vite environment variables must be set **at build time**, not runtime. Vercel needs the `VITE_API_BASE_URL` during the build process.

---

## ✅ Solution: Set Environment Variables in Vercel

### Method 1: Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Select your project

2. **Add Environment Variable**
   - Click **Settings** tab
   - Click **Environment Variables** in sidebar
   - Click **Add New**

3. **Configure Variable**
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: Your Cloud Run URL (e.g., `https://dev-productivity-api-xxxxx-ew.a.run.app`)
   - **Environments**: Check ✅ Production (and optionally Preview, Development)
   - Click **Save**

4. **Redeploy**
   - Go to **Deployments** tab
   - Find the latest deployment
   - Click the **⋯** (three dots) menu
   - Click **Redeploy**
   - Wait for build to complete

5. **Verify**
   - Open your Vercel URL
   - Open browser console (F12)
   - Check for API calls - should go to your Cloud Run URL
   - No errors should appear

---

### Method 2: Vercel CLI

```bash
cd /Users/pmittal/Desktop/Code/hackathon/demo-app/frontend

# Add environment variable
vercel env add VITE_API_BASE_URL production

# When prompted, paste your Cloud Run URL:
# https://dev-productivity-api-xxxxx-ew.a.run.app

# Redeploy
vercel --prod
```

---

### Method 3: vercel.json Configuration

Create `vercel.json` in the frontend directory:

```json
{
  "env": {
    "VITE_API_BASE_URL": "https://dev-productivity-api-xxxxx-ew.a.run.app"
  },
  "build": {
    "env": {
      "VITE_API_BASE_URL": "https://dev-productivity-api-xxxxx-ew.a.run.app"
    }
  }
}
```

Then redeploy:
```bash
vercel --prod
```

---

## 🔍 Debugging Steps

### 1. Check Environment Variables in Vercel

```bash
# List all environment variables
vercel env ls

# Should show:
# VITE_API_BASE_URL (Production)
```

### 2. Check Build Logs

1. Go to Vercel Dashboard → Deployments
2. Click on the latest deployment
3. Check the **Build Logs**
4. Look for: `VITE_API_BASE_URL=https://...`
5. If not present, the variable wasn't set during build

### 3. Check Runtime in Browser

1. Open your deployed app
2. Open browser console (F12)
3. Type: `import.meta.env.VITE_API_BASE_URL`
4. Should show your Cloud Run URL
5. If shows `undefined`, rebuild with env var set

### 4. Check API Calls

1. Open browser Network tab (F12 → Network)
2. Reload the page
3. Look for API calls
4. Should go to: `https://dev-productivity-api-xxxxx-ew.a.run.app/...`
5. If going to `undefined` or `localhost`, env var not set

---

## 🚨 Common Mistakes

### ❌ Wrong: Setting .env.production locally
```bash
# This doesn't work for Vercel!
echo "VITE_API_BASE_URL=..." > .env.production
vercel --prod
```
**Why**: Vercel builds in its own environment, doesn't use your local .env files

### ✅ Right: Set in Vercel Dashboard or CLI
```bash
# This works!
vercel env add VITE_API_BASE_URL production
```

---

## 📝 Checklist

After deployment, verify:

- [ ] Environment variable set in Vercel Dashboard
- [ ] Variable shows in `vercel env ls`
- [ ] Redeployed after setting variable
- [ ] Build logs show the variable
- [ ] Browser console shows correct API URL
- [ ] API calls go to Cloud Run (not localhost)
- [ ] Dashboard loads without errors
- [ ] Charts display data

---

## 🔄 Quick Fix (If Still Not Working)

```bash
# 1. Remove existing deployment
vercel remove <deployment-url> --yes

# 2. Set environment variable
vercel env add VITE_API_BASE_URL production
# Enter: https://dev-productivity-api-xxxxx-ew.a.run.app

# 3. Fresh deployment
vercel --prod

# 4. Verify
curl https://your-app.vercel.app
```

---

## 💡 Pro Tips

1. **Always set env vars BEFORE deploying**
2. **Use Vercel Dashboard** - it's the most reliable method
3. **Redeploy after changing env vars** - changes don't apply to existing deployments
4. **Check build logs** - they show if env vars are set
5. **Test in browser console** - `import.meta.env.VITE_API_BASE_URL`

---

## 📞 Still Having Issues?

### Check CORS

If API calls fail with CORS errors:

1. Verify backend CORS settings in `simple_main.py`:
```python
allow_origins=[
    "https://*.vercel.app",
    "https://your-app.vercel.app"
]
```

2. Redeploy backend:
```bash
cd ../backend
./deploy-cloud-run.sh jira-to-code europe-west1
```

### Check Backend URL

Make sure your Cloud Run URL is correct:
```bash
# Get Cloud Run URL
gcloud run services describe dev-productivity-api \
  --region europe-west1 \
  --format 'value(status.url)'
```

---

## ✅ Success Indicators

Your deployment is working when:

1. ✅ App loads without errors
2. ✅ Dashboard shows data
3. ✅ Charts render correctly
4. ✅ Browser console has no errors
5. ✅ Network tab shows API calls to Cloud Run
6. ✅ No CORS errors

---

**Need more help?** Check the main `DEPLOYMENT.md` guide.

