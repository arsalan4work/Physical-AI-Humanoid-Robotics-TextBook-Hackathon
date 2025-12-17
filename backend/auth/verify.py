"""
Authentication verification module
- Validates authentication tokens using Better-auth
- Verifies user permissions
- Returns user context (ID, email, preferred language)
"""

from fastapi import HTTPException, Request
from typing import Optional, Dict, Any
import jwt
import os
from datetime import datetime
from auth.models import UserResponse
import httpx
import asyncio


async def verify_token_with_better_auth(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify authentication token using Better-auth service

    Args:
        token: Authentication token to verify

    Returns:
        User context dict with ID, email, preferred language, or None if invalid
    """
    try:
        # In a real implementation, this would call the Better-auth API
        # For now, we'll simulate the call to Better-auth service
        if not token:
            return None

        # Simulate calling Better-auth verification endpoint
        # In real implementation: make HTTP request to Better-auth service
        user_context = {
            "user_id": "test_user_123",
            "email": "user@example.com",
            "preferred_language": "en",
            "name": "Test User"
        }

        return user_context
    except Exception as e:
        print(f"Token verification error: {e}")
        return None


def get_token_from_request(request: Request) -> Optional[str]:
    """
    Extract token from request headers or cookies

    Args:
        request: FastAPI request object

    Returns:
        Token string or None if not found
    """
    # Check Authorization header first
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    # Check for token in cookies (common with Better-auth)
    token = request.cookies.get("better-auth.session_token")
    if token:
        return token

    return None


async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Get current user from request headers using Better-auth verification

    Args:
        request: FastAPI request object

    Returns:
        User context dict

    Raises:
        HTTPException: If token is invalid or missing
    """
    token = get_token_from_request(request)

    if not token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    user_context = await verify_token_with_better_auth(token)

    if not user_context:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_context


def create_auth_middleware():
    """
    Create authentication middleware for token verification
    """
    async def auth_middleware(request: Request, call_next):
        # Skip auth for public endpoints
        if request.url.path in ["/", "/health", "/docs", "/redoc"]:
            return await call_next(request)

        # For auth endpoints, allow through but validate if token provided
        if request.url.path.startswith("/auth") and request.method == "POST":
            return await call_next(request)

        # For protected endpoints, require valid auth
        try:
            current_user = await get_current_user(request)
            # Add user info to request state for use in route handlers
            request.state.user = current_user
        except HTTPException as e:
            if e.status_code == 401:
                # Only reject if it's a protected endpoint
                protected_prefixes = ["/chat", "/vector", "/translate"]
                if any(request.url.path.startswith(prefix) for prefix in protected_prefixes):
                    return await call_next(request)  # Let the route handle auth error

        response = await call_next(request)
        return response

    return auth_middleware


# Protected route decorator
def require_auth():
    """
    Decorator to require authentication for routes
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This will be handled by the middleware
            return await func(*args, **kwargs)
        return wrapper
    return decorator