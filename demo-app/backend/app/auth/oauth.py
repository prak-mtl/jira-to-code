"""
OAuth 2.0 authentication handlers for GitHub and GitLab.
Implements authorization code flow for both platforms.
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import httpx
import jwt
from fastapi import HTTPException, status

# OAuth Configuration
GITHUB_OAUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"

GITLAB_OAUTH_URL = "https://gitlab.com/oauth/authorize"
GITLAB_TOKEN_URL = "https://gitlab.com/oauth/token"
GITLAB_USER_API = "https://gitlab.com/api/v4/user"

JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


class OAuthProvider:
    """Base class for OAuth providers."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
    def generate_state(self) -> str:
        """Generate a random state parameter for CSRF protection."""
        return secrets.token_urlsafe(32)
    
    def get_authorization_url(self, state: str) -> str:
        """Get the OAuth authorization URL."""
        raise NotImplementedError
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        raise NotImplementedError
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information using the access token."""
        raise NotImplementedError


class GitHubOAuth(OAuthProvider):
    """GitHub OAuth 2.0 implementation."""
    
    def get_authorization_url(self, state: str) -> str:
        """Generate GitHub OAuth authorization URL."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "read:user user:email repo",
            "state": state,
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{GITHUB_OAUTH_URL}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange GitHub authorization code for access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GITHUB_TOKEN_URL,
                headers={"Accept": "application/json"},
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                },
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange code for token"
                )
            
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get GitHub user information."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GITHUB_USER_API,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to fetch user info"
                )
            
            user_data = response.json()
            
            # Normalize user data
            return {
                "user_id": str(user_data["id"]),
                "username": user_data["login"],
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("avatar_url"),
                "provider": "github",
            }


class GitLabOAuth(OAuthProvider):
    """GitLab OAuth 2.0 implementation."""
    
    def get_authorization_url(self, state: str) -> str:
        """Generate GitLab OAuth authorization URL."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "read_user read_api",
            "state": state,
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{GITLAB_OAUTH_URL}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange GitLab authorization code for access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GITLAB_TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri,
                },
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange code for token"
                )

            return response.json()

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get GitLab user information."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GITLAB_USER_API,
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to fetch user info"
                )

            user_data = response.json()

            # Normalize user data
            return {
                "user_id": str(user_data["id"]),
                "username": user_data["username"],
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("avatar_url"),
                "provider": "gitlab",
            }


def create_jwt_token(user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token for authenticated user.

    Args:
        user_data: User information to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = user_data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access_token",
    })

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if payload.get("type") != "access_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_oauth_provider(provider: str, redirect_uri: str) -> OAuthProvider:
    """
    Factory function to get the appropriate OAuth provider.

    Args:
        provider: Provider name ('github' or 'gitlab')
        redirect_uri: OAuth redirect URI

    Returns:
        OAuthProvider instance

    Raises:
        HTTPException: If provider is not supported
    """
    if provider == "github":
        client_id = os.environ.get("GITHUB_CLIENT_ID")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitHub OAuth not configured"
            )

        return GitHubOAuth(client_id, client_secret, redirect_uri)

    elif provider == "gitlab":
        client_id = os.environ.get("GITLAB_CLIENT_ID")
        client_secret = os.environ.get("GITLAB_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitLab OAuth not configured"
            )

        return GitLabOAuth(client_id, client_secret, redirect_uri)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}"
        )

