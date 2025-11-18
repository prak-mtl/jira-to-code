# Persona Framework - Cloud Run Deployment Summary

This directory contains deployment resources for the Persona Framework on Google Cloud Run.

---

## 📁 Deployment Files

All deployment files are located in `persona-framework/`:

| File | Description |
|------|-------------|
| `Dockerfile` | Container image definition |
| `.dockerignore` | Files to exclude from Docker build |
| `deploy-cloud-run.sh` | Automated deployment script |
| `CLOUD_RUN_QUICK_START.md` | 5-minute quick start guide |
| `DEPLOYMENT_GUIDE.md` | Complete deployment documentation |
| `API_USAGE_EXAMPLES.md` | API integration examples |

---

## 🚀 Quick Deployment

```bash
cd persona-framework
export GEMINI_API_KEY="your-gemini-api-key"
./deploy-cloud-run.sh YOUR-PROJECT-ID europe-west1
```

---

## 📚 Documentation

### For First-Time Deployment
Start with **[CLOUD_RUN_QUICK_START.md](../../persona-framework/CLOUD_RUN_QUICK_START.md)**

### For Detailed Configuration
See **[DEPLOYMENT_GUIDE.md](../../persona-framework/DEPLOYMENT_GUIDE.md)**

### For API Integration
See **[API_USAGE_EXAMPLES.md](../../persona-framework/API_USAGE_EXAMPLES.md)**

---

## 🎯 What Gets Deployed

- **Service**: FastAPI application with 5 AI personas
- **Container**: Python 3.11 with all dependencies
- **Storage**: Google Cloud Storage for artifacts
- **Database**: Firestore for workflow state (optional)
- **Scaling**: Auto-scaling from 0 to 10 instances
- **Region**: Configurable (default: europe-west1)

---

## 💰 Cost Estimate

- **Free Tier**: 2M requests/month
- **Light Usage**: $0-5/month
- **Medium Usage**: $10-20/month
- **Heavy Usage**: $50-100/month

---

## 🔗 Quick Links

- [Cloud Run Console](https://console.cloud.google.com/run)
- [Cloud Storage Console](https://console.cloud.google.com/storage)
- [Firestore Console](https://console.cloud.google.com/firestore)
- [Gemini API Keys](https://aistudio.google.com/app/apikey)

---

## ✅ Deployment Checklist

- [ ] Google Cloud account with billing enabled
- [ ] gcloud CLI installed and authenticated
- [ ] Gemini API key obtained
- [ ] Project ID selected
- [ ] Region chosen
- [ ] Deployment script executed
- [ ] Service URL obtained
- [ ] Health check passed
- [ ] Test workflow executed
- [ ] API documentation accessible

---

## 🆘 Support

For issues or questions:
1. Check the [DEPLOYMENT_GUIDE.md](../../persona-framework/DEPLOYMENT_GUIDE.md) troubleshooting section
2. Review Cloud Run logs: `gcloud run services logs tail persona-framework-api`
3. Check service status: `gcloud run services describe persona-framework-api`

---

**Ready to deploy?** Navigate to `persona-framework/` and follow the [CLOUD_RUN_QUICK_START.md](../../persona-framework/CLOUD_RUN_QUICK_START.md)!

