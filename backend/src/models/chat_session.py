from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .query import Query
from .response import Response


class ChatSession(BaseModel):
    id: str
    user_id: Optional[str] = None
    start_time: datetime
    last_activity: Optional[datetime] = None
    messages: List[Query] = []  # List of queries and responses in the conversation

    class Config:
        json_schema_extra = {
            "example": {
                "id": "session-123",
                "user_id": "user-456",
                "start_time": "2023-10-10T12:00:00Z",
                "last_activity": "2023-10-10T12:05:30Z",
                "messages": [
                    {
                        "id": "query-123",
                        "text": "What are the main themes in this book?",
                        "timestamp": "2023-10-10T12:00:00Z"
                    }
                ]
            }
        }