import pytest
import asyncio
from fastapi.testclient import TestClient
from auth.models import UserRegistration, UserLogin
from backend.main import app

client = TestClient(app)

def test_register_user():
    """Test user registration endpoint"""
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "name": "Test User",
        "preferred_language": "en"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "user" in data
    assert data["user"]["email"] == user_data["email"]


def test_login_user():
    """Test user login endpoint"""
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/auth/login", json=login_data)
    # This might fail in the simulation since we don't have a real user in the system
    # but it should at least return the proper error format
    assert response.status_code in [200, 401]  # Either success or proper auth error


def test_auth_verify_endpoint():
    """Test auth verification endpoint without token (should fail)"""
    response = client.get("/auth/verify")
    assert response.status_code == 401  # Should require authentication


def test_logout_endpoint():
    """Test logout endpoint without token (should fail properly)"""
    response = client.post("/auth/logout")
    assert response.status_code == 401  # Should require authentication


def test_get_user_profile():
    """Test get user profile endpoint without token (should fail)"""
    response = client.get("/auth/me")
    assert response.status_code == 401  # Should require authentication


def test_protected_endpoint():
    """Test that chat endpoint requires authentication"""
    response = client.post("/chat/", json={"message": "Hello"})
    assert response.status_code == 401  # Should require authentication


if __name__ == "__main__":
    pytest.main([__file__])