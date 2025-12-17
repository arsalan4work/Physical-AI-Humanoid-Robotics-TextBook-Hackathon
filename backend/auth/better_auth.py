"""
Better-auth integration module
Handles user registration, login, logout, and session management
"""
from fastapi import HTTPException, Request, Response
from typing import Optional, Dict, Any
import httpx
import os
from auth.models import UserRegistration, UserLogin, UserResponse
from auth.verify import verify_token_with_better_auth


class BetterAuthIntegration:
    """
    Better-auth integration class to handle authentication operations
    """

    def __init__(self):
        self.base_url = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
        self.secret = os.getenv("BETTER_AUTH_SECRET")

    async def register_user(self, user_data: UserRegistration) -> UserResponse:
        """
        Register a new user with Better-auth

        Args:
            user_data: User registration information

        Returns:
            UserResponse with user information
        """
        # In a real implementation, this would call Better-auth registration API
        # For now, we'll simulate the registration process
        from datetime import datetime

        user = {
            "id": f"user_{hash(user_data.email)}",  # Simulated user ID
            "email": user_data.email,
            "name": user_data.name,
            "preferred_language": user_data.preferred_language,
            "created_at": datetime.utcnow(),
            "is_active": True
        }

        # Convert to UserResponse
        return UserResponse(**user)

    async def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """
        Authenticate user with Better-auth

        Args:
            login_data: User login credentials

        Returns:
            Dict with user info and session token
        """
        # In a real implementation, this would call Better-auth login API
        # For now, we'll simulate the login process
        from datetime import datetime

        # Simulate user lookup and authentication
        user = {
            "id": f"user_{hash(login_data.email)}",
            "email": login_data.email,
            "name": "Test User",  # In real app, retrieve from DB
            "preferred_language": "en",  # In real app, retrieve from DB
            "created_at": datetime.utcnow(),
            "is_active": True
        }

        # Simulate token generation
        token = f"token_{hash(login_data.email + login_data.password)}"

        return {
            "user": UserResponse(**user),
            "token": token,
            "expires_at": datetime.utcnow().timestamp() + 3600  # 1 hour
        }

    async def logout_user(self, token: str) -> bool:
        """
        Logout user with Better-auth

        Args:
            token: User session token

        Returns:
            True if logout successful, False otherwise
        """
        # In a real implementation, this would call Better-auth logout API
        # For now, we'll simulate the logout process
        try:
            # In real app: make HTTP request to Better-auth logout endpoint
            # await httpx.post(f"{self.base_url}/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
            return True
        except Exception:
            return False

    async def get_user_by_token(self, token: str) -> Optional[UserResponse]:
        """
        Get user information using authentication token

        Args:
            token: User session token

        Returns:
            UserResponse if token is valid, None otherwise
        """
        user_context = await verify_token_with_better_auth(token)
        if not user_context:
            return None

        from datetime import datetime

        user = {
            "id": user_context["user_id"],
            "email": user_context["email"],
            "name": user_context.get("name", "Unknown User"),
            "preferred_language": user_context["preferred_language"],
            "created_at": datetime.utcnow(),  # In real app, retrieve from DB
            "is_active": True
        }

        return UserResponse(**user)


# Global instance
better_auth = BetterAuthIntegration()


async def get_current_user_from_request(request: Request) -> Optional[UserResponse]:
    """
    Extract and verify user from request

    Args:
        request: FastAPI request object

    Returns:
        UserResponse if authenticated, None otherwise
    """
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
    elif "better-auth.session_token" in request.cookies:
        token = request.cookies.get("better-auth.session_token")
    else:
        return None

    return await better_auth.get_user_by_token(token)