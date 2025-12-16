from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.api_responses import SearchQueryRequest, SearchResultResponse
from utils.qdrant_client import qdrant_manager
from utils.embedding.generator import embedding_generator


router = APIRouter(prefix="/api/textbook", tags=["search"])


@router.get("/search", response_model=List[SearchResultResponse])
async def search_textbook(request: SearchQueryRequest):
    """
    Search textbook content based on query.
    """
    try:
        # Generate embedding for the search query
        query_embedding = embedding_generator.generate_embedding(request.q)
        
        # Search for similar content in Qdrant
        search_results = qdrant_manager.search_similar(
            query_embedding=query_embedding,
            limit=request.limit
        )
        
        # Filter results by chapter if specified
        if request.chapter is not None:
            search_results = [
                result for result in search_results 
                if result.get("metadata", {}).get("chapter_number") == request.chapter
            ]
        
        # Convert to response format
        formatted_results = []
        for result in search_results:
            formatted_result = SearchResultResponse(
                content_id=result["content_id"],
                title=f"Chapter {result['metadata'].get('chapter_number', 'N/A')}",
                chapter_number=result["metadata"].get("chapter_number", 0),
                section_number=result["metadata"].get("section_number", "N/A"),
                preview=result["chunk_text"][:200] + "..." if len(result["chunk_text"]) > 200 else result["chunk_text"],  # Truncate preview
                relevance_score=result["score"]
            )
            formatted_results.append(formatted_result)
        
        return formatted_results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")