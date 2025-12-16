from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# Textbook content models
class TextbookContentResponse(BaseModel):
    id: str
    title: str
    content: str
    chapter_number: int
    section_number: Optional[str] = None
    sections: Optional[List['SectionResponse']] = []
    metadata: Optional[Dict[str, Any]] = {}
    language: str = "en"
    level: Optional[DifficultyLevel] = None
    prerequisites: List[str] = []


class SectionResponse(BaseModel):
    id: str
    title: str
    section_number: str
    content: str


class TextbookSummaryResponse(BaseModel):
    id: str
    title: str
    chapter_number: int
    description: Optional[str] = None
    word_count: Optional[int] = 0
    estimated_reading_time: Optional[int] = 0  # in minutes


# Chat models
class ChatQueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    language: str = "en"


class SourceReferenceResponse(BaseModel):
    content_id: str
    title: str
    chapter_number: int
    section_number: Optional[str]


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceReferenceResponse]
    session_id: str
    timestamp: datetime


class MessageResponse(BaseModel):
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    sources: Optional[List[SourceReferenceResponse]] = []


class ConversationResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    session_id: str
    timestamp: datetime
    messages: List[MessageResponse]
    source_references: List[str]  # List of TextbookContent IDs
    language: str = "en"


# Search models
class SearchQueryRequest(BaseModel):
    q: str
    chapter: Optional[int] = None
    limit: Optional[int] = 10


class SearchResultResponse(BaseModel):
    content_id: str
    title: str
    chapter_number: int
    section_number: Optional[str]
    preview: str
    relevance_score: float


# Personalization models
class PersonalizationSettingsRequest(BaseModel):
    preferred_language: Optional[str] = None
    difficulty_level: Optional[DifficultyLevel] = None
    interests: Optional[List[str]] = None
    learning_goals: Optional[List[str]] = None


class ReadingHistoryItem(BaseModel):
    content_id: str
    title: str
    timestamp: datetime


class QuizPerformance(BaseModel):
    total_questions_answered: int
    correct_answer_rate: float  # percentage


class PersonalizationSettingsResponse(BaseModel):
    user_id: str
    preferred_language: str
    difficulty_level: Optional[DifficultyLevel] = None
    interests: List[str] = []
    learning_goals: List[str] = []
    reading_history: List[ReadingHistoryItem] = []
    quiz_performance: QuizPerformance
    updated_at: datetime


# Response models for API endpoints
class SuccessResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str


class ChatHistoryResponse(BaseModel):
    messages: List[MessageResponse]