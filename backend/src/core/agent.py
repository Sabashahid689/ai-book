import google.generativeai as genai
from typing import List
from ..models.knowledge_chunk import KnowledgeChunk
from ..config.settings import settings


class Agent:
    def __init__(self):
        # Initialize the Google Gemini client
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_answer_with_context(self, query: str, context_chunks: List[KnowledgeChunk], 
                                     conversation_history: List[tuple] = None) -> str:
        """
        Generate an answer based on query, context chunks, and optional conversation history.
        """
        # Build context from chunks
        context = self._build_context_from_chunks(context_chunks)
        
        # Build conversation history if available
        history_context = self._build_history_context(conversation_history) if conversation_history else ""
        
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

    def synthesize_information_from_chunks(self, query: str, chunks: List[KnowledgeChunk]) -> str:
        """
        Synthesize information from multiple knowledge chunks to provide a comprehensive answer.
        """
        # Aggregate chunks by document
        aggregated = self._aggregate_chunks_by_document(chunks)

        # Build a comprehensive context from aggregated information
        context_parts = []
        for doc_key, doc_data in aggregated.items():
            doc_context = f"Document: {doc_key}\nContent:\n"
            for i, content_part in enumerate(doc_data['content_parts']):
                doc_context += f"{i+1}. {content_part}\n"
            context_parts.append(doc_context)

        full_context = "\n".join(context_parts)

        # Construct the synthesis prompt
        prompt = f"""
        Based on the following information from various parts of the book,
        please synthesize a comprehensive answer to the query.

        Information:
        {full_context}

        Query: {query}

        Please provide a synthesized answer that combines insights from multiple sections:
        """

        try:
            # Generate the synthesized response
            result = self.model.generate_content(prompt)
            return result.text
        except Exception as e:
            print(f"Error synthesizing information: {e}")
            return "I'm sorry, but I couldn't synthesize the information at this time."

    def _aggregate_chunks_by_document(self, chunks: List[KnowledgeChunk]) -> dict:
        """
        Private method to aggregate chunks by document.
        """
        aggregated = {}
        for chunk in chunks:
            doc_key = chunk.source_document
            if doc_key not in aggregated:
                aggregated[doc_key] = {
                    'chunks': [],
                    'content_parts': [],
                    'metadata': chunk.metadata or {}
                }

            aggregated[doc_key]['chunks'].append(chunk)
            aggregated[doc_key]['content_parts'].append(chunk.content)

        return aggregated
    
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
    
    def _build_history_context(self, history: List[tuple]) -> str:
        """
        Build context from conversation history.
        History is a list of (query, response) tuples.
        """
        if not history:
            return ""
        
        history_parts = ["Previous conversation:"]
        for query, response in history:
            history_parts.append(f"Q: {query}")
            history_parts.append(f"A: {response}")
            history_parts.append("---")
        
        return "\n".join(history_parts) + "\n\n"