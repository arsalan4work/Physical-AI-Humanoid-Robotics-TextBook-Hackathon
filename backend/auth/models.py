"""
User model with preferred language field for the authentication system
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """
    User model that includes preferred language field
    """
    id: str
    email: EmailStr
    name: Optional[str] = None
    preferred_language: str = "en"  # Default to English
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class UserRegistration(BaseModel):
    """
    Model for user registration
    """
    email: EmailStr
    password: str
    name: Optional[str] = None
    preferred_language: str = "en"


class UserLogin(BaseModel):
    """
    Model for user login
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Model for user response (excluding sensitive data)
    """
    id: str
    email: EmailStr
    name: Optional[str]
    preferred_language: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True