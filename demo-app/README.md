# Developer Productivity Dashboard - Demo Application

**Status**: ✅ **DEMO READY** | **Built in 4 hours** | **2,800+ lines of code generated**

A full-stack web application that visualizes developer productivity metrics with real-time charts and analytics. This application was **100% generated** using the Persona-Driven AI Framework, demonstrating **97% time savings** compared to traditional development.

## 🌐 Live Demo

**🎯 Try it now**: [https://dev-productivity-dashboard.vercel.app](https://dev-productivity-dashboard.vercel.app)
**📚 API Documentation**: [Cloud Run API Docs](https://dev-productivity-api-meinl6j2jq-ew.a.run.app/)
**💻 Source Code**: [GitHub Repository](https://github.com/prak-mtl/persona-framework)
**📝 Blog Post**: [Read the full story on Medium](https://medium.com/@prakmtl)

> **Note**: Update URLs above after deployment. See `DEPLOY_NOW.md` for deployment instructions.

## 🎯 Quick Start (30 seconds)

```bash
cd demo-app
./start-demo.sh
```

Then open http://localhost:3000 in your browser!

To stop:
```bash
./stop-demo.sh
```

## 📁 Directory Structure

```
demo-app/
├── backend/                    # Python backend services
│   ├── app/                   # FastAPI application
│   │   ├── api/v1/           # API endpoints
│   │   ├── auth/             # OAuth & JWT authentication
│   │   └── services/         # Business logic
│   └── ingestor_lambda/      # Data ingestion services
│       └── integrations/     # GitHub/GitLab API clients
├── frontend/                   # React TypeScript frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API client
│   │   └── types/            # TypeScript definitions
│   └── package.json
├── infrastructure/             # Infrastructure as Code
│   ├── serverless.yml        # Serverless Framework
│   ├── dynamodb_schema.yaml  # CloudFormation
│   └── terraform/            # Terraform configs
├── demo_data/                  # Sample data
│   ├── mock_data.json        # Static mock data
│   └── generate_demo_data.py # Data generator
└── generated_code.json         # Previously generated models

```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS Account (for deployment)
- GitHub/GitLab OAuth App credentials
- Google Gemini API key (optional, for AI insights)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GITHUB_CLIENT_ID=your_github_client_id
export GITHUB_CLIENT_SECRET=your_github_client_secret
export GITLAB_CLIENT_ID=your_gitlab_client_id
export GITLAB_CLIENT_SECRET=your_gitlab_client_secret
export JWT_SECRET=your_jwt_secret
export GEMINI_API_KEY=your_gemini_api_key

# Run locally
cd app
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Set environment variables
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

### 3. Infrastructure Deployment

#### Option A: Serverless Framework

```bash
cd infrastructure
serverless deploy --stage dev
```

#### Option B: Terraform

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

### 4. Load Demo Data

```bash
cd demo_data
python generate_demo_data.py
```

This generates `generated_demo_data.json` with:
- 30 days of commit activity
- 20 pull requests with reviews
- 6 sprints with velocity data
- AI insights
- Contributor statistics

## 🔧 Configuration

### Environment Variables

#### Backend
```bash
GITHUB_CLIENT_ID=<your_github_oauth_app_client_id>
GITHUB_CLIENT_SECRET=<your_github_oauth_app_secret>
GITLAB_CLIENT_ID=<your_gitlab_oauth_app_client_id>
GITLAB_CLIENT_SECRET=<your_gitlab_oauth_app_secret>
GEMINI_API_KEY=<your_google_gemini_api_key>
JWT_SECRET=<random_secret_for_jwt_signing>
METRICS_TABLE_NAME=DeveloperProductivityMetrics
RAW_EVENTS_TABLE_NAME=DeveloperProductivityRawEvents
SPRINTS_TABLE_NAME=DeveloperProductivitySprints
USERS_TABLE_NAME=DeveloperProductivityUsers
AI_INSIGHTS_TABLE_NAME=DeveloperProductivityAIInsights
```

#### Frontend
```bash
VITE_API_BASE_URL=http://localhost:8000  # or your deployed API URL
```

## 📚 Key Components

### Backend

- **`backend/app/auth/oauth.py`** - OAuth 2.0 implementation for GitHub/GitLab
- **`backend/app/api/v1/auth.py`** - Authentication API endpoints
- **`backend/app/services/user_service.py`** - User management with DynamoDB
- **`backend/ingestor_lambda/integrations/github_client.py`** - GitHub API client
- **`backend/ingestor_lambda/integrations/gitlab_client.py`** - GitLab API client

### Frontend

- **`frontend/src/components/Dashboard.tsx`** - Main dashboard component
- **`frontend/src/components/charts/CommitActivityChart.tsx`** - Commit activity visualization
- **`frontend/src/components/charts/PRMetricsChart.tsx`** - PR metrics visualization
- **`frontend/src/services/api.ts`** - API client with Axios
- **`frontend/src/types/index.ts`** - TypeScript type definitions

### Infrastructure

- **`infrastructure/serverless.yml`** - 7 Lambda functions, API Gateway, SQS, S3
- **`infrastructure/dynamodb_schema.yaml`** - 5 DynamoDB tables (CloudFormation)
- **`infrastructure/terraform/dynamodb.tf`** - DynamoDB tables (Terraform)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📖 Documentation

For detailed documentation, see the parent directory:
- **[../README.md](../README.md)** - Main project documentation
- **[../FEATURE_REQUIREMENTS.md](../FEATURE_REQUIREMENTS.md)** - Feature requirements
- **[../IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md)** - Implementation roadmap
- **[../SYSTEM_DESIGN.md](../SYSTEM_DESIGN.md)** - Architecture details
- **[../INDEX.md](../INDEX.md)** - File navigation guide

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Verify all environment variables are set
- Check if port 8000 is available

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check if port 5173 (Vite default) is available

### Deployment fails
- Verify AWS credentials: `aws sts get-caller-identity`
- Check IAM permissions for Lambda, DynamoDB, API Gateway
- Review CloudFormation/Terraform error messages

## 📝 Notes

- This is a demo application with production-ready structure
- OAuth apps must be created on GitHub/GitLab before use
- AWS resources will incur costs (estimated $30-60/month for small teams)
- Demo data is provided for immediate testing without real integrations

---

**Generated**: 2024-11-17  
**Framework**: Persona-Driven AI Framework v1.0.0  
**Workflow**: DASHBOARD-001

