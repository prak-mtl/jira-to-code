from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

from workflow_engine.orchestrator import WorkflowOrchestrator, ApprovalStatus
from context_bootstrap.bootstrap import ContextBootstrap

load_dotenv()

app = FastAPI(
    title="Persona-Driven AI Framework",
    description="AI-powered software development automation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = WorkflowOrchestrator(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT', 'local-project'),
    bucket_name=os.getenv('STORAGE_BUCKET', 'local-bucket')
)

class WorkflowRequest(BaseModel):
    ticket_id: str
    requirements: str
    context: Optional[Dict[str, Any]] = None
    auto_approve: bool = False

class BootstrapRequest(BaseModel):
    project_name: str
    description: str
    tech_stack: list
    architecture_type: str = "microservices"

@app.get("/")
async def root():
    return {
        "service": "Persona-Driven AI Framework",
        "version": "1.0.0",
        "status": "running",
        "personas": ["Requirements AI", "Architect AI", "Planner AI", "Developer AI", "Unit Test AI"]
    }

@app.post("/api/v1/workflow/execute")
async def execute_workflow(request: WorkflowRequest):
    """
    Execute complete AI workflow: Requirements → Architecture → Planning → Code → Tests
    """
    try:
        # Auto-approve callback if requested
        def auto_approve_callback(stage: str, artifact_url: str) -> ApprovalStatus:
            print(f"🤖 Auto-approving {stage} stage")
            return ApprovalStatus.APPROVED
        
        results = orchestrator.execute_workflow_with_gates(
            ticket_id=request.ticket_id,
            requirements_doc=request.requirements,
            context=request.context,
            approval_callback=auto_approve_callback if request.auto_approve else None
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/workflow/{ticket_id}/status")
async def get_workflow_status(ticket_id: str):
    """Get status of a workflow execution"""
    status = orchestrator.get_workflow_status(ticket_id)
    if 'error' in status:
        raise HTTPException(status_code=404, detail=status['error'])
    return status

@app.post("/api/v1/bootstrap")
async def bootstrap_project(request: BootstrapRequest):
    """
    Bootstrap .ai/ directory structure for a new project
    """
    try:
        bootstrap = ContextBootstrap(project_root="./demo-app")
        
        project_info = {
            "name": request.project_name,
            "description": request.description,
            "tech_stack": request.tech_stack,
            "architecture_type": request.architecture_type
        }
        
        bootstrap.bootstrap(project_info)
        
        return {
            "status": "success",
            "message": f"Context bootstrapped for {request.project_name}",
            "ai_directory": str(bootstrap.ai_dir)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload-requirements")
async def upload_requirements(
    ticket_id: str,
    file: UploadFile = File(...),
    auto_approve: bool = False
):
    """
    Upload requirements document and execute workflow
    """
    try:
        # Read uploaded file
        content = await file.read()
        requirements_text = content.decode('utf-8')
        
        # Auto-approve callback if requested
        def auto_approve_callback(stage: str, artifact_url: str) -> ApprovalStatus:
            print(f"🤖 Auto-approving {stage} stage")
            return ApprovalStatus.APPROVED
        
        # Execute workflow
        results = orchestrator.execute_workflow_with_gates(
            ticket_id=ticket_id,
            requirements_doc=requirements_text,
            approval_callback=auto_approve_callback if auto_approve else None
        )
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

