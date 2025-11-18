"""
User service for managing user data in DynamoDB.
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class UserService:
    """Service for user data operations."""
    
    def __init__(self):
        self.table_name = os.environ.get("USERS_TABLE_NAME", "DeveloperProductivityUsers")
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)
    
    async def create_or_update_user(
        self,
        user_id: str,
        username: str,
        email: Optional[str],
        name: Optional[str],
        avatar_url: Optional[str],
        provider: str,
        oauth_token: str,
        team_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create or update user in DynamoDB.
        
        Args:
            user_id: Unique user identifier from OAuth provider
            username: Username
            email: User email
            name: User full name
            avatar_url: Avatar image URL
            provider: OAuth provider ('github' or 'gitlab')
            oauth_token: OAuth access token (encrypted in production)
            team_id: Optional team identifier
            
        Returns:
            User data dictionary
        """
        try:
            user_data = {
                "user_id": f"{provider}:{user_id}",
                "username": username,
                "email": email,
                "name": name,
                "avatar_url": avatar_url,
                "provider": provider,
                "oauth_token": oauth_token,  # TODO: Encrypt in production
                "team_id": team_id,
                "updated_at": datetime.utcnow().isoformat(),
            }
            
            # Check if user exists
            existing_user = await self.get_user(user_data["user_id"])
            
            if existing_user:
                user_data["created_at"] = existing_user.get("created_at")
            else:
                user_data["created_at"] = datetime.utcnow().isoformat()
            
            # Save to DynamoDB
            self.table.put_item(Item=user_data)
            
            logger.info(f"User {username} created/updated successfully")
            
            return user_data
        
        except ClientError as e:
            logger.error(f"Error creating/updating user: {e}")
            raise
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID from DynamoDB.
        
        Args:
            user_id: User identifier
            
        Returns:
            User data dictionary or None if not found
        """
        try:
            response = self.table.get_item(Key={"user_id": user_id})
            return response.get("Item")
        
        except ClientError as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email using GSI.
        
        Args:
            email: User email
            
        Returns:
            User data dictionary or None if not found
        """
        try:
            response = self.table.query(
                IndexName="EmailIndex",
                KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
            )
            
            items = response.get("Items", [])
            return items[0] if items else None
        
        except ClientError as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_team_users(self, team_id: str) -> list[Dict[str, Any]]:
        """
        Get all users in a team.
        
        Args:
            team_id: Team identifier
            
        Returns:
            List of user data dictionaries
        """
        try:
            response = self.table.query(
                IndexName="TeamIdIndex",
                KeyConditionExpression=boto3.dynamodb.conditions.Key("team_id").eq(team_id)
            )
            
            return response.get("Items", [])
        
        except ClientError as e:
            logger.error(f"Error getting team users: {e}")
            return []
    
    async def update_team(self, user_id: str, team_id: str) -> bool:
        """
        Update user's team assignment.
        
        Args:
            user_id: User identifier
            team_id: Team identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="SET team_id = :team_id, updated_at = :updated_at",
                ExpressionAttributeValues={
                    ":team_id": team_id,
                    ":updated_at": datetime.utcnow().isoformat(),
                }
            )
            
            logger.info(f"User {user_id} assigned to team {team_id}")
            return True
        
        except ClientError as e:
            logger.error(f"Error updating user team: {e}")
            return False

