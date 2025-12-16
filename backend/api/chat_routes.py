from fastapi import APIRouter, HTTPException
from typing import List
import logging
from datetime import datetime
from models.api_responses import (
    ChatQueryRequest,
    ChatResponse,
    ConversationResponse,
    SourceReferenceResponse
)
from models.textbook_content import TextbookContent
from utils.qdrant_client import qdrant_manager
from utils.embedding.generator import embedding_generator
from services.embedding_service import embedding_service


router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatQueryRequest):
    """
    Submit a question to the RAG chatbot and receive an answer based on textbook content.
    """
    try:
        # Generate embedding for the question
        question_embedding = embedding_generator.generate_embedding(request.question)
        
        # Search for similar content in Qdrant
        search_results = qdrant_manager.search_similar(
            query_embedding=question_embedding,
            limit=5  # Retrieve top 5 results
        )
        
        if not search_results:
            # If no relevant content found, return an appropriate response
            return ChatResponse(
                answer="I couldn't find relevant content in the textbook to answer your question.",
                sources=[],
                session_id=request.session_id or "temp_session",
                timestamp=datetime.utcnow()
            )
        
        # Construct the response from the search results
        # In a real implementation, you would use a language model to generate the answer
        # based on the retrieved content and the question
        context_texts = [result["chunk_text"] for result in search_results]
        context = " ".join(context_texts)
        
        # For this implementation, we'll just return a synthetic response based on the context
        answer = f"Based on the textbook content: {context[:500]}..."  # Truncate for demo
        
        # Create source references
        sources = []
        for result in search_results:
            source = SourceReferenceResponse(
                content_id=result["content_id"],
                title=f"Chapter {result['metadata'].get('chapter_number', 'N/A')}", 
                chapter_number=result["metadata"].get("chapter_number", 0),
                section_number=result["metadata"].get("section_number", "N/A")
            )
            sources.append(source)
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=request.session_id or "temp_session",
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        logging.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history", response_model=List[ConversationResponse])
async def get_conversation_history(session_id: str):
    """
    Retrieve the conversation history for a specific session.
    Note: This is a simplified implementation that doesn't store conversation history.
    In a real implementation, this would query the database for stored conversations.
    """
    # In a real implementation, this would fetch from the database
    # For now, we'll return an empty list
    return []