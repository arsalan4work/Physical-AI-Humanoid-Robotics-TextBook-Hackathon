"""
Knowledge agent for handling search and knowledge retrieval tasks
Uses Qdrant vector database for memory and knowledge storage
"""
import os
import logging
from typing import Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeAgent:
    """
    KnowledgeAgent for handling knowledge search and retrieval tasks
    Uses Qdrant vector database for memory and knowledge storage
    """

    def __init__(self, collection_name: str = "chatbot_memory"):
        self.collection_name = collection_name

        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_api_key:
            self.qdrant_client = QdrantClient(
                url=qdrant_url,
                port=qdrant_port,
                api_key=qdrant_api_key,
                prefer_grpc=True
            )
        else:
            self.qdrant_client = QdrantClient(
                host=qdrant_url,
                port=qdrant_port
            )

        # Initialize Cohere client for embeddings
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.cohere_client = cohere.Client(cohere_api_key)

        # Ensure collection exists
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the knowledge base collection exists in Qdrant"""
        try:
            # Get collection info to check if it exists
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception:
            # Create collection if it doesn't exist
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
                optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000, indexing_threshold=20000)
            )
            logger.info(f"Created collection '{self.collection_name}'")

    async def search(self, query: str, user_id: str, top_k: int = 5) -> str:
        """
        Search the knowledge base for relevant information

        Args:
            query: The search query
            user_id: ID of the requesting user
            top_k: Number of top results to return

        Returns:
            Formatted search results
        """
        try:
            logger.info(f"Searching knowledge base for: {query}")

            # Generate embedding for the query using Cohere
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            query_embedding = response.embeddings[0]

            # Search in Qdrant with user-specific filter
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=user_id)
                        )
                    ]
                ),
                limit=top_k,
                with_payload=True
            )

            # Format results
            if search_results:
                results = []
                for hit in search_results:
                    content = hit.payload.get("message", "")
                    timestamp = hit.payload.get("timestamp", "unknown")
                    results.append(f"- {content} (from {timestamp})")

                result_str = f"Found {len(results)} relevant results for your query '{query}':\n"
                result_str += "\n".join(results)
                return result_str
            else:
                return f"No relevant information found for your query '{query}'. I can help you with other questions."

        except Exception as e:
            logger.error(f"Error in knowledge search: {str(e)}")
            return f"I encountered an error while searching for information: {str(e)}"

    async def store_memory(self, user_id: str, message: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Store a message in the knowledge base for future retrieval

        Args:
            user_id: ID of the user
            message: Message to store
            metadata: Additional metadata to store with the message

        Returns:
            True if successful, False otherwise
        """
        try:
            import uuid
            from datetime import datetime

            # Generate embedding for the content using Cohere
            response = self.cohere_client.embed(
                texts=[message],
                model="embed-english-v3.0",
                input_type="search_document"
            )
            content_embedding = response.embeddings[0]

            # Add to Qdrant
            record_id = str(uuid.uuid4())

            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=record_id,
                        vector=content_embedding,
                        payload={
                            "user_id": user_id,
                            "message": message,
                            "timestamp": datetime.now().isoformat(),
                            "metadata": metadata or {}
                        }
                    )
                ]
            )

            logger.info(f"Stored knowledge with ID: {record_id}")
            return True

        except Exception as e:
            logger.error(f"Error storing knowledge: {str(e)}")
            return False


# Global instance for easy access
knowledge_agent_instance = KnowledgeAgent()


async def knowledge_agent(message: str, user_id: str) -> str:
    """
    Handle knowledge retrieval tasks
    """
    try:
        # Search for relevant information in the knowledge base
        result = await knowledge_agent_instance.search(message, user_id)
        return result
    except Exception as e:
        logger.error(f"Knowledge agent error: {str(e)}")
        return f"Knowledge search error: {str(e)}"