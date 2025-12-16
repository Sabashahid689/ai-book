from typing import List
import numpy as np
import logging

# Try to import transformers and torch, but handle the case where they're not available
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    TORCH_AVAILABLE = True
except (ImportError, OSError) as e:
    logging.warning(f"Could not import transformers/torch: {str(e)}")
    TORCH_AVAILABLE = False
    AutoTokenizer = None
    AutoModel = None
    torch = None


class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator with a pre-trained model.

        Args:
            model_name: Name of the pre-trained model to use for embeddings
        """
        if TORCH_AVAILABLE:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)

                # Move model to CPU explicitly (though this is the default)
                self.model = self.model.cpu()
                self.model_available = True
            except Exception as e:
                logging.error(f"Error initializing embedding model: {str(e)}")
                self.model_available = False
        else:
            self.model_available = False
            logging.warning("Embedding model not available. Using mock implementation.")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate a single embedding for the given text.

        Args:
            text: Input text to generate embedding for

        Returns:
            A list of floats representing the embedding vector
        """
        if not TORCH_AVAILABLE or not self.model_available:
            # Return a mock embedding (384-dimensional vector of zeros with some variation)
            # This matches the expected dimensionality of the sentence-transformers model
            import random
            return [random.uniform(-0.1, 0.1) for _ in range(384)]

        try:
            # Tokenize the input text
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

            # Ensure tensors are on CPU
            inputs = {key: val.cpu() for key, val in inputs.items()}

            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use mean pooling to get sentence embedding
                embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

            # Convert to list and return
            return embeddings.tolist()
        except Exception as e:
            logging.error(f"Error generating embedding: {str(e)}")
            # Return a mock embedding as fallback
            import random
            return [random.uniform(-0.1, 0.1) for _ in range(384)]

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of input texts to generate embeddings for

        Returns:
            A list of embedding vectors (each vector is a list of floats)
        """
        embeddings = []

        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)

        return embeddings


# Create a singleton instance
embedding_generator = EmbeddingGenerator()