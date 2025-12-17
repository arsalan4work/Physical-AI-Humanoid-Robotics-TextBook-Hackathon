"""
Qdrant database operations for the AI Multilingual Chatbot System
Handles vector storage, retrieval, and management for conversation memory
"""
import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import cohere
from pydantic import BaseModel
from datetime import datetime
import logging
import uuid

# Configure logging
logger = logging.getLogger(__name__)

class VectorRecord(BaseModel):
    """
    Model for vector records in the chatbot memory collection
    """
    user_id: str
    message: str
    timestamp: int
    metadata: Dict[str, Any]


class QdrantService:
    """
    Service class to handle Qdrant database operations
    """

    def __init__(self):
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", 6333))

        if qdrant_url and qdrant_api_key:
            # Use cloud instance
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                timeout=10
            )
        else:
            # Use local instance
            self.client = QdrantClient(
                host=qdrant_host,
                port=qdrant_port,
                timeout=10
            )

        # Initialize Cohere client for embeddings
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        self.cohere_client = cohere.Client(cohere_api_key)

        # Collection name
        self.collection_name = "chatbot_memory"

        # Vector size for Cohere embed-english-v3.0
        # This model returns 1024-dimensional vectors
        self.vector_size = 1024

    def init_collection(self):
        """
        Initialize the chatbot_memory collection with proper schema
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections().collections
            collection_names = [coll.name for coll in collections]

            if self.collection_name not in collection_names:
                # Create collection with vector configuration
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )

                # Create payload index for user_id to improve search performance
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="user_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                # Create payload index for timestamp
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="timestamp",
                    field_schema=models.PayloadSchemaType.INTEGER
                )

                logger.info(f"Created collection '{self.collection_name}' with proper schema")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")

        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector from Cohere Embed v3

        Args:
            text: Text to embed

        Returns:
            Embedding vector as a list of floats
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")

            response = self.cohere_client.embed(
                model="embed-english-v3.0",
                input_type="search_query",  # Use search_query for queries
                texts=[text],
            )
            return response.embeddings[0]  # Return the first embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def upsert_vector(self, user_id: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store a message in the vector database with embedding

        Args:
            user_id: ID of the user
            message: The message text to store
            metadata: Additional metadata (topic, lang, agent, etc.)

        Returns:
            ID of the stored vector
        """
        try:
            if not user_id or not message:
                raise ValueError("user_id and message are required")

            # Generate embedding for the message
            embedding = self.get_embedding(message)

            # Create timestamp
            timestamp = int(datetime.utcnow().timestamp())

            # Prepare payload
            payload = {
                "user_id": user_id,
                "message": message,
                "timestamp": timestamp,
                "metadata": metadata or {}
            }

            # Generate a unique ID for this record
            vector_id = str(uuid.uuid4())

            # Upsert the record
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=vector_id,
                        vector=embedding,
                        payload=payload
                    )
                ]
            )

            logger.info(f"Upserted vector with ID: {vector_id}")
            return vector_id

        except Exception as e:
            logger.error(f"Error upserting vector: {e}")
            raise

    def search_vectors(self, query: str, user_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the database

        Args:
            query: Query text to search for
            user_id: Optional user ID to filter results
            limit: Maximum number of results to return

        Returns:
            List of matching records with scores
        """
        try:
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")

            # Validate limit
            if limit <= 0 or limit > 100:
                limit = min(limit, 100)  # Cap at 100 to prevent abuse

            # Generate embedding for the query
            query_embedding = self.get_embedding(query)

            # Prepare search filter if user_id is provided
            search_filter = None
            if user_id:
                search_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=user_id)
                        )
                    ]
                )

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=search_filter,
                limit=limit
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "message": result.payload.get("message", ""),
                    "user_id": result.payload.get("user_id", ""),
                    "timestamp": result.payload.get("timestamp", 0),
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score
                })

            logger.info(f"Found {len(formatted_results)} results for query")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise

    def delete_vectors_by_user(self, user_id: str):
        """
        Delete all vectors associated with a specific user

        Args:
            user_id: ID of the user whose vectors to delete
        """
        try:
            if not user_id:
                raise ValueError("user_id is required")

            # Create filter to find points with specific user_id
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id)
                    )
                ]
            )

            # Get all points matching the filter
            points = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=search_filter,
                limit=10000  # Adjust as needed
            )[0]

            if points:
                point_ids = [point.id for point in points]

                # Delete the points
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=point_ids
                    )
                )

                logger.info(f"Deleted {len(point_ids)} vectors for user {user_id}")
            else:
                logger.info(f"No vectors found for user {user_id}")

        except Exception as e:
            logger.error(f"Error deleting vectors for user {user_id}: {e}")
            raise


# Global instance
qdrant_service = QdrantService()


def get_qdrant_service() -> QdrantService:
    """
    Get the global Qdrant service instance
    """
    return qdrant_service