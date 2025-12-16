from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    cohere_api_key: str
    qdrant_api_key: Optional[str] = None
    gemini_api_key: str
    
    # Service URLs
    qdrant_url: str
    
    # Application settings
    environment: str = "development"
    debug: bool = True
    cors_origins: list = ["*"]  # Will be configured properly based on deployment
    
    # Performance settings
    response_timeout: int = 5  # seconds
    max_query_length: int = 2000  # characters
    top_k_chunks: int = 5  # number of chunks to retrieve
    
    class Config:
        env_file = ".env"


settings = Settings()