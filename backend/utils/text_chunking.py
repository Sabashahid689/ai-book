from typing import List


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text: The input text to be chunked
        chunk_size: The maximum size of each chunk (in characters)
        overlap: The number of characters to overlap between chunks
    
    Returns:
        A list of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this is the last chunk, include all remaining text
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Find a good breaking point (try to break at sentence or word boundary)
        chunk = text[start:end]
        break_point = find_break_point(chunk, chunk_size - overlap)
        
        if break_point and break_point > 0:
            actual_end = start + break_point
            chunks.append(text[start:actual_end])
            start = actual_end - overlap
        else:
            # If no good break point found, just cut at the limit
            chunks.append(text[start:end])
            start = end - overlap
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def find_break_point(chunk: str, preferred_size: int) -> int:
    """Find an appropriate break point in a chunk."""
    # Look for sentence boundaries first
    for i in range(preferred_size, len(chunk)):
        if chunk[i] in '.!?':
            # Break after the sentence
            return i + 1
    
    # If no sentence boundary, look for word boundaries
    for i in range(preferred_size, len(chunk)):
        if chunk[i] == ' ':
            return i
    
    # If no good break point found, just return the preferred size
    return preferred_size


def chunk_textbook_content(content: str, chunk_size: int = 512, overlap: int = 50) -> List[dict]:
    """
    Chunk textbook content with additional metadata for each chunk.
    
    Args:
        content: The textbook content to chunk
        chunk_size: The maximum size of each chunk (in characters)
        overlap: The number of characters to overlap between chunks
    
    Returns:
        A list of dictionaries containing chunk text and metadata
    """
    chunks = chunk_text(content, chunk_size, overlap)
    
    chunked_content = []
    for i, chunk in enumerate(chunks):
        chunked_content.append({
            "text": chunk,
            "index": i,
            "size": len(chunk)
        })
    
    return chunked_content