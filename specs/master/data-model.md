# Data Model: AI-Native Textbook with RAG Chatbot

## Core Entities

### 1. Textbook Content
- **Entity Name**: TextbookContent
- **Fields**:
  - `id` (string): Unique identifier for the content
  - `title` (string): Title of the chapter/section
  - `content` (string): Main text content
  - `chapter_number` (integer): Sequential chapter number (1-6)
  - `section_number` (string): Hierarchical section identifier (e.g., "1.2.3")
  - `metadata` (object): Additional information about the content
    - `author`: Author of the content
    - `last_modified`: Timestamp of last update
    - `word_count`: Number of words in content
    - `reading_time`: Estimated reading time in minutes
  - `language` (string): Language code (default: "en", optional: "ur" for Urdu)
  - `level` (string): Difficulty level ("beginner", "intermediate", "advanced")
  - `prerequisites` (array): List of prerequisite concepts
- **Relationships**: 
  - One-to-many with TextbookContent (parent-child for sections)
  - One-to-many with QuestionAnswer (content referenced by QA pairs)
- **Validation Rules**:
  - `chapter_number` must be between 1 and 6
  - `title` and `content` are required fields
  - `language` must be a valid ISO language code
- **State Transitions**: N/A (content is static once published)

### 2. User Interaction
- **Entity Name**: UserInteraction
- **Fields**:
  - `id` (string): Unique identifier for the interaction
  - `user_id` (string): Identifier for the user (if available)
  - `session_id` (string): Identifier for the user session
  - `interaction_type` (string): Type of interaction ("navigation", "search", "chat", "personalization")
  - `timestamp` (datetime): When the interaction occurred
  - `target_resource` (string): ID of the resource being interacted with
  - `action_details` (object): Specific details about the interaction
    - `search_query`: For search interactions
    - `question`: For chatbot interactions
    - `chapter_requested`: For navigation events
- **Relationships**:
  - Many-to-one with TextbookContent (if interaction relates to content)
- **Validation Rules**:
  - `interaction_type` must be one of the specified values
  - `timestamp` must be in the past or present
- **State Transitions**: N/A (interactions are logs of past events)

### 3. Chatbot Conversation
- **Entity Name**: Conversation
- **Fields**:
  - `id` (string): Unique identifier for the conversation
  - `user_id` (string): Identifier for the user (if available)
  - `session_id` (string): Identifier for the session
  - `timestamp` (datetime): When the conversation started
  - `messages` (array): List of messages in the conversation
    - `role`: "user" or "assistant"
    - `content`: The message content
    - `timestamp`: When the message was sent
  - `source_references` (array): List of TextbookContent IDs referenced in responses
  - `language` (string): Language of the conversation
- **Relationships**:
  - One-to-many with TextbookContent (referenced sources)
- **Validation Rules**:
  - Each conversation must have at least one message
  - Messages must alternate between user and assistant
  - Source references must exist in the TextbookContent
- **State Transitions**: N/A (conversations are logs of past events)

### 4. Embedding Vector
- **Entity Name**: EmbeddingVector
- **Fields**:
  - `id` (string): Unique identifier for the vector entry
  - `content_id` (string): Reference to associated TextbookContent
  - `chunk_text` (string): The text chunk that was embedded
  - `chunk_index` (integer): Position of the chunk in the original content
  - `embedding` (array): The actual embedding vector (float array)
  - `metadata` (object): Additional metadata for retrieval
    - `chapter_number`: Associated chapter number
    - `section_number`: Associated section number
    - `language`: Language of the text chunk
    - `level`: Difficulty level
  - `created_at` (datetime): When the embedding was created
- **Relationships**:
  - Many-to-one with TextbookContent (source of the embedding)
- **Validation Rules**:
  - `embedding` array must have consistent dimensions
  - `content_id` must reference an existing TextbookContent
  - `chunk_text` must not exceed max token limits
- **State Transitions**: N/A (embeddings are static once created)

### 5. Personalization Settings
- **Entity Name**: PersonalizationSettings
- **Fields**:
  - `user_id` (string): Identifier for the user
  - `preferred_language` (string): Default language preference
  - `difficulty_level` (string): Preferred content difficulty ("beginner", "intermediate", "advanced")
  - `interests` (array): Array of topic interests
  - `learning_goals` (array): Array of learning objectives
  - `reading_history` (array): Array of recently viewed content IDs
  - `quiz_performance` (object): Performance statistics on quizzes
    - `total_questions_answered`: Number of questions answered
    - `correct_answer_rate`: Percentage of correct answers
  - `updated_at` (datetime): When settings were last updated
- **Relationships**:
  - One-to-many with TextbookContent (reading history)
- **Validation Rules**:
  - `preferred_language` must be a supported language
  - `difficulty_level` must be one of the specified values
  - `interests` must be from a predefined list of topics
- **State Transitions**: Settings can be updated as user preferences change

## Relationships Summary

1. **TextbookContent** ← → **EmbeddingVector** (one-to-many)
2. **TextbookContent** ← → **UserInteraction** (many-to-one for interactions)
3. **TextbookContent** ← → **Conversation** (many-to-many via source_references)
4. **PersonalizationSettings** ← → **TextbookContent** (one-to-many for reading history)
5. **Conversation** ← → **UserInteraction** (one-to-many for chat interactions)