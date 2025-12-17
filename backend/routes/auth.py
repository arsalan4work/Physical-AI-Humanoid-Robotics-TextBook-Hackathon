"""
Authentication-related endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Dict, Any

from auth.verify import get_current_user
from auth.better_auth import better_auth, get_current_user_from_request
from auth.models import UserRegistration, UserLogin

router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserRegistration):
    """
    Register a new user
    """
    try:
        user = await better_auth.register_user(user_data)
        return {
            "success": True,
            "user": user
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login_user(login_data: UserLogin):
    """
    Authenticate user and return session token
    """
    try:
        result = await better_auth.login_user(login_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")


@router.post("/logout")
async def logout_user(request: Request):
    """
    Logout current user
    """
    try:
        # Get token from request
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]
        elif "better-auth.session_token" in request.cookies:
            token = request.cookies.get("better-auth.session_token")
        else:
            raise HTTPException(status_code=401, detail="No authentication token provided")

        success = await better_auth.logout_user(token)
        if success:
            response = Response(status_code=200)
            # Clear the session cookie if it exists
            response.delete_cookie("better-auth.session_token")
            return {"success": True}
        else:
            raise HTTPException(status_code=400, detail="Logout failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Logout failed: {str(e)}")


@router.get("/verify")
async def verify_auth(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Verify authentication token and return user information
    """
    return {
        "authenticated": True,
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "name": current_user.get("name", "Unknown User"),
        "preferred_language": current_user["preferred_language"]
    }


@router.get("/me")
async def get_user_profile(request: Request):
    """
    Get current user profile information
    """
    user = await get_current_user_from_request(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user