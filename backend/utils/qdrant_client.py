import os
import logging
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "textbook_content_embeddings"

class QdrantManager:
    def __init__(self):
        self.client = None
        self.collection_exists = False
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Qdrant client."""
        try:
            if QDRANT_URL and QDRANT_API_KEY:
                # Use Qdrant Cloud
                self.client = QdrantClient(
                    url=QDRANT_URL,
                    api_key=QDRANT_API_KEY,
                    timeout=10
                )
            else:
                # For development, try local Qdrant
                self.client = QdrantClient(host="localhost", port=6333, timeout=5)

            # Verify connection and check if collection exists
            try:
                self.client.get_collection(COLLECTION_NAME)
                self.collection_exists = True
                print(f"Connected to Qdrant, collection '{COLLECTION_NAME}' exists")
            except:
                # Collection doesn't exist, will be created when needed
                print(f"Connected to Qdrant, collection '{COLLECTION_NAME}' will be created when needed")
                self.collection_exists = False

        except Exception as e:
            logging.warning(f"Could not connect to Qdrant: {str(e)}")
            print("Warning: Could not connect to Qdrant. Search functionality may not work.")
            self.client = None
            self.collection_exists = False

    def _create_collection(self):
        """Create the collection for storing textbook content embeddings if it doesn't exist."""
        if not self.client:
            logging.error("No Qdrant client available")
            return False

        try:
            if not self.collection_exists:
                print(f"Creating collection '{COLLECTION_NAME}'...")
                self.client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # Using sentence-transformers default size
                )
                self.collection_exists = True
                print(f"Collection '{COLLECTION_NAME}' created successfully")
            return True
        except Exception as e:
            logging.error(f"Error creating collection: {str(e)}")
            return False

    def store_embedding(self,
                        content_id: str,
                        embedding: List[float],
                        chunk_text: str,
                        chunk_index: int,
                        metadata: dict):
        """Store an embedding vector with its associated metadata."""
        if not self.client:
            logging.error("No Qdrant client available")
            return False

        # Create collection if it doesn't exist
        if not self.collection_exists:
            if not self._create_collection():
                return False

        try:
            # Prepare the point for storage
            points = [
                models.PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload={
                        "content_id": content_id,
                        "chunk_text": chunk_text,
                        "chunk_index": chunk_index,
                        **metadata
                    }
                )
            ]

            # Upload the point to Qdrant
            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )

            return True
        except Exception as e:
            logging.error(f"Error storing embedding: {str(e)}")
            return False

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[dict]:
        """Search for similar content based on the query embedding."""
        if not self.client:
            logging.error("No Qdrant client available")
            return []

        # Create collection if it doesn't exist
        if not self.collection_exists:
            if not self._create_collection():
                return []

        try:
            search_result = self.client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_embedding,
                limit=limit
            )

            # Extract the relevant information from search results
            results = []
            for hit in search_result:
                result = {
                    "content_id": hit.payload.get("content_id"),
                    "chunk_text": hit.payload.get("chunk_text"),
                    "chunk_index": hit.payload.get("chunk_index"),
                    "metadata": {k: v for k, v in hit.payload.items()
                               if k not in ["content_id", "chunk_text", "chunk_index"]},
                    "score": hit.score
                }
                results.append(result)

            return results
        except Exception as e:
            logging.error(f"Error searching for similar content: {str(e)}")
            return []

    def get_all_content_ids(self) -> List[str]:
        """Get all stored content IDs."""
        if not self.client:
            logging.error("No Qdrant client available")
            return []

        # Create collection if it doesn't exist
        if not self.collection_exists:
            if not self._create_collection():
                return []

        try:
            all_points = self.client.scroll(
                collection_name=COLLECTION_NAME,
                limit=10000,  # Adjust as needed
                with_payload=True
            )

            content_ids = []
            for point, _ in all_points:
                content_id = point.payload.get("content_id")
                if content_id and content_id not in content_ids:
                    content_ids.append(content_id)

            return content_ids
        except Exception as e:
            logging.error(f"Error getting content IDs: {str(e)}")
            return []


# Create a singleton instance
try:
    qdrant_manager = QdrantManager()
except Exception as e:
    logging.error(f"Error initializing QdrantManager: {str(e)}")
    # Create a mock instance that does nothing
    class MockQdrantManager:
        def store_embedding(self, *args, **kwargs): return False
        def search_similar(self, *args, **kwargs): return []
        def get_all_content_ids(self): return []

    qdrant_manager = MockQdrantManager()