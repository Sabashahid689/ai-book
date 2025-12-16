# Data Model: AI-Powered Book Content Chatbot

## Entities

### Query
- **Description**: User input containing questions or prompts about the book content
- **Fields**:
  - `id`: Unique identifier for the query
  - `text`: The actual text of the user's question or prompt
  - `timestamp`: When the query was submitted
  - `user_id`: Identifier for the user (if applicable)
  - `session_id`: Identifier for the conversation session
- **Validation**:
  - `text` must not be empty
  - `text` length should be within reasonable limits (e.g., 1-2000 characters)

### Knowledge Chunk
- **Description**: Segments of book content stored in the system, associated with semantic representations
- **Fields**:
  - `id`: Unique identifier for the chunk
  - `content`: The text content from the book
  - `source_document`: Reference to the original book/document
  - `source_page` or `source_section`: Location within the document
  - `embedding`: Vector representation of the content for semantic search
  - `metadata`: Additional information about the chunk (e.g., chapter, topic)
- **Validation**:
  - `content` must not be empty
  - `source_document` must be valid
  - `embedding` must be a valid vector representation

### Response
- **Description**: Generated answer based on user query and relevant book content retrieved from the knowledge base
- **Fields**:
  - `id`: Unique identifier for the response
  - `query_id`: Reference to the original query
  - `content`: The generated answer text
  - `sources`: List of knowledge chunks used to generate the answer
  - `timestamp`: When the response was generated
  - `confidence`: Confidence score for the generated answer
- **Validation**:
  - `content` must not be empty
  - `query_id` must reference a valid query

### Chat Session
- **Description**: Represents a conversation session between a user and the chatbot
- **Fields**:
  - `id`: Unique identifier for the session
  - `user_id`: Identifier for the user (if applicable)
  - `start_time`: When the session started
  - `last_activity`: When the last interaction occurred
  - `messages`: List of messages in the conversation (queries and responses)
- **Validation**:
  - Must have a valid start time
  - Should have a reasonable timeout period

## Relationships

1. **Query** → *belongs to* → **Chat Session**
   - A query is part of a specific chat session

2. **Response** → *responds to* → **Query**
   - A response is generated for a specific query

3. **Response** → *references* → **Knowledge Chunk**
   - A response can reference multiple knowledge chunks that were used to generate the answer

4. **Knowledge Chunk** → *part of* → **Source Document**
   - Knowledge chunks are derived from specific source documents (books)

## State Transitions

### Query States
- `pending`: Query received, waiting for processing
- `processing`: Currently being processed by the system
- `completed`: Processing finished, response generated
- `failed`: Error occurred during processing

### Chat Session States
- `active`: Session is currently in progress
- `inactive`: No recent activity, may timeout
- `closed`: Session has ended