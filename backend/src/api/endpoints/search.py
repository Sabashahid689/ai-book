from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from ..models.knowledge_chunk import KnowledgeChunk
from ..services.retrieval_service import RetrievalService
from ..services.embedding_service import EmbeddingService
from ..services.storage_service import StorageService
from ..config.settings import settings


router = APIRouter()


@router.post("/search")
async def search_knowledge_chunks(
    query: str = Query(..., description="The query text to find similar chunks"),
    top_k: int = Query(default=settings.top_k_chunks, description="Number of top similar chunks to retrieve"),
    filters: Optional[Dict[str, Any]] = None
):
    """
    Retrieve relevant text chunks from Qdrant based on query.
    """
    try:
        # Generate embedding for the query
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.generate_embeddings(query)
        
        # Retrieve relevant chunks
        retrieval_service = RetrievalService()
        
        if filters:
            chunks = retrieval_service.search_chunks_with_filters(
                query_embedding, 
                top_k=top_k,
                filters=filters
            )
        else:
            chunks = retrieval_service.search_chunks(
                query_embedding,
                top_k=top_k
            )
        
        return {"chunks": chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching chunks: {str(e)}")


@router.get("/search/{chunk_id}")
async def get_chunk_by_id(chunk_id: str):
    """
    Retrieve a specific knowledge chunk by its ID.
    """
    try:
        storage_service = StorageService()
        chunk = storage_service.get_chunk(chunk_id)
        
        if chunk:
            return {"chunk": chunk}
        else:
            raise HTTPException(status_code=404, detail=f"Chunk with id {chunk_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chunk: {str(e)}")