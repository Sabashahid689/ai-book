# API Contracts: AI-Native Textbook RAG Chatbot

## 1. Chatbot Interaction API

### 1.1. Submit Question to Chatbot
- **Endpoint**: `POST /api/chat/query`
- **Description**: Submit a question to the RAG chatbot and receive an answer based on textbook content
- **Request Body**:
  ```json
  {
    "question": "string (required) - The user's question",
    "session_id": "string (optional) - Session identifier to maintain conversation context",
    "user_id": "string (optional) - User identifier for personalization",
    "language": "string (optional) - Language code, defaults to 'en'"
  }
  ```
- **Response**:
  - **Success (200)**:
    ```json
    {
      "answer": "string - The chatbot's answer based on textbook content",
      "sources": [
        {
          "content_id": "string - ID of the textbook content used",
          "title": "string - Title of the referenced content",
          "chapter_number": "integer - Chapter number",
          "section_number": "string - Section number"
        }
      ],
      "session_id": "string - Session identifier",
      "timestamp": "datetime - When the response was generated"
    }
    ```
  - **Validation Error (400)**:
    ```json
    {
      "error": "string - Description of the validation error"
    }
    ```
  - **No Relevant Sources (404)**:
    ```json
    {
      "error": "No relevant content found in textbook to answer the question",
      "suggestion": "string - Suggested related content or chapter to explore"
    }
    ```
  - **Server Error (500)**:
    ```json
    {
      "error": "string - Description of the server error"
    }
    ```

### 1.2. Get Conversation History
- **Endpoint**: `GET /api/chat/history`
- **Description**: Retrieve the conversation history for a specific session
- **Query Parameters**:
  - `session_id`: "string (required) - Session identifier"
- **Response**:
  - **Success (200)**:
    ```json
    [
      {
        "id": "string - Message ID",
        "role": "string - 'user' or 'assistant'",
        "content": "string - Message content",
        "timestamp": "datetime - When the message was created",
        "sources": [
          {
            "content_id": "string - ID of referenced content",
            "title": "string - Title of the referenced content"
          }
        ]
      }
    ]
    ```
  - **Not Found (404)**: If session_id doesn't exist

## 2. Textbook Content API

### 2.1. Get All Chapters
- **Endpoint**: `GET /api/textbook/chapters`
- **Description**: Retrieve a list of all textbook chapters
- **Response**:
  - **Success (200)**:
    ```json
    [
      {
        "id": "string - Chapter ID",
        "title": "string - Chapter title",
        "chapter_number": "integer - Chapter number (1-6)",
        "description": "string - Brief description of the chapter",
        "word_count": "integer - Approximate word count",
        "estimated_reading_time": "integer - Reading time in minutes"
      }
    ]
    ```

### 2.2. Get Chapter Content
- **Endpoint**: `GET /api/textbook/chapters/{chapter_number}`
- **Description**: Retrieve the content of a specific chapter
- **Path Parameters**:
  - `chapter_number`: "integer (required) - Chapter number between 1 and 6"
- **Response**:
  - **Success (200)**:
    ```json
    {
      "id": "string - Chapter ID",
      "title": "string - Chapter title",
      "chapter_number": "integer - Chapter number",
      "content": "string - Full chapter content in Markdown format",
      "sections": [
        {
          "id": "string - Section ID",
          "title": "string - Section title",
          "section_number": "string - Section number (e.g., '2.1', '2.2.1')",
          "content": "string - Section content in Markdown format"
        }
      ],
      "metadata": {
        "author": "string - Author of the chapter",
        "last_modified": "datetime - Last modification date",
        "language": "string - Language code"
      }
    }
    ```
  - **Not Found (404)**: If chapter doesn't exist

### 2.3. Search Textbook Content
- **Endpoint**: `GET /api/textbook/search`
- **Description**: Search textbook content based on query
- **Query Parameters**:
  - `q`: "string (required) - Search query"
  - `chapter`: "integer (optional) - Limit search to specific chapter (1-6)"
  - `limit`: "integer (optional) - Number of results to return, default 10, max 50"
- **Response**:
  - **Success (200)**:
    ```json
    [
      {
        "content_id": "string - ID of the content chunk",
        "title": "string - Title of the content",
        "chapter_number": "integer - Chapter number",
        "section_number": "string - Section number",
        "preview": "string - Preview of the content with query match highlighted",
        "relevance_score": "number - Relevance score between 0 and 1"
      }
    ]
    ```

## 3. Personalization API

### 3.1. Get Personalization Settings
- **Endpoint**: `GET /api/personalization/settings`
- **Description**: Retrieve the user's personalization settings
- **Request Headers**:
  - `Authorization`: "Bearer {token}"
- **Response**:
  - **Success (200)**:
    ```json
    {
      "user_id": "string - User identifier",
      "preferred_language": "string - Preferred language (default 'en')",
      "difficulty_level": "string - Preferred difficulty ('beginner', 'intermediate', 'advanced')",
      "interests": ["string - List of topic interests"],
      "learning_goals": ["string - List of learning objectives"],
      "reading_history": [
        {
          "content_id": "string - ID of recently read content",
          "title": "string - Title of the content",
          "timestamp": "datetime - When it was read"
        }
      ],
      "quiz_performance": {
        "total_questions_answered": "integer",
        "correct_answer_rate": "number - Percentage between 0 and 100"
      }
    }
    ```

### 3.2. Update Personalization Settings
- **Endpoint**: `PUT /api/personalization/settings`
- **Description**: Update the user's personalization settings
- **Request Headers**:
  - `Authorization`: "Bearer {token}"
- **Request Body**:
  ```json
  {
    "preferred_language": "string (optional) - Preferred language",
    "difficulty_level": "string (optional) - Preferred difficulty level",
    "interests": ["string (optional) - List of topic interests"],
    "learning_goals": ["string (optional) - List of learning objectives"]
  }
  ```
- **Response**:
  - **Success (200)**:
    ```json
    {
      "message": "Personalization settings updated successfully",
      "updated_settings": "{same format as GET response}"
    }
    ```

## 4. Content Embedding API (Internal)

### 4.1. Create Embeddings for Content
- **Endpoint**: `POST /api/internal/embeddings`
- **Description**: Create vector embeddings for textbook content (internal use only)
- **Request Body**:
  ```json
  {
    "content_id": "string - ID of the content to embed",
    "content": "string - The content text to create embeddings for",
    "language": "string - Language of the content",
    "chunk_size": "integer (optional) - Size of text chunks for embedding, default 512"
  }
  ```
- **Response**:
  - **Success (201)**:
    ```json
    {
      "message": "Embeddings created successfully",
      "content_id": "string - ID of the content that was embedded",
      "chunks_processed": "integer - Number of text chunks processed"
    }
    ```
- **Notes**: This endpoint should require authentication and be restricted to internal use only.

## 5. Common Error Responses

All endpoints may return these common error responses:

- **Authentication Error (401)**:
  ```json
  {
    "error": "Authentication required or token invalid"
  }
  ```

- **Rate Limit Exceeded (429)**:
  ```json
  {
    "error": "Rate limit exceeded. Please try again later."
  }
  ```

- **Server Error (500)**:
  ```json
  {
    "error": "Internal server error. Please try again later."
  }
  ```

## 6. API Security and Rate Limits

- All public-facing endpoints have rate limiting (100 requests/hour per IP)
- Authentication required for personalization endpoints using JWT tokens
- Internal endpoints (like embedding creation) are protected with API keys
- All query parameters and request bodies are validated to prevent injection attacks