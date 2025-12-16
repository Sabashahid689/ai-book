from fastapi import APIRouter, HTTPException
from typing import Optional
from ..models.query import Query as QueryModel
from ..models.response import Response as ResponseModel
from ..services.chat_service import ChatService
from ..config.settings import settings


router = APIRouter()


@router.post("/chat")
async def chat_endpoint(
    query: str,
    session_id: Optional[str] = None
):
    """
    Main chat endpoint that retrieves relevant chunks and returns Gemini-generated answer.
    """
    try:
        # Create a query object
        query_obj = QueryModel(
            text=query,
            session_id=session_id
        )
        
        # Generate response using the chat service
        chat_service = ChatService()
        response = chat_service.generate_response(query_obj)
        
        return {
            "response": response.content,
            "sources": response.sources,
            "query_id": response.query_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@router.post("/chat-full")
async def chat_full_endpoint(query_obj: QueryModel):
    """
    Full chat endpoint that accepts a complete Query model.
    """
    try:
        # Generate response using the chat service
        chat_service = ChatService()
        response = chat_service.generate_response(query_obj)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")