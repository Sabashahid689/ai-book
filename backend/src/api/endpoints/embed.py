from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.knowledge_chunk import KnowledgeChunk
from ..services.embedding_service import EmbeddingService
from ..config.settings import settings


router = APIRouter()


@router.post("/embed")
async def generate_embeddings(text: str):
    """
    Generate embeddings for provided text using Cohere.
    """
    try:
        embedding_service = EmbeddingService()
        embeddings = embedding_service.generate_embeddings(text)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")


@router.post("/embed-batch")
async def generate_embeddings_batch(texts: List[str]):
    """
    Generate embeddings for a batch of texts using Cohere.
    """
    try:
        embedding_service = EmbeddingService()
        embeddings = embedding_service.generate_embeddings_batch(texts)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")


@router.post("/embed-chunks")
async def generate_chunk_embeddings(chunks: List[KnowledgeChunk]):
    """
    Generate embeddings for knowledge chunks.
    """
    try:
        embedding_service = EmbeddingService()
        embedded_chunks = embedding_service.generate_knowledge_chunk_embeddings(chunks)
        return {"chunks": embedded_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chunk embeddings: {str(e)}")