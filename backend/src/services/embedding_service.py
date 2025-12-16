import cohere
from typing import List
from ..config.settings import settings
from ..models.knowledge_chunk import KnowledgeChunk


class EmbeddingService:
    def __init__(self):
        self.client = cohere.Client(settings.cohere_api_key)
    
    def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for a single text using Cohere.
        """
        response = self.client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        return response.embeddings[0]
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts using Cohere.
        """
        response = self.client.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"  # For documents being stored
        )
        return response.embeddings
    
    def generate_knowledge_chunk_embeddings(self, chunks: List[KnowledgeChunk]) -> List[KnowledgeChunk]:
        """
        Generate embeddings for a list of KnowledgeChunk objects.
        """
        texts = [chunk.content for chunk in chunks]
        embeddings = self.generate_embeddings_batch(texts)
        
        # Update chunks with embeddings
        updated_chunks = []
        for i, chunk in enumerate(chunks):
            updated_chunk = chunk.copy(update={"embedding": embeddings[i]})
            updated_chunks.append(updated_chunk)
        
        return updated_chunks