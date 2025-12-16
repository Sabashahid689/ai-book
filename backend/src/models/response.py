from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .knowledge_chunk import KnowledgeChunk


class SourceAttribution(BaseModel):
    chunk_id: str
    source_document: str
    source_page: Optional[int] = None
    source_section: Optional[str] = None
    content_snippet: str
    relevance_score: Optional[float] = None


class Response(BaseModel):
    id: Optional[str] = None
    query_id: str
    content: str = Field(..., min_length=1)
    sources: Optional[List[KnowledgeChunk]] = None
    source_attributions: Optional[List[SourceAttribution]] = None
    timestamp: Optional[datetime] = None
    confidence: Optional[float] = None  # Confidence score between 0 and 1
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "response-123",
                "query_id": "query-456",
                "content": "The main themes in this book include...",
                "sources": [
                    {
                        "id": "chunk-001",
                        "content": "Artificial intelligence is a branch of computer science...",
                        "source_document": "my-book.txt",
                        "source_page": 42,
                        "embedding": [0.1, 0.2, 0.3]  # Simplified representation
                    }
                ],
                "source_attributions": [
                    {
                        "chunk_id": "chunk-001",
                        "source_document": "my-book.txt",
                        "source_page": 42,
                        "source_section": "Introduction",
                        "content_snippet": "Artificial intelligence is a branch of computer science...",
                        "relevance_score": 0.92
                    }
                ],
                "timestamp": "2023-10-10T12:00:05Z",
                "confidence": 0.85
            }
        }