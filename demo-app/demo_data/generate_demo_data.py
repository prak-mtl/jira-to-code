"""
Script to generate and populate demo data for the Developer Productivity Dashboard.
This script creates realistic sample data for testing and demonstration purposes.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metrics_api.models import Metric


def generate_commit_activity(days: int = 30) -> List[Dict[str, Any]]:
    """Generate commit activity data for the specified number of days."""
    authors = ["alice", "bob", "charlie", "david", "eve"]
    activity = []
    
    end_date = datetime.utcnow()
    
    for i in range(days):
        date = end_date - timedelta(days=days - i - 1)
        
        # Simulate lower activity on weekends
        is_weekend = date.weekday() >= 5
        
        if is_weekend:
            count = random.randint(0, 5)
        else:
            count = random.randint(8, 25)
        
        # Select random authors for the day
        num_authors = min(count, random.randint(1, len(authors)))
        day_authors = random.sample(authors, num_authors) if count > 0 else []
        
        activity.append({
            "date": date.isoformat() + "Z",
            "count": count,
            "authors": day_authors
        })
    
    return activity


def generate_pull_requests(count: int = 20) -> List[Dict[str, Any]]:
    """Generate sample pull request data."""
    authors = ["alice", "bob", "charlie", "david", "eve"]
    reviewers = ["alice", "bob", "charlie", "david", "eve"]
    states = ["open", "merged", "closed"]
    
    prs = []
    
    for i in range(count):
        author = random.choice(authors)
        state = random.choices(states, weights=[0.2, 0.7, 0.1])[0]
        
        created_at = datetime.utcnow() - timedelta(days=random.randint(1, 30))
        updated_at = created_at + timedelta(hours=random.randint(1, 72))
        
        merged_at = None
        closed_at = None
        
        if state == "merged":
            merged_at = updated_at
        elif state == "closed":
            closed_at = updated_at
        
        # Generate reviews
        num_reviews = random.randint(1, 3)
        available_reviewers = [r for r in reviewers if r != author]
        review_users = random.sample(available_reviewers, min(num_reviews, len(available_reviewers)))
        
        reviews = []
        for j, reviewer in enumerate(review_users):
            review_state = random.choices(
                ["approved", "changes_requested", "commented"],
                weights=[0.7, 0.2, 0.1]
            )[0]
            
            submitted_at = created_at + timedelta(hours=random.randint(2, 48))
            
            reviews.append({
                "id": f"rev-{i}-{j}",
                "user": reviewer,
                "state": review_state,
                "submitted_at": submitted_at.isoformat() + "Z"
            })
        
        pr = {
            "id": f"pr-{i+1}",
            "number": 100 + i,
            "title": f"Feature/fix #{i+1}",
            "state": state,
            "author": author,
            "created_at": created_at.isoformat() + "Z",
            "updated_at": updated_at.isoformat() + "Z",
            "merged_at": merged_at.isoformat() + "Z" if merged_at else None,
            "closed_at": closed_at.isoformat() + "Z" if closed_at else None,
            "url": f"https://github.com/example/repo/pull/{100+i}",
            "repository": "example/repo",
            "additions": random.randint(10, 500),
            "deletions": random.randint(5, 200),
            "changed_files": random.randint(1, 15),
            "review_comments": random.randint(0, 20),
            "reviews": reviews
        }
        
        prs.append(pr)
    
    return prs


def calculate_pr_metrics(prs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate PR metrics from pull request data."""
    merged_prs = [pr for pr in prs if pr["state"] == "merged"]
    
    if not merged_prs:
        return {
            "average_time_to_merge": 0,
            "average_review_time": 0,
            "approval_rate": 0,
            "pr_size_distribution": {"small": 0, "medium": 0, "large": 0, "xlarge": 0}
        }
    
    # Calculate average time to merge
    merge_times = []
    for pr in merged_prs:
        created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
        merged = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
        hours = (merged - created).total_seconds() / 3600
        merge_times.append(hours)
    
    avg_merge_time = sum(merge_times) / len(merge_times)
    
    # Calculate average review time (time to first review)
    review_times = []
    for pr in prs:
        if pr["reviews"]:
            created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
            first_review = min(
                datetime.fromisoformat(r["submitted_at"].replace("Z", "+00:00"))
                for r in pr["reviews"]
            )
            hours = (first_review - created).total_seconds() / 3600
            review_times.append(hours)
    
    avg_review_time = sum(review_times) / len(review_times) if review_times else 0
    
    # Calculate approval rate
    approved_prs = sum(
        1 for pr in prs
        if any(r["state"] == "approved" for r in pr["reviews"])
    )
    approval_rate = (approved_prs / len(prs)) * 100 if prs else 0
    
    # PR size distribution
    size_dist = {"small": 0, "medium": 0, "large": 0, "xlarge": 0}
    for pr in prs:
        total_changes = pr["additions"] + pr["deletions"]
        if total_changes < 100:
            size_dist["small"] += 1
        elif total_changes < 500:
            size_dist["medium"] += 1
        elif total_changes < 1000:
            size_dist["large"] += 1
        else:
            size_dist["xlarge"] += 1
    
    return {
        "average_time_to_merge": round(avg_merge_time, 1),
        "average_review_time": round(avg_review_time, 1),
        "approval_rate": round(approval_rate, 1),
        "pr_size_distribution": size_dist
    }


def generate_sprints(count: int = 6) -> List[Dict[str, Any]]:
    """Generate sprint data."""
    sprints = []

    for i in range(count):
        sprint_num = 18 + i
        start_date = datetime.utcnow() - timedelta(days=(count - i) * 14)
        end_date = start_date + timedelta(days=13)

        capacity = random.randint(70, 85)
        completed = random.randint(int(capacity * 0.85), capacity)

        status = "completed"
        if i == count - 1:
            status = "active"

        sprints.append({
            "sprint_id": f"sprint-{sprint_num}",
            "name": f"Sprint {sprint_num}",
            "team_id": "default-team",
            "start_date": start_date.isoformat() + "Z",
            "end_date": end_date.isoformat() + "Z",
            "capacity": capacity,
            "completed_points": completed,
            "status": status
        })

    return sprints


def generate_sprint_velocity(sprints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate sprint velocity data from sprints."""
    velocity = []

    for sprint in sprints:
        if sprint["status"] == "completed":
            velocity_pct = (sprint["completed_points"] / sprint["capacity"]) * 100
            velocity.append({
                "sprint_name": sprint["name"],
                "planned_points": sprint["capacity"],
                "completed_points": sprint["completed_points"],
                "velocity": round(velocity_pct, 1)
            })

    return velocity


def main():
    """Generate all demo data and save to JSON file."""
    print("Generating demo data...")

    # Generate data
    commit_activity = generate_commit_activity(30)
    pull_requests = generate_pull_requests(20)
    pr_metrics = calculate_pr_metrics(pull_requests)
    sprints = generate_sprints(6)
    sprint_velocity = generate_sprint_velocity(sprints)

    # Load existing mock data for AI insights and contributors
    with open("mock_data.json", "r") as f:
        existing_data = json.load(f)

    # Combine all data
    demo_data = {
        "commit_activity": commit_activity,
        "pr_metrics": pr_metrics,
        "pull_requests": pull_requests,
        "sprints": sprints,
        "sprint_velocity": sprint_velocity,
        "ai_insights": existing_data.get("ai_insights", []),
        "contributors": existing_data.get("contributors", [])
    }

    # Save to file
    output_file = "generated_demo_data.json"
    with open(output_file, "w") as f:
        json.dump(demo_data, f, indent=2)

    print(f"✅ Demo data generated successfully!")
    print(f"📁 Saved to: {output_file}")
    print(f"\nGenerated:")
    print(f"  - {len(commit_activity)} days of commit activity")
    print(f"  - {len(pull_requests)} pull requests")
    print(f"  - {len(sprints)} sprints")
    print(f"  - {len(sprint_velocity)} sprint velocity records")
    print(f"  - PR metrics calculated")

    # Print summary statistics
    total_commits = sum(day["count"] for day in commit_activity)
    unique_authors = set()
    for day in commit_activity:
        unique_authors.update(day["authors"])

    print(f"\nSummary:")
    print(f"  - Total commits: {total_commits}")
    print(f"  - Unique contributors: {len(unique_authors)}")
    print(f"  - Avg time to merge: {pr_metrics['average_time_to_merge']}h")
    print(f"  - Approval rate: {pr_metrics['approval_rate']}%")


if __name__ == "__main__":
    main()


