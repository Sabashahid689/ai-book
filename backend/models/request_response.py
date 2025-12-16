from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class Chapter(BaseModel):
    id: str
    title: str
    chapter_number: int
    content: str
    sections: Optional[List['Section']] = []
    metadata: Optional[Dict[str, Any]] = {}
    
    class Config:
        from_attributes = True


class Section(BaseModel):
    id: str
    title: str
    section_number: str
    content: str
    
    class Config:
        from_attributes = True


class ChatQuery(BaseModel):
    question: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    language: str = "en"


class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]  # [{"content_id": str, "title": str, "chapter_number": int, "section_number": str}]
    session_id: str
    timestamp: datetime


class SearchQuery(BaseModel):
    q: str
    chapter: Optional[int] = None
    limit: Optional[int] = 10


class SearchResult(BaseModel):
    content_id: str
    title: str
    chapter_number: int
    section_number: Optional[str]
    preview: str
    relevance_score: float