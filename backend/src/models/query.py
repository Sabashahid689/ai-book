from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Query(BaseModel):
    id: Optional[str] = None
    text: str = Field(..., min_length=1, max_length=2000)
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "query-123",
                "text": "What are the main themes in this book?",
                "timestamp": "2023-10-10T12:00:00Z",
                "user_id": "user-456",
                "session_id": "session-789"
            }
        }