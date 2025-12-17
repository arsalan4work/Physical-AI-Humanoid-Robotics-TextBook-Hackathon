import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()
    assert response.json()["service"] == "AI Multilingual Chatbot API"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "AI Multilingual Chatbot API"
    assert "endpoints" in response.json()

def test_cors_middleware():
    """Test that CORS headers are properly set"""
    response = client.get("/health")
    # Check if CORS headers are present in response
    assert "access-control-allow-origin" in [header.lower() for header in response.headers.keys()]

if __name__ == "__main__":
    pytest.main([__file__])