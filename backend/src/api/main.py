from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.settings import settings


def create_app():
    app = FastAPI(
        title="Book Content Chatbot API",
        description="API for a RAG-based chatbot system that allows users to ask questions about book content and receive AI-generated answers",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    from .api.endpoints import embed, upsert, search, chat
    app.include_router(embed.router, prefix="/api/v1", tags=["embed"])
    app.include_router(upsert.router, prefix="/api/v1", tags=["upsert"])
    app.include_router(search.router, prefix="/api/v1", tags=["search"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "book-content-chatbot-api"}
    
    return app


app = create_app()