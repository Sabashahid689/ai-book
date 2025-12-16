from typing import List, Dict, Any
import logging
from utils.qdrant_client import qdrant_manager
from utils.text_chunking import chunk_textbook_content
from utils.embedding.generator import embedding_generator
from models.textbook_content import TextbookContent


class EmbeddingService:
    def __init__(self):
        self.qdrant = qdrant_manager
        self.chunker = chunk_textbook_content
        self.generator = embedding_generator

    def create_embeddings_for_content(self, 
                                      content: TextbookContent, 
                                      chunk_size: int = 512, 
                                      overlap: int = 50) -> bool:
        """
        Create and store embeddings for a textbook content item.
        
        Args:
            content: TextbookContent model instance
            chunk_size: Size of text chunks for embedding
            overlap: Overlap between chunks
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Chunk the content
            chunked_content = self.chunker(content.content, chunk_size, overlap)
            
            # Process each chunk
            for chunk in chunked_content:
                # Generate embedding for the chunk
                embedding = self.generator.generate_embedding(chunk["text"])
                
                # Prepare metadata for Qdrant
                metadata = {
                    "content_id": content.id,
                    "title": content.title,
                    "chapter_number": content.chapter_number,
                    "section_number": content.section_number,
                    "language": content.language,
                    "level": content.level.value if content.level else "beginner"
                }
                
                # Store the embedding in Qdrant
                content_id_with_chunk = f"{content.id}_chunk_{chunk['index']}"
                self.qdrant.store_embedding(
                    content_id=content_id_with_chunk,
                    embedding=embedding,
                    chunk_text=chunk["text"],
                    chunk_index=chunk["index"],
                    metadata=metadata
                )
            
            return True
        except Exception as e:
            logging.error(f"Error creating embeddings for content {content.id}: {str(e)}")
            return False

    def create_embeddings_for_sample_content(self):
        """
        Create embeddings for sample textbook content to demonstrate the functionality.
        """
        # Sample content for testing
        sample_content = TextbookContent(
            id="sample-chapter-1",
            title="Introduction to Physical AI",
            content="""
            Physical AI is an interdisciplinary field that combines robotics, artificial intelligence, 
            and control theory to create machines that can interact with the physical world intelligently. 
            This field encompasses the design, construction, and operation of robots that can perceive, 
            reason, and act in real-world environments.
            
            The core concepts of Physical AI include:
            
            1. Perception: The ability to sense and interpret the environment using various sensors like 
               cameras, LIDAR, and tactile sensors.
            
            2. Reasoning: The capacity to process sensory information and make decisions based on 
               algorithms and learned patterns.
            
            3. Action: The capability to execute physical movements and manipulate objects in the 
               environment.
            
            Physical AI systems must handle uncertainty in the real world, deal with incomplete 
            information, and adapt to changing conditions. This requires sophisticated algorithms 
            that can work with noisy data and make robust decisions.
            """,
            chapter_number=1,
            section_number="1.1",
            language="en",
            level="intermediate"
        )
        
        # Create embeddings for the sample content
        success = self.create_embeddings_for_content(sample_content)
        return success


# Create a singleton instance
embedding_service = EmbeddingService()