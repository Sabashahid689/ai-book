import qdrant_client
from qdrant_client import models
from typing import List, Optional
from ..models.knowledge_chunk import KnowledgeChunk
from ..config.settings import settings


class StorageService:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = "book_content_chunks"
        self._init_collection()
    
    def _init_collection(self):
        """
        Initialize the Qdrant collection for storing knowledge chunks.
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
            )
    
    def upsert_chunks(self, chunks: List[KnowledgeChunk]) -> bool:
        """
        Store knowledge chunks in Qdrant vector database.
        """
        try:
            points = []
            for chunk in chunks:
                points.append(
                    models.PointStruct(
                        id=chunk.id,
                        vector=chunk.embedding if chunk.embedding else [],
                        payload={
                            "content": chunk.content,
                            "source_document": chunk.source_document,
                            "source_page": chunk.source_page,
                            "source_section": chunk.source_section,
                            "metadata": chunk.metadata or {}
                        }
                    )
                )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error upserting chunks: {e}")
            return False
    
    def get_chunk(self, chunk_id: str) -> Optional[KnowledgeChunk]:
        """
        Retrieve a specific knowledge chunk by ID.
        """
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id]
            )
            
            if records:
                record = records[0]
                return KnowledgeChunk(
                    id=record.id,
                    content=record.payload.get("content"),
                    source_document=record.payload.get("source_document"),
                    source_page=record.payload.get("source_page"),
                    source_section=record.payload.get("source_section"),
                    metadata=record.payload.get("metadata")
                )
            return None
        except Exception as e:
            print(f"Error retrieving chunk {chunk_id}: {e}")
            return None
    
    def delete_chunks(self, chunk_ids: List[str]) -> bool:
        """
        Delete knowledge chunks by their IDs.
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=chunk_ids
            )
            return True
        except Exception as e:
            print(f"Error deleting chunks: {e}")
            return False