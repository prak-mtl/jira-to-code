# Persona-Driven AI Framework

AI-powered software development automation using specialized AI personas.

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GCP credentials and Gemini API key
```

### 2. Run Framework

```bash
# Start the API service
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 3. Execute Workflow

```bash
# Run test workflow
python test_workflow.py
```

## Architecture

- **personas/**: AI persona implementations (Requirements, Architect, Planner, Developer, UnitTest)
- **workflow_engine/**: Workflow orchestration with approval gates
- **context_bootstrap/**: Project context initialization
- **.ai/**: Generated context and workflow artifacts

## API Endpoints

- `POST /api/v1/workflow/execute` - Execute complete workflow
- `GET /api/v1/workflow/{ticket_id}/status` - Get workflow status
- `POST /api/v1/bootstrap` - Bootstrap new project
- `POST /api/v1/upload-requirements` - Upload requirements file

## Deployment

### Local Development
```bash
python main.py
# Or: uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Google Cloud Run (Production)

**Quick Deploy**:
```bash
cd persona-framework
export GEMINI_API_KEY="your-api-key"
./deploy-cloud-run.sh YOUR-PROJECT-ID europe-west1
```

**Documentation**:
- **[CLOUD_RUN_QUICK_START.md](CLOUD_RUN_QUICK_START.md)** - 5-minute deployment guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment documentation
- **[API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md)** - Integration examples and API usage

## License

MIT

