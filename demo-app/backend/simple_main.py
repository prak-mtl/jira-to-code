"""
Simple FastAPI backend with metrics endpoints
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random

app = FastAPI(
    title="Developer Productivity Dashboard API",
    description="Real-time developer productivity metrics and insights",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",  # Allow all Vercel deployments
        "https://dev-productivity-dashboard.vercel.app",  # Production URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response Models
class CommitActivity(BaseModel):
    date: str
    count: int
    authors: List[str]


class PRMetrics(BaseModel):
    total_prs: int
    merged_prs: int
    open_prs: int
    average_time_to_merge: float
    approval_rate: float
    average_review_time: float


class MetricData(BaseModel):
    timestamp: str
    value: float
    label: str


# Helper functions
def generate_commit_activity(start_date: datetime, end_date: datetime) -> List[CommitActivity]:
    """Generate mock commit activity data"""
    activities = []
    current_date = start_date
    
    while current_date <= end_date:
        count = random.randint(0, 20)
        all_authors = ["alice", "bob", "charlie", "diana", "eve"]
        num_authors = random.randint(1, min(count, len(all_authors))) if count > 0 else 0
        authors = random.sample(all_authors, num_authors) if count > 0 else []
        
        activities.append(CommitActivity(
            date=current_date.strftime("%Y-%m-%d"),
            count=count,
            authors=authors
        ))
        
        current_date += timedelta(days=1)
    
    return activities


def generate_pr_metrics() -> PRMetrics:
    """Generate mock PR metrics"""
    total_prs = random.randint(50, 150)
    merged_prs = int(total_prs * random.uniform(0.7, 0.9))
    open_prs = total_prs - merged_prs
    
    return PRMetrics(
        total_prs=total_prs,
        merged_prs=merged_prs,
        open_prs=open_prs,
        average_time_to_merge=round(random.uniform(2, 48), 2),
        approval_rate=round(random.uniform(75, 95), 2),
        average_review_time=round(random.uniform(1, 24), 2)
    )


# Endpoints
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Developer Productivity Dashboard API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/metrics/commit_frequency", response_model=List[CommitActivity])
async def get_commit_frequency(
    team_id: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """Get commit frequency data"""
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        activities = generate_commit_activity(start, end)
        return activities
    except Exception as e:
        return []


@app.get("/metrics/pr_analytics", response_model=PRMetrics)
async def get_pr_analytics(team_id: str = Query(...)):
    """Get PR analytics"""
    return generate_pr_metrics()


@app.get("/metrics/pr_velocity", response_model=MetricData)
async def get_pr_velocity(
    team_id: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """Get PR velocity"""
    return MetricData(
        timestamp=datetime.now().isoformat(),
        value=round(random.uniform(5, 25), 2),
        label="PRs per week"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

