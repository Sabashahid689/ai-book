import google.generativeai as genai
from typing import List
from ..models.query import Query
from ..models.response import Response
from ..models.knowledge_chunk import KnowledgeChunk
from ..services.embedding_service import EmbeddingService
from ..services.retrieval_service import RetrievalService
from ..config.settings import settings


class ChatService:
    def __init__(self):
        # Initialize the Google Gemini client
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize dependencies
        self.embedding_service = EmbeddingService()
        self.retrieval_service = RetrievalService()
    
    def generate_response(self, query: Query) -> Response:
        """
        Generate a response for a user query using RAG approach.
        """
        # Step 1: Get conversation history
        conversation_history = self.manage_conversation_context(query)

        # Step 2: Generate embedding for the query
        query_embedding = self.embedding_service.generate_embeddings(query.text)

        # Step 3: Retrieve relevant chunks from storage
        relevant_chunks = self.retrieval_service.search_chunks(
            query_embedding,
            top_k=settings.top_k_chunks
        )

        # Step 4: Generate context from retrieved chunks
        context = self._build_context_from_chunks(relevant_chunks)

        # Step 5: Generate AI response using Gemini
        ai_response = self._generate_ai_answer(query.text, context, conversation_history)

        # Step 6: Create and return response object
        response = Response(
            query_id=query.id or "",
            content=ai_response,
            sources=relevant_chunks,
            confidence=0.8  # Placeholder - would be calculated in a real implementation
        )

        return response
    
    def _build_context_from_chunks(self, chunks: List[KnowledgeChunk]) -> str:
        """
        Build context string from retrieved knowledge chunks.
        """
        context_parts = []
        for chunk in chunks:
            chunk_text = f"Source: {chunk.source_document}"
            if chunk.source_page:
                chunk_text += f", Page: {chunk.source_page}"
            if chunk.source_section:
                chunk_text += f", Section: {chunk.source_section}"
            chunk_text += f"\nContent: {chunk.content}\n"
            context_parts.append(chunk_text)
        
        return "\n".join(context_parts)

    def _generate_ai_answer(self, query: str, context: str, conversation_history: list = None) -> str:
        """
        Generate an AI answer based on the query, context, and optional conversation history.
        """
        # Build conversation history context if available
        history_context = ""
        if conversation_history:
            history_context = "Previous conversation:\n"
            for q, a in conversation_history:
                history_context += f"Q: {q}\nA: {a}\n"
            history_context += "\n"

        # Construct the prompt for the AI model
        prompt = f"""
        {history_context}
        Context information is below.
        ----------------------------
        {context}
        ----------------------------
        Given the context information and not prior knowledge, answer the query.
        Query: {query}
        Answer:
        """

        try:
            # Generate the response using the Gemini model
            result = self.model.generate_content(prompt)
            return result.text
        except Exception as e:
            print(f"Error generating AI answer: {e}")
            return "I'm sorry, but I couldn't generate a response at this time."

    def manage_conversation_context(self, query: Query, max_history: int = 5) -> list:
        """
        Manage conversation context by maintaining a limited history.
        In a real implementation, this would interface with a session store.
        For now, it returns an empty list as a placeholder.
        """
        # In a real implementation, this would retrieve the conversation history
        # from a database or cache based on the session_id
        return []