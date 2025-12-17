"""
Vector database operations (upsert, search)
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from auth.verify import get_current_user
from db.qdrant import get_qdrant_service, VectorRecord

router = APIRouter()


class VectorUpsertRequest(BaseModel):
    text: str
    user_id: str
    metadata: Optional[Dict[str, Any]] = None


class VectorSearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    limit: int = 10


class VectorUpsertResponse(BaseModel):
    success: bool
    vector_id: Optional[str] = None


class VectorSearchResponse(BaseModel):
    results: List[Dict[str, Any]]


@router.post("/upsert")
async def upsert_vector(
    request: VectorUpsertRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Store text in vector database with embedding
    """
    try:
        # Verify the user has permission to store data
        if current_user["user_id"] != request.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to store data for this user")

        qdrant_service = get_qdrant_service()

        # Initialize collection if needed
        qdrant_service.init_collection()

        # Upsert the vector
        vector_id = qdrant_service.upsert_vector(
            user_id=request.user_id,
            message=request.text,
            metadata=request.metadata
        )

        return VectorUpsertResponse(
            success=True,
            vector_id=vector_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing vector: {str(e)}")


@router.post("/search")
async def search_vector(
    request: VectorSearchRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Search vector database for relevant context
    """
    try:
        # If user_id is not provided in request, use current user's ID
        search_user_id = request.user_id or current_user["user_id"]

        # Verify the user has permission to search data
        if current_user["user_id"] != search_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to search data for this user")

        qdrant_service = get_qdrant_service()

        # Initialize collection if needed
        qdrant_service.init_collection()

        # Search the vectors
        results = qdrant_service.search_vectors(
            query=request.query,
            user_id=search_user_id,
            limit=request.limit
        )

        return VectorSearchResponse(
            results=results
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching vectors: {str(e)}")