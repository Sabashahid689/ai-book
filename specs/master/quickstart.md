# Quickstart Guide: AI-Native Textbook with RAG Chatbot

## Overview
This guide will help you quickly set up and run the AI-Native Textbook with RAG Chatbot system. The project consists of a Docusaurus-based frontend for the textbook and a FastAPI backend that handles RAG functionality using Qdrant for vector storage.

## Prerequisites
- Node.js (v16 or higher)
- Python (v3.11 or higher)
- Git
- Access to Qdrant Cloud (free tier sufficient)
- Access to Neon Database (free tier sufficient)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up Backend (FastAPI)
```bash
# Navigate to backend directory (if separate) or project root
cd backend  # or stay in root if monolithic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Qdrant and Neon credentials
```

### 3. Set Up Frontend (Docusaurus)
```bash
# Navigate to frontend directory (if separate) or project root
cd frontend  # or stay in root if monolithic

# Install dependencies
npm install

# Set up environment variables if needed
cp .env.example .env
# Edit .env with backend API endpoint
```

### 4. Environment Variables
For the backend, configure these in your `.env` file:
```env
QDRANT_URL=your-qdrant-cluster-url
QDRANT_API_KEY=your-qdrant-api-key
NEON_DB_URL=your-neon-database-url
SECRET_KEY=your-secret-key-for-jwt
DEBUG=true  # Set to false in production
```

## Running the Applications

### 1. Start the Backend
```bash
# From backend directory
python -m uvicorn main:app --reload --port 8000
```
The backend API will be available at `http://localhost:8000`

### 2. Start the Frontend
```bash
# From frontend directory
npm run start
```
The frontend will be available at `http://localhost:3000`

## Initial Setup Tasks

### 1. Populate Textbook Content
- Add your 6 chapters of content to the system
- Each chapter should be in Markdown format
- Use the `/api/internal/embeddings` endpoint to create vector embeddings for the content

### 2. Initialize Vector Database
```bash
# Example script to initialize vectors (details will depend on your implementation)
python scripts/initialize_embeddings.py
```

### 3. Test the RAG Chatbot
1. Navigate to the chat interface in your frontend
2. Submit a question related to your textbook content
3. Verify that the response is grounded in your textbook content
4. Check that sources are properly cited

## Key Endpoints

### Backend API
- `POST /api/chat/query` - Submit questions to the chatbot
- `GET /api/textbook/chapters` - Get available chapters
- `GET /api/textbook/chapters/{number}` - Get specific chapter content

### Frontend Development
- `http://localhost:3000` - Main textbook interface
- `http://localhost:3000/chat` - Chatbot interface

## Troubleshooting

### Common Issues:

1. **Backend not connecting to Qdrant**:
   - Verify your QDRANT_URL and QDRANT_API_KEY are correct
   - Check that your Qdrant cluster is running

2. **Frontend can't reach backend**:
   - Ensure both services are running
   - Check that REACT_APP_API_URL (or similar) points to your backend

3. **Embeddings not generating properly**:
   - Check that your content is properly formatted
   - Verify that your embedding model is configured correctly

## Next Steps

1. Customize the Docusaurus theme to match your branding
2. Add all 6 chapters of textbook content
3. Implement personalization features
4. Add Urdu translation if required
5. Deploy to production using GitHub Pages (frontend) and a Python hosting service (backend)