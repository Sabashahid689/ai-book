# Quickstart Guide: AI-Powered Book Content Chatbot

## Overview
This guide will help you set up and run the AI-powered chatbot for your book website. The system uses RAG (Retrieval-Augmented Generation) to provide accurate answers to questions about book content.

## Prerequisites
- Python 3.11 or higher
- pip package manager
- Access to Cohere API (embed-english-v3.0)
- Access to Qdrant vector database
- Access to Google Gemini API
- Node.js (optional, for development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

Required environment variables:
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: Your Qdrant API key
- `GEMINI_API_KEY`: Your Google Gemini API key

## Running the Backend

1. Start the backend API:
```bash
cd backend
python -m src.api.main
```

The API will be available at `http://localhost:8000`

## Running the Frontend

1. The frontend widget is designed to be included in your existing book website.
2. Copy the files from `frontend/static` to your website's static assets directory.
3. Include the widget in your HTML templates using the provided `chat-widget.html`.

## API Endpoints

- `POST /embed` - Generate embeddings for provided text
- `POST /upsert` - Store text chunks in Qdrant vector database
- `POST /search` - Retrieve relevant text chunks from Qdrant
- `POST /chat` - Main chat endpoint that returns Gemini-generated answers

## Integration with Book Website

1. Add the following to your website's main HTML template:
```html
<script src="/static/js/chat-widget.js"></script>
<link rel="stylesheet" href="/static/css/chat-widget.css">
```

2. Add the chat widget container to the DOM:
```html
<div id="book-chat-widget"></div>
```

3. Initialize the widget:
```javascript
document.addEventListener('DOMContentLoaded', function() {
  initChatWidget({
    apiEndpoint: 'http://localhost:8000/chat',
    title: 'Book Assistant'
  });
});
```

## Testing the System

1. To test the API endpoints, you can use curl or a tool like Postman:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main themes in this book?"}'
```

2. For frontend testing, simply load your book website and interact with the chat widget.

## Configuration

The system behavior can be configured by modifying the settings in `backend/src/config/settings.py`:
- Adjust timeout values for API calls
- Configure the number of retrieved chunks (top-k)
- Modify the prompt engineering for the Gemini model