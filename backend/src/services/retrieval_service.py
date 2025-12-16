import qdrant_client
from qdrant_client import models
from typing import List
from ..models.knowledge_chunk import KnowledgeChunk
from ..config.settings import settings


class RetrievalService:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = "book_content_chunks"
    
    def search_chunks(self, query_embedding: List[float], top_k: int = 5) -> List[KnowledgeChunk]:
        """
        Retrieve relevant knowledge chunks based on query embedding.
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )
            
            chunks = []
            for result in results:
                chunk = KnowledgeChunk(
                    id=result.id,
                    content=result.payload.get("content"),
                    source_document=result.payload.get("source_document"),
                    source_page=result.payload.get("source_page"),
                    source_section=result.payload.get("source_section"),
                    metadata=result.payload.get("metadata", {})
                )
                chunks.append(chunk)
            
            return chunks
        except Exception as e:
            print(f"Error searching chunks: {e}")
            return []
    
    def search_chunks_with_filters(self, query_embedding: List[float], 
                                   top_k: int = 5, 
                                   filters: dict = None) -> List[KnowledgeChunk]:
        """
        Retrieve relevant knowledge chunks with additional filters.
        """
        try:
            # Build filter conditions
            filter_conditions = []
            if filters:
                for key, value in filters.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )
            
            search_filter = models.Filter(must=filter_conditions) if filter_conditions else None
            
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True,
                query_filter=search_filter
            )
            
            chunks = []
            for result in results:
                chunk = KnowledgeChunk(
                    id=result.id,
                    content=result.payload.get("content"),
                    source_document=result.payload.get("source_document"),
                    source_page=result.payload.get("source_page"),
                    source_section=result.payload.get("source_section"),
                    metadata=result.payload.get("metadata", {})
                )
                chunks.append(chunk)
            
            return chunks
        except Exception as e:
            print(f"Error searching chunks with filters: {e}")
            return []

    def aggregate_chunks_by_document(self, chunks: List[KnowledgeChunk]) -> dict:
        """
        Aggregate knowledge chunks by document to synthesize information from multiple sources.
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