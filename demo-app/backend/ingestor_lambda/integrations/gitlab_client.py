"""
GitLab API client for fetching repository data, commits, and merge requests.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from ratelimit import limits, sleep_and_retry

logger = logging.getLogger(__name__)

# GitLab API Configuration
GITLAB_API_BASE = "https://gitlab.com/api/v4"

# Rate limiting: GitLab allows 2000 requests per minute for authenticated users
RATE_LIMIT_CALLS = 2000
RATE_LIMIT_PERIOD = 60  # 1 minute in seconds


class GitLabClient:
    """Client for interacting with GitLab API."""
    
    def __init__(self, access_token: str):
        """
        Initialize GitLab client.
        
        Args:
            access_token: GitLab OAuth access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
        }
    
    @sleep_and_retry
    @limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make an HTTP request to GitLab API with rate limiting.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
        """
        url = f"{GITLAB_API_BASE}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                timeout=30.0,
            )
            
            response.raise_for_status()
            return response.json()
    
    async def get_user_projects(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get projects for a user or authenticated user.
        
        Args:
            username: GitLab username (None for authenticated user)
            
        Returns:
            List of project data
        """
        if username:
            # First get user ID
            user_data = await self._make_request("GET", f"/users?username={username}")
            if not user_data:
                return []
            user_id = user_data[0]["id"]
            endpoint = f"/users/{user_id}/projects"
        else:
            endpoint = "/projects"
        
        params = {
            "per_page": 100,
            "order_by": "updated_at",
            "sort": "desc",
            "membership": True,
        }
        
        projects = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(projects)} projects")
        
        return projects
    
    async def get_commits(
        self,
        project_id: int,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        author: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get commits for a project.
        
        Args:
            project_id: GitLab project ID
            since: Only commits after this date
            until: Only commits before this date
            author: Filter by commit author
            
        Returns:
            List of commit data
        """
        endpoint = f"/projects/{project_id}/repository/commits"
        
        params = {"per_page": 100}
        
        if since:
            params["since"] = since.isoformat()
        if until:
            params["until"] = until.isoformat()
        if author:
            params["author"] = author
        
        commits = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(commits)} commits for project {project_id}")
        
        return commits
    
    async def get_merge_requests(
        self,
        project_id: int,
        state: str = "all",
        updated_after: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get merge requests for a project.
        
        Args:
            project_id: GitLab project ID
            state: MR state ('opened', 'closed', 'merged', 'all')
            updated_after: Only MRs updated after this date
            
        Returns:
            List of merge request data
        """
        endpoint = f"/projects/{project_id}/merge_requests"
        
        params = {
            "state": state,
            "per_page": 100,
            "order_by": "updated_at",
            "sort": "desc",
        }
        
        if updated_after:
            params["updated_after"] = updated_after.isoformat()
        
        mrs = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(mrs)} merge requests for project {project_id}")

        return mrs

    async def get_mr_approvals(
        self,
        project_id: int,
        mr_iid: int,
    ) -> Dict[str, Any]:
        """
        Get approval information for a merge request.

        Args:
            project_id: GitLab project ID
            mr_iid: Merge request IID (internal ID)

        Returns:
            Approval data
        """
        endpoint = f"/projects/{project_id}/merge_requests/{mr_iid}/approvals"

        approvals = await self._make_request("GET", endpoint)
        logger.info(f"Fetched approvals for MR !{mr_iid}")

        return approvals

    async def get_mr_notes(
        self,
        project_id: int,
        mr_iid: int,
    ) -> List[Dict[str, Any]]:
        """
        Get notes (comments) for a merge request.

        Args:
            project_id: GitLab project ID
            mr_iid: Merge request IID

        Returns:
            List of note data
        """
        endpoint = f"/projects/{project_id}/merge_requests/{mr_iid}/notes"

        params = {"per_page": 100}

        notes = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(notes)} notes for MR !{mr_iid}")

        return notes

    async def get_project_stats(
        self,
        project_id: int,
    ) -> Dict[str, Any]:
        """
        Get project statistics.

        Args:
            project_id: GitLab project ID

        Returns:
            Project statistics
        """
        endpoint = f"/projects/{project_id}"

        params = {"statistics": True}

        project_data = await self._make_request("GET", endpoint, params)

        stats = {
            "name": project_data["name"],
            "path_with_namespace": project_data["path_with_namespace"],
            "description": project_data.get("description"),
            "stars": project_data["star_count"],
            "forks": project_data["forks_count"],
            "open_issues": project_data.get("open_issues_count", 0),
            "created_at": project_data["created_at"],
            "last_activity_at": project_data["last_activity_at"],
        }

        if "statistics" in project_data:
            stats.update({
                "repository_size": project_data["statistics"]["repository_size"],
                "commit_count": project_data["statistics"]["commit_count"],
            })

        logger.info(f"Fetched stats for project {project_id}")

        return stats

    async def get_project_contributors(
        self,
        project_id: int,
    ) -> List[Dict[str, Any]]:
        """
        Get contributors for a project.

        Args:
            project_id: GitLab project ID

        Returns:
            List of contributor data
        """
        endpoint = f"/projects/{project_id}/repository/contributors"

        params = {"per_page": 100, "order_by": "commits", "sort": "desc"}

        contributors = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(contributors)} contributors for project {project_id}")

        return contributors

