# Persona-Driven AI Framework - Hackathon Project

## 🎯 Project Overview

An AI-powered software development automation framework that uses specialized AI personas to transform requirements into production-ready code through a structured workflow with human approval gates.

## 🤖 AI Personas

1. **Requirements AI** - Analyzes product requirements → Generates FEATURE_REQUIREMENTS.md
2. **Architect AI** - Designs system architecture → Generates SYSTEM_DESIGN.md
3. **Planner AI** - Creates implementation plans → Generates IMPLEMENTATION_PLAN.md
4. **Developer AI** - Generates code scaffolding → Generates code files
5. **Unit Test AI** - Generates unit tests → Generates test files + TEST_SUMMARY.md

## 🚦 Workflow with Approval Gates

```
Requirements Input
       ↓
[Requirements AI] → FEATURE_REQUIREMENTS.md
       ↓
   🚦 Gate 1: Human Review
       ↓
[Architect AI] → SYSTEM_DESIGN.md
       ↓
   🚦 Gate 2: Human Review
       ↓
[Planner AI] → IMPLEMENTATION_PLAN.md
       ↓
   🚦 Gate 3: Human Review
       ↓
[Developer AI] → Generated Code
       ↓
   🚦 Gate 4: Human Review
       ↓
[Unit Test AI] → Unit Tests
       ↓
   🚦 Gate 5: Human Review
       ↓
   ✅ Complete
```

## 🚀 Quick Start

See **[QUICK_START.md](QUICK_START.md)** for 5-minute setup guide.

```bash
cd persona-framework
./setup.sh
# Edit .env and add GEMINI_API_KEY
source venv/bin/activate
python test_workflow.py
```

## 📁 Project Structure

```
hackathon/
├── persona-framework/          # Core AI framework
│   ├── personas/              # 5 AI personas
│   ├── workflow_engine/       # Orchestrator with approval gates
│   ├── context_bootstrap/     # Project context generator
│   ├── main.py               # FastAPI service
│   └── test_workflow.py      # End-to-end test
├── demo-app/                  # Developer Productivity Dashboard
│   ├── requirements.md        # Demo app requirements
│   ├── backend/              # FastAPI backend (to be implemented)
│   └── frontend/             # React frontend (to be implemented)
├── QUICK_START.md            # 5-minute setup guide
├── PROJECT_STATUS.md         # Detailed project status
└── README.md                 # This file
```

## 🎬 Demo Application

**Developer Productivity Dashboard** - A comprehensive dashboard that:
- Integrates with GitHub/GitLab for commit and PR data
- Visualizes team productivity metrics with charts
- Generates AI-powered insights using Gemini
- Tracks sprint velocity and burndown
- Provides actionable recommendations

This demo app showcases how the framework generates:
- Complete requirements documentation
- System architecture with diagrams
- Implementation plans with tasks
- React component scaffolding
- FastAPI endpoint implementations
- Comprehensive unit tests

## 🛠️ Technology Stack

**Framework**:
- Python 3.9+
- Google Gemini 1.5 Pro
- FastAPI
- Cloud Firestore (optional)
- Cloud Storage (optional)

**Demo App**:
- Frontend: React + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Database: Cloud Firestore
- AI: Google Gemini API
- Deployment: Cloud Run

## 📊 Current Status

✅ **COMPLETE** - Core framework ready for testing
- All 5 AI personas implemented
- Workflow orchestrator with 5 approval gates
- Context bootstrap system
- FastAPI REST API service
- Demo app requirements document
- End-to-end test script
- Setup automation

See **[PROJECT_STATUS.md](PROJECT_STATUS.md)** for detailed status.

## 🎯 Next Steps

1. ✅ Test framework with demo app requirements
2. ⏳ Implement demo app backend (Hours 11-14)
3. ⏳ Implement demo app frontend (Hours 14-16)
4. ⏳ Deploy to Cloud Run (Hours 16-18)
5. ⏳ Write blog post and create demo (Hours 18-24)

## 🎤 Demo Talking Points

1. **Problem**: Manual software development is slow and error-prone
2. **Solution**: AI personas automate requirements → architecture → code → tests
3. **Innovation**: Human approval gates ensure quality and control
4. **Demo**: Show live workflow execution generating complete documentation and code
5. **Impact**: 10x faster development with maintained quality

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Detailed project status
- **[persona-framework/README.md](persona-framework/README.md)** - Framework documentation
- **[demo-app/requirements.md](demo-app/requirements.md)** - Demo app requirements

## 🔑 Configuration

Required:
- `GEMINI_API_KEY` - Get from https://makersuite.google.com/app/apikey

Optional (for cloud deployment):
- `GOOGLE_CLOUD_PROJECT` - GCP project ID
- `STORAGE_BUCKET` - Cloud Storage bucket name

## 🧪 Testing

```bash
# Test complete workflow
python test_workflow.py

# Start API service
python main.py

# Test API endpoint
curl http://localhost:8080/
```

## 📝 License

MIT

## 👥 Team

Built for Google Cloud Hackathon 2024

---

**Ready to revolutionize software development with AI! 🚀**

