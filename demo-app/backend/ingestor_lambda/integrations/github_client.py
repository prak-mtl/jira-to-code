"""
GitHub API client for fetching repository data, commits, and pull requests.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import httpx
from ratelimit import limits, sleep_and_retry

logger = logging.getLogger(__name__)

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"

# Rate limiting: GitHub allows 5000 requests per hour for authenticated users
RATE_LIMIT_CALLS = 5000
RATE_LIMIT_PERIOD = 3600  # 1 hour in seconds


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, access_token: str):
        """
        Initialize GitHub client.
        
        Args:
            access_token: GitHub OAuth access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        }
    
    @sleep_and_retry
    @limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to GitHub API with rate limiting.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
        """
        url = f"{GITHUB_API_BASE}{endpoint}"
        
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
    
    async def get_user_repos(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get repositories for a user or authenticated user.
        
        Args:
            username: GitHub username (None for authenticated user)
            
        Returns:
            List of repository data
        """
        if username:
            endpoint = f"/users/{username}/repos"
        else:
            endpoint = "/user/repos"
        
        params = {
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        }
        
        repos = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(repos)} repositories")
        
        return repos
    
    async def get_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        author: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get commits for a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            since: Only commits after this date
            until: Only commits before this date
            author: Filter by commit author
            
        Returns:
            List of commit data
        """
        endpoint = f"/repos/{owner}/{repo}/commits"
        
        params = {"per_page": 100}
        
        if since:
            params["since"] = since.isoformat()
        if until:
            params["until"] = until.isoformat()
        if author:
            params["author"] = author
        
        commits = await self._make_request("GET", endpoint, params)
        logger.info(f"Fetched {len(commits)} commits for {owner}/{repo}")
        
        return commits
    
    async def get_pull_requests(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get pull requests for a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state ('open', 'closed', 'all')
            since: Only PRs updated after this date
            
        Returns:
            List of pull request data
        """
        endpoint = f"/repos/{owner}/{repo}/pulls"
        
        params = {
            "state": state,
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        }
        
        prs = await self._make_request("GET", endpoint, params)
        
        # Filter by date if specified
        if since:
            prs = [
                pr for pr in prs
                if datetime.fromisoformat(pr["updated_at"].replace("Z", "+00:00")) >= since
            ]
        
        logger.info(f"Fetched {len(prs)} pull requests for {owner}/{repo}")

        return prs

    async def get_pr_reviews(
        self,
        owner: str,
        repo: str,
        pr_number: int,
    ) -> List[Dict[str, Any]]:
        """
        Get reviews for a specific pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number

        Returns:
            List of review data
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews"

        reviews = await self._make_request("GET", endpoint)
        logger.info(f"Fetched {len(reviews)} reviews for PR #{pr_number}")

        return reviews

    async def get_pr_comments(
        self,
        owner: str,
        repo: str,
        pr_number: int,
    ) -> List[Dict[str, Any]]:
        """
        Get comments for a specific pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number

        Returns:
            List of comment data
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pr_number}/comments"

        comments = await self._make_request("GET", endpoint)
        logger.info(f"Fetched {len(comments)} comments for PR #{pr_number}")

        return comments

    async def get_repo_stats(
        self,
        owner: str,
        repo: str,
    ) -> Dict[str, Any]:
        """
        Get repository statistics.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Repository statistics
        """
        endpoint = f"/repos/{owner}/{repo}"

        repo_data = await self._make_request("GET", endpoint)

        stats = {
            "name": repo_data["name"],
            "full_name": repo_data["full_name"],
            "description": repo_data.get("description"),
            "stars": repo_data["stargazers_count"],
            "forks": repo_data["forks_count"],
            "open_issues": repo_data["open_issues_count"],
            "language": repo_data.get("language"),
            "created_at": repo_data["created_at"],
            "updated_at": repo_data["updated_at"],
            "size": repo_data["size"],
        }

        logger.info(f"Fetched stats for {owner}/{repo}")

        return stats

    async def get_contributor_stats(
        self,
        owner: str,
        repo: str,
    ) -> List[Dict[str, Any]]:
        """
        Get contributor statistics for a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            List of contributor statistics
        """
        endpoint = f"/repos/{owner}/{repo}/stats/contributors"

        contributors = await self._make_request("GET", endpoint)
        logger.info(f"Fetched {len(contributors)} contributors for {owner}/{repo}")

        return contributors

