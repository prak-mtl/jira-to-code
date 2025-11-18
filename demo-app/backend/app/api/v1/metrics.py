"""
Metrics API endpoints
Provides developer productivity metrics and analytics
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()


# Response Models
class CommitActivity(BaseModel):
    date: str
    count: int
    authors: List[str]


class PRMetrics(BaseModel):
    total_prs: int
    merged_prs: int
    open_prs: int
    average_time_to_merge: float  # in hours
    approval_rate: float  # percentage
    average_review_time: float  # in hours


class MetricData(BaseModel):
    timestamp: str
    value: float
    label: str


class Contributor(BaseModel):
    user_id: str
    username: str
    avatar_url: Optional[str]
    commits: int
    prs: int
    reviews: int


# Mock data generators
def generate_commit_activity(start_date: datetime, end_date: datetime) -> List[CommitActivity]:
    """Generate mock commit activity data"""
    import random
    
    activities = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate random commit count (0-20)
        count = random.randint(0, 20)
        
        # Generate random authors
        all_authors = ["alice", "bob", "charlie", "diana", "eve"]
        num_authors = random.randint(1, min(count, len(all_authors)))
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
    import random
    
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
@router.get("/commit_frequency", response_model=List[CommitActivity])
async def get_commit_frequency(
    team_id: str = Query(..., description="Team identifier"),
    start_date: str = Query(..., description="Start date (ISO format)"),
    end_date: str = Query(..., description="End date (ISO format)")
):
    """
    Get commit frequency data for a team within a date range
    """
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        if start > end:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Generate mock data
        activities = generate_commit_activity(start, end)
        
        return activities
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")


@router.get("/pr_analytics", response_model=PRMetrics)
async def get_pr_analytics(
    team_id: str = Query(..., description="Team identifier")
):
    """
    Get pull request analytics for a team
    """
    # Generate mock data
    metrics = generate_pr_metrics()
    return metrics


@router.get("/pr_velocity", response_model=MetricData)
async def get_pr_velocity(
    team_id: str = Query(..., description="Team identifier"),
    start_date: str = Query(..., description="Start date (ISO format)"),
    end_date: str = Query(..., description="End date (ISO format)")
):
    """
    Get PR velocity metric for a team
    """
    import random
    
    return MetricData(
        timestamp=datetime.now().isoformat(),
        value=round(random.uniform(5, 25), 2),
        label="PRs per week"
    )

