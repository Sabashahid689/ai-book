from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class TextbookContent(BaseModel):
    id: str
    title: str
    content: str
    chapter_number: int
    section_number: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}
    language: str = "en"
    level: Optional[DifficultyLevel] = None
    prerequisites: List[str] = []
    
    class Config:
        # Enable ORM mode for compatibility with database models
        from_attributes = True


class TextbookSummary(BaseModel):
    id: str
    title: str
    chapter_number: int
    description: Optional[str] = None
    word_count: Optional[int] = 0
    estimated_reading_time: Optional[int] = 0  # in minutes
    
    class Config:
        from_attributes = True


class UserInteraction(BaseModel):
    id: str
    user_id: Optional[str] = None
    session_id: str
    interaction_type: str  # "navigation", "search", "chat", "personalization"
    timestamp: datetime
    target_resource: str
    action_details: Optional[Dict[str, Any]] = {}
    
    class Config:
        from_attributes = True


class Conversation(BaseModel):
    id: str
    user_id: Optional[str] = None
    session_id: str
    timestamp: datetime
    messages: List[Dict[str, Any]]  # {"role": str, "content": str, "timestamp": datetime}
    source_references: List[str]  # List of TextbookContent IDs
    language: str = "en"
    
    class Config:
        from_attributes = True


class EmbeddingVector(BaseModel):
    id: str
    content_id: str
    chunk_text: str
    chunk_index: int
    embedding: List[float]
    metadata: Dict[str, Any]  # {"chapter_number": int, "section_number": str, "language": str, "level": str}
    created_at: datetime
    
    class Config:
        from_attributes = True


class PersonalizationSettings(BaseModel):
    user_id: str
    preferred_language: str = "en"
    difficulty_level: Optional[DifficultyLevel] = None
    interests: List[str] = []
    learning_goals: List[str] = []
    reading_history: List[Dict[str, Any]] = []  # [{"content_id": str, "title": str, "timestamp": datetime}]
    quiz_performance: Optional[Dict[str, Any]] = {"total_questions_answered": 0, "correct_answer_rate": 0.0}
    updated_at: datetime
    
    class Config:
        from_attributes = True