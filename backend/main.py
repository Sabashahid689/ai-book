import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.textbook_routes import router as textbook_router
from api.chat_routes import router as chat_router  # Now implemented
from api.search_routes import router as search_router  # Now implemented
from middleware.rate_limiter import rate_limit_middleware
from fastapi import Request


app = FastAPI(title="Textbook RAG API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
@app.middleware("http")
async def add_rate_limiting(request: Request, call_next):
    # Apply rate limiting to all requests except for health checks
    if request.url.path not in ["/", "/health"]:
        rate_limit_middleware(request)
    response = await call_next(request)
    return response

# Include API routers
app.include_router(textbook_router)
app.include_router(chat_router)  # Now implemented
app.include_router(search_router)  # Now implemented

@app.get("/")
def read_root():
    return {"message": "Welcome to the Textbook RAG API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)