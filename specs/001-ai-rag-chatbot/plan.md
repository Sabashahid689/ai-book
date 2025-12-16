# Implementation Plan: AI-Powered Book Content Chatbot

**Branch**: `001-ai-rag-chatbot` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a complete RAG (Retrieval-Augmented Generation) chatbot system for the book website that allows users to ask questions about book content and receive AI-generated answers. The system will include a backend with Cohere embeddings, Qdrant vector storage, and Gemini for answer generation, plus a frontend floating chat widget integrated into the existing book website.

## Technical Context

**Language/Version**: Python 3.11 for backend, JavaScript ES6+ for frontend
**Primary Dependencies**:
  - Backend: FastAPI, Cohere Python SDK, Qdrant Python client, Google Gemini API
  - Frontend: Vanilla HTML/CSS/JS (no additional frameworks to maintain compatibility)
**Storage**: Qdrant vector database for embeddings, existing book website for frontend assets
**Testing**: pytest for backend API testing, manual testing for frontend integration
**Target Platform**: Web application server (backend), cross-browser compatible frontend widget
**Project Type**: Web/Microservice (backend API + frontend widget)
**Performance Goals**: <5 second response time for chat queries, <100ms for retrieval operations
**Constraints**:
  - Must integrate with existing book website without layout disruption
  - Use provided Cohere embed-english-v3.0 and Gemini models
  - Follow existing agent.py structure for Gemini integration
  - CORS headers must be configured properly for frontend-backend communication
**Scale/Scope**: Single book integration, supporting multiple concurrent users with streaming responses

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution file currently contains template placeholders and needs to be properly filled out. For this implementation plan, we'll follow standard best practices:

- Test-driven development will be used where feasible
- Code will be modular and maintainable
- Security and privacy considerations will be addressed
- Performance requirements will be met
- Integration will be backward-compatible where possible

### Gate Evaluation

- [x] Architecture follows separation of concerns
- [x] Technology choices are appropriate for requirements
- [x] API design follows standard patterns
- [x] Approach aligns with industry standards for RAG systems
- [x] No identified violations of standard best practices

### Post-Design Constitution Check

After implementing the design artifacts (data models, API contracts, architecture), the system still aligns with best practices:

- [x] Data models are well-defined with appropriate relationships
- [x] API contracts follow OpenAPI standards
- [x] Architecture maintains separation of concerns between frontend and backend
- [x] Security considerations are addressed through API keys and proper authentication
- [x] Performance requirements are achievable with the chosen architecture

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── query.py
│   │   ├── knowledge_chunk.py
│   │   └── response.py
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── storage_service.py
│   │   ├── retrieval_service.py
│   │   └── chat_service.py
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── embed.py
│   │   │   ├── upsert.py
│   │   │   ├── search.py
│   │   │   └── chat.py
│   │   └── main.py
│   ├── core/
│   │   └── agent.py
│   └── config/
│       └── settings.py
└── tests/
    ├── unit/
    └── integration/

frontend/
├── static/
│   ├── js/
│   │   └── chat-widget.js
│   ├── css/
│   │   └── chat-widget.css
│   └── assets/
└── templates/
    └── chat-widget.html
```

**Structure Decision**: Web application structure selected since this feature requires both backend API endpoints and frontend UI component. Backend handles API processing and RAG operations, frontend provides the chat interface that integrates into the existing book website.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Project Details

### Backend API Endpoints

1. **/embed** - Generate embeddings for provided text using Cohere
2. **/upsert** - Store text chunks in Qdrant vector database
3. **/search** - Retrieve relevant text chunks from Qdrant based on query
4. **/chat** - Main endpoint that retrieves relevant chunks and returns Gemini-generated answer

### Frontend Components

1. **Floating Chat Widget** - HTML/JS/CSS implementation that can be injected into the book website
2. Handles user input, communicates with backend API, displays conversation
3. Minimal, clean, dark-mode friendly design
4. Streaming or final response display as specified

### Integration Points

1. Widget script injection into book's root layout
2. API communication with proper CORS handling
3. Using existing Qdrant ingestion index as specified
