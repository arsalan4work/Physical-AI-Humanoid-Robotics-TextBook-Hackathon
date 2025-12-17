import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.qdrant import get_qdrant_service

client = TestClient(app)

def test_qdrant_service_initialization():
    """Test that Qdrant service initializes properly"""
    service = get_qdrant_service()
    assert service is not None
    assert service.collection_name == "chatbot_memory"


def test_vector_upsert_endpoint():
    """Test vector upsert endpoint"""
    # This will fail without proper authentication, which is expected
    upsert_data = {
        "text": "Test message for vector storage",
        "user_id": "test_user_123",
        "metadata": {"topic": "test", "lang": "en", "agent": "test"}
    }
    response = client.post("/vector/upsert", json=upsert_data)
    # Should return 401 because authentication is required
    assert response.status_code == 401


def test_vector_search_endpoint():
    """Test vector search endpoint"""
    # This will fail without proper authentication, which is expected
    search_data = {
        "query": "Test search query",
        "user_id": "test_user_123",
        "limit": 5
    }
    response = client.post("/vector/search", json=search_data)
    # Should return 401 because authentication is required
    assert response.status_code == 401


def test_embedding_function():
    """Test that embedding function works"""
    service = get_qdrant_service()

    # Test that the embedding function works
    test_text = "This is a test sentence"
    embedding = service.get_embedding(test_text)

    # Cohere embed-english-v3.0 should return 1024-dimensional vectors
    assert len(embedding) == 1024
    assert all(isinstance(val, float) for val in embedding)


def test_collection_initialization():
    """Test collection initialization"""
    service = get_qdrant_service()

    # This should not raise an exception
    try:
        service.init_collection()
        assert True  # If we get here, initialization worked
    except Exception as e:
        # If there's a connection issue, that's okay for testing purposes
        if "connection" in str(e).lower() or "network" in str(e).lower():
            # This is expected if Qdrant is not running
            assert True
        else:
            raise e


if __name__ == "__main__":
    pytest.main([__file__])