# AI-Powered Book Content Chatbot

This project implements a RAG (Retrieval-Augmented Generation) chatbot system for book websites that allows users to ask questions about book content and receive AI-generated answers.

## Features

- **RAG Pipeline**: Uses Cohere for embeddings, Qdrant for vector storage, and Google Gemini for answer generation
- **Floating Chat Widget**: HTML/CSS/JS implementation that can be injected into existing book websites
- **API Endpoints**: 
  - `/embed` - Generate embeddings for provided text using Cohere
  - `/upsert` - Store text chunks in Qdrant vector database
  - `/search` - Retrieve relevant text chunks from Qdrant based on query
  - `/chat` - Main endpoint that retrieves relevant chunks and returns Gemini-generated answer
- **Book Knowledge Integration**: Leverages book content as the primary knowledge source
- **Seamless Integration**: Minimal, clean, dark-mode friendly design that integrates with existing book websites

## Architecture

- **Backend**: Python 3.11 with FastAPI
- **Frontend**: Vanilla JavaScript/CSS/HTML
- **Embeddings**: Cohere embed-english-v3.0
- **Vector Storage**: Qdrant
- **Language Model**: Google Gemini Pro

## Setup and Installation

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Set up environment variables by copying `.env.example` to `.env` and filling in your API keys:
   - `COHERE_API_KEY`
   - `QDRANT_API_KEY`
   - `GEMINI_API_KEY`
   - `QDRANT_URL`

5. Run the backend server:
   ```bash
   cd backend
   uvicorn src.api.main:app --reload
   ```

## Usage

1. The API will be available at `http://localhost:8000`
2. To integrate the chat widget into your book website:
   - Add the CSS file: `<link rel="stylesheet" href="/static/css/chat-widget.css">`
   - Add the JavaScript file: `<script src="/static/js/chat-widget.js"></script>`
   - Add the widget container: `<div id="book-chat-widget"></div>`

## How It Works

The system follows the RAG (Retrieval-Augmented Generation) pattern:

1. Book content is processed and stored as embeddings in Qdrant
2. When a user asks a question, the query is converted to an embedding
3. The system retrieves the most relevant book content chunks based on embedding similarity
4. The retrieved content is used as context for the Gemini model
5. The model generates a response that's grounded in the actual book content

## API Endpoints

- `POST /api/v1/embed` - Generate embeddings for provided text
- `POST /api/v1/upsert` - Store text chunks in Qdrant vector database
- `POST /api/v1/search` - Retrieve relevant text chunks from Qdrant
- `POST /api/v1/chat` - Main chat endpoint that returns Gemini-generated answers