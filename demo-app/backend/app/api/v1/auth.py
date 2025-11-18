"""
Authentication API endpoints for OAuth and JWT token management.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from app.auth.oauth import (
    get_oauth_provider,
    create_jwt_token,
    verify_jwt_token,
)
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


# Request/Response Models
class AuthURLResponse(BaseModel):
    """Response model for OAuth authorization URL."""
    authorization_url: str
    state: str


class OAuthCallbackRequest(BaseModel):
    """Request model for OAuth callback."""
    code: str
    state: str
    provider: str


class TokenResponse(BaseModel):
    """Response model for JWT token."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400  # 24 hours in seconds
    user: Dict[str, Any]


class UserResponse(BaseModel):
    """Response model for user information."""
    user_id: str
    username: str
    email: Optional[str]
    name: Optional[str]
    avatar_url: Optional[str]
    provider: str
    team_id: Optional[str] = None


# Dependency for getting current user from JWT
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to extract and verify current user from JWT token.
    
    Args:
        credentials: HTTP Authorization header with Bearer token
        
    Returns:
        User data from verified token
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    user_data = verify_jwt_token(token)
    return user_data


@router.get("/auth/{provider}/authorize", response_model=AuthURLResponse)
async def get_authorization_url(
    provider: str,
    redirect_uri: str,
) -> AuthURLResponse:
    """
    Get OAuth authorization URL for the specified provider.
    
    Args:
        provider: OAuth provider ('github' or 'gitlab')
        redirect_uri: Redirect URI after authorization
        
    Returns:
        Authorization URL and state parameter
    """
    try:
        oauth_provider = get_oauth_provider(provider, redirect_uri)
        state = oauth_provider.generate_state()
        auth_url = oauth_provider.get_authorization_url(state)
        
        logger.info(f"Generated {provider} authorization URL")
        
        return AuthURLResponse(
            authorization_url=auth_url,
            state=state
        )
    
    except Exception as e:
        logger.error(f"Error generating authorization URL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/auth/callback", response_model=TokenResponse)
async def oauth_callback(
    callback_data: OAuthCallbackRequest,
) -> TokenResponse:
    """
    Handle OAuth callback and exchange code for JWT token.
    
    Args:
        callback_data: OAuth callback data with code and state
        
    Returns:
        JWT access token and user information
    """
    try:
        # Get OAuth provider
        oauth_provider = get_oauth_provider(
            callback_data.provider,
            ""  # redirect_uri not needed for token exchange
        )
        
        # Exchange code for access token
        token_data = await oauth_provider.exchange_code_for_token(callback_data.code)
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token received"
            )
        
        # Get user info from provider
        user_info = await oauth_provider.get_user_info(access_token)
        
        # Store or update user in database
        user_service = UserService()
        user = await user_service.create_or_update_user(
            user_id=user_info["user_id"],
            username=user_info["username"],
            email=user_info.get("email"),
            name=user_info.get("name"),
            avatar_url=user_info.get("avatar_url"),
            provider=user_info["provider"],
            oauth_token=access_token,
        )
        
        # Create JWT token
        jwt_token = create_jwt_token(user_info)
        
        logger.info(f"User {user_info['username']} authenticated via {callback_data.provider}")
        
        return TokenResponse(
            access_token=jwt_token,
            user=user_info
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in OAuth callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user information.

    Args:
        current_user: Current user from JWT token (injected by dependency)

    Returns:
        User information
    """
    user_service = UserService()
    user = await user_service.get_user(current_user["user_id"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(**user)


@router.post("/auth/logout")
async def logout(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Logout current user (client-side token removal).

    Note: Since we're using stateless JWT, actual logout happens client-side
    by removing the token. This endpoint is mainly for logging purposes.

    Args:
        current_user: Current user from JWT token

    Returns:
        Success message
    """
    logger.info(f"User {current_user.get('username')} logged out")

    return {"message": "Successfully logged out"}


@router.post("/auth/refresh")
async def refresh_token(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> TokenResponse:
    """
    Refresh JWT token for current user.

    Args:
        current_user: Current user from JWT token

    Returns:
        New JWT access token
    """
    # Create new JWT token with same user data
    new_token = create_jwt_token(current_user)

    logger.info(f"Token refreshed for user {current_user.get('username')}")

    return TokenResponse(
        access_token=new_token,
        user=current_user
    )

