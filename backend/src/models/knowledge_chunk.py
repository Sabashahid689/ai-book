from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import numpy as np


class KnowledgeChunk(BaseModel):
    id: str
    content: str = Field(..., min_length=1)
    source_document: str
    source_page: Optional[int] = None
    source_section: Optional[str] = None
    embedding: Optional[List[float]] = None  # Vector representation
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "chunk-001",
                "content": "Artificial intelligence is a branch of computer science...",
                "source_document": "my-book.txt",
                "source_page": 42,
                "source_section": "Introduction",
                "embedding": [0.1, 0.2, 0.3],  # Simplified representation
                "metadata": {"chapter": "Introduction", "topic": "AI"}
            }
        }