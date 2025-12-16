import os
import math
import glob
from typing import Dict, List


def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Calculate the estimated reading time for a text.
    
    Args:
        text: The text to analyze
        words_per_minute: Reading speed in words per minute (default 200)
        
    Returns:
        Estimated reading time in minutes
    """
    # Count words in the text
    words = len(text.split())
    minutes = words / words_per_minute
    # Round up to the nearest minute
    return math.ceil(minutes)


def calculate_word_count(text: str) -> int:
    """
    Calculate the word count for a text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Number of words in the text
    """
    return len(text.split())


def generate_metadata_for_chapters(docs_path: str = "frontend/docs/"):
    """
    Generate metadata for all chapter files and update their frontmatter.
    
    Args:
        docs_path: Path to the docs directory
    """
    # Find all markdown files in the docs directory
    chapter_files = glob.glob(os.path.join(docs_path, "*.md"))
    
    for file_path in chapter_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split the content to separate frontmatter from the rest
        lines = content.split('\n')
        frontmatter_start = -1
        frontmatter_end = -1
        
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if frontmatter_start == -1:
                    frontmatter_start = i
                elif frontmatter_end == -1:
                    frontmatter_end = i
                    break
        
        if frontmatter_start != -1 and frontmatter_end != -1:
            # Extract frontmatter and content
            frontmatter = lines[frontmatter_start:frontmatter_end + 1]
            content_lines = lines[frontmatter_end + 1:]
            
            # Calculate metadata from content (excluding frontmatter)
            content_text = '\n'.join(content_lines)
            word_count = calculate_word_count(content_text)
            reading_time = calculate_reading_time(content_text)
            
            # Update frontmatter with metadata
            updated_frontmatter = []
            frontmatter_dict = {}
            
            # Parse existing frontmatter
            for line in frontmatter[1:-1]:  # Skip the --- lines
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter_dict[key.strip()] = value.strip()
            
            # Add or update metadata
            frontmatter_dict['word_count'] = str(word_count)
            frontmatter_dict['estimated_reading_time'] = str(reading_time)
            
            # Rebuild frontmatter
            updated_frontmatter = ['---']
            for key, value in frontmatter_dict.items():
                updated_frontmatter.append(f'{key}: {value}')
            updated_frontmatter.append('---')
            
            # Combine everything together
            updated_content = '\n'.join(updated_frontmatter + content_lines)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated metadata for {os.path.basename(file_path)}: "
                  f"{word_count} words, ~{reading_time} min read")
        else:
            print(f"No frontmatter found in {os.path.basename(file_path)}")


if __name__ == "__main__":
    generate_metadata_for_chapters()