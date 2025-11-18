# Quick Reference Card

## 🚀 Start Demo (30 seconds)
```bash
cd demo-app
./start-demo.sh
```
Open: http://localhost:3000

## 🛑 Stop Demo
```bash
./stop-demo.sh
```

## 🔗 URLs
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Test
```bash
python3 test_integration.py
```

## 📦 Deploy

### Backend (Cloud Run)
```bash
cd backend
./deploy-cloud-run.sh YOUR_PROJECT_ID
```

### Frontend (Vercel)
```bash
cd frontend
./deploy-vercel.sh https://your-api-url.run.app
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/metrics/commit_frequency` | GET | Commit activity |
| `/metrics/pr_analytics` | GET | PR metrics |
| `/metrics/pr_velocity` | GET | PR velocity |

### Example API Call
```bash
curl "http://localhost:8000/metrics/pr_analytics?team_id=demo"
```

## 🗂️ Project Structure
```
demo-app/
├── backend/
│   ├── simple_main.py      # FastAPI app
│   ├── Dockerfile          # Container
│   └── deploy-cloud-run.sh # Deploy script
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   └── types/          # TypeScript types
│   └── deploy-vercel.sh    # Deploy script
├── start-demo.sh           # Quick start
├── stop-demo.sh            # Stop servers
└── test_integration.py     # Tests
```

## 📚 Documentation
- `README.md` - Overview
- `DEPLOYMENT.md` - Deploy guide
- `DEMO_SCRIPT.md` - Presentation
- `PROJECT_STATUS.md` - Status
- `COMPLETION_SUMMARY.md` - Summary

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

### API not responding
```bash
# Check backend logs
tail -f backend/backend.log

# Test health endpoint
curl http://localhost:8000/health
```

### CORS errors
- Backend already configured for localhost:3000
- For production, update CORS in `simple_main.py`

## 💡 Tips

1. **Always start from demo-app directory**
2. **Use ./start-demo.sh for quickest setup**
3. **Check logs if something fails**
4. **Backend must start before frontend**
5. **Use Ctrl+C to stop log tailing**

## 🎯 Demo Checklist

Before presenting:
- [ ] Run `./start-demo.sh`
- [ ] Open http://localhost:3000
- [ ] Verify charts load
- [ ] Have DEMO_SCRIPT.md ready
- [ ] Test API with curl
- [ ] Prepare to show code

## 📞 Support

- Check logs: `backend/backend.log`, `frontend/frontend.log`
- Run tests: `python3 test_integration.py`
- Read docs: `README.md`, `DEPLOYMENT.md`
- View status: `PROJECT_STATUS.md`

---

**Quick Start**: `./start-demo.sh` → http://localhost:3000 → Done! 🎉

