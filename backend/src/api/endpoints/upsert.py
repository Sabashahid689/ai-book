from fastapi import APIRouter, HTTPException
from typing import List
from ..models.knowledge_chunk import KnowledgeChunk
from ..services.storage_service import StorageService
from ..services.embedding_service import EmbeddingService


router = APIRouter()


@router.post("/upsert")
async def upsert_knowledge_chunks(chunks: List[KnowledgeChunk]):
    """
    Store text chunks in Qdrant vector database.
    """
    try:
        # Generate embeddings for chunks if they don't already have them
        embedding_service = EmbeddingService()
        chunks_with_embeddings = embedding_service.generate_knowledge_chunk_embeddings(chunks)
        
        # Store the chunks in Qdrant
        storage_service = StorageService()
        success = storage_service.upsert_chunks(chunks_with_embeddings)
        
        if success:
            return {
                "success": True,
                "inserted_count": len(chunks_with_embeddings)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upsert chunks")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error upserting chunks: {str(e)}")


@router.post("/upsert-single")
async def upsert_single_chunk(chunk: KnowledgeChunk):
    """
    Store a single text chunk in Qdrant vector database.
    """
    try:
        # Generate embeddings for the chunk if they don't already have them
        embedding_service = EmbeddingService()
        chunks_with_embeddings = embedding_service.generate_knowledge_chunk_embeddings([chunk])
        
        # Store the chunk in Qdrant
        storage_service = StorageService()
        success = storage_service.upsert_chunks(chunks_with_embeddings)
        
        if success:
            return {
                "success": True,
                "inserted_count": 1
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upsert chunk")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error upserting chunk: {str(e)}")