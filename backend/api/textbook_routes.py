from fastapi import APIRouter, HTTPException
from typing import List
import os
import glob
import re
from models.api_responses import TextbookSummaryResponse, TextbookContentResponse
from utils.text_chunking import chunk_text


router = APIRouter(prefix="/api/textbook", tags=["textbook"])


def extract_chapter_metadata(file_path: str) -> dict:
    """Extract metadata from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for frontmatter (metadata between ---)
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
    
    metadata = {}
    if frontmatter_start != -1 and frontmatter_end != -1:
        # Extract metadata from frontmatter
        for line in lines[frontmatter_start + 1:frontmatter_end]:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
    
    # Extract content after frontmatter
    content_start = frontmatter_end + 1 if frontmatter_end != -1 else 0
    raw_content = '\n'.join(lines[content_start:])
    
    # Calculate additional metadata if not present
    if 'word_count' not in metadata:
        metadata['word_count'] = str(len(raw_content.split()))
    
    if 'estimated_reading_time' not in metadata:
        # Estimate reading time based on word count (200 words per minute)
        words_per_minute = 200
        words = int(metadata['word_count'])
        minutes = words / words_per_minute
        metadata['estimated_reading_time'] = str(int(minutes) + (1 if minutes % 1 != 0 else 0))
    
    # Extract title if not in metadata
    if 'title' not in metadata:
        # Look for the first H1 in the file
        title_match = re.search(r'^# (.+)$', raw_content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1)
        else:
            # Use the filename as title
            filename = os.path.basename(file_path)
            # Remove ch#- and .md from filename
            title = re.sub(r'^ch\d+-|\.md$', '', filename).replace('-', ' ').title()
            metadata['title'] = title
    
    # Extract chapter number from filename
    chapter_match = re.search(r'ch(\d+)-', os.path.basename(file_path))
    if chapter_match:
        metadata['chapter_number'] = int(chapter_match.group(1))
    else:
        metadata['chapter_number'] = 0
    
    # Create an ID based on filename
    metadata['id'] = os.path.basename(file_path).replace('.md', '')
    
    return metadata


@router.get("/chapters", response_model=List[TextbookSummaryResponse])
async def get_all_chapters():
    """Get a list of all textbook chapters."""
    # Get all markdown files in the docs directory
    # For this implementation, we'll simulate the data
    # In a real implementation, you would read from the actual docs directory
    
    # For demo purposes, I'll return summaries for the 6 chapters we created
    chapters = [
        {
            "id": "ch1-introduction-to-physical-ai",
            "title": "Introduction to Physical AI",
            "chapter_number": 1,
            "description": "Introduction to the concepts of Physical AI",
            "word_count": 294,
            "estimated_reading_time": 2
        },
        {
            "id": "ch2-foundations-of-robotics",
            "title": "Foundations of Robotics: Systems, Structure & Core Mechanisms",
            "chapter_number": 2,
            "description": "Overview of robotics systems and mechanisms",
            "word_count": 513,
            "estimated_reading_time": 3
        },
        {
            "id": "ch3-human-inspired-design",
            "title": "Human-Inspired Design Principles in Humanoid Robotics",
            "chapter_number": 3,
            "description": "Design principles inspired by human structure and function",
            "word_count": 652,
            "estimated_reading_time": 4
        },
        {
            "id": "ch4-perception-systems",
            "title": "Perception Systems in Humanoids",
            "chapter_number": 4,
            "description": "Sensing and perception in humanoid robots",
            "word_count": 726,
            "estimated_reading_time": 4
        },
        {
            "id": "ch5-ai-deep-learning-control",
            "title": "AI, Deep Learning & Control Systems",
            "chapter_number": 5,
            "description": "AI and control systems in humanoid robotics",
            "word_count": 925,
            "estimated_reading_time": 5
        },
        {
            "id": "ch6-humanoid-locomotion-manipulation",
            "title": "Humanoid Locomotion and Manipulation",
            "chapter_number": 6,
            "description": "Locomotion and manipulation in humanoid robots",
            "word_count": 1132,
            "estimated_reading_time": 6
        }
    ]
    
    # Convert to response models
    chapter_summaries = [
        TextbookSummaryResponse(
            id=chapter["id"],
            title=chapter["title"],
            chapter_number=chapter["chapter_number"],
            description=chapter["description"],
            word_count=chapter["word_count"],
            estimated_reading_time=chapter["estimated_reading_time"]
        ) for chapter in chapters
    ]
    
    return chapter_summaries


@router.get("/chapters/{chapter_number}", response_model=TextbookContentResponse)
async def get_chapter_content(chapter_number: int):
    """Get the content of a specific chapter."""
    if chapter_number < 1 or chapter_number > 6:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # For this implementation, we'll return simulated content
    # In a real implementation, you would read the actual chapter markdown file
    
    # Map chapter number to title and content
    chapters_content = {
        1: {
            "id": "ch1-introduction-to-physical-ai",
            "title": "Chapter 1: Introduction to Physical AI",
            "content": "# Chapter 1: Introduction to Physical AI\n\n## Overview\n\nPhysical AI is an interdisciplinary field that combines robotics, artificial intelligence, and control theory to create machines that can interact with the physical world intelligently. This field encompasses the design, construction, and operation of robots that can perceive, reason, and act in real-world environments.\n\n## Core Concepts\n\nThe fundamental concepts of Physical AI include:\n\n1. **Perception**: The ability to sense and interpret the environment using various sensors like cameras, LIDAR, and tactile sensors.\n\n2. **Reasoning**: The capacity to process sensory information and make decisions based on algorithms and learned patterns.\n\n3. **Action**: The capability to execute physical movements and manipulate objects in the environment.\n\nPhysical AI systems must handle uncertainty in the real world, deal with incomplete information, and adapt to changing conditions. This requires sophisticated algorithms that can work with noisy data and make robust decisions.\n\n## Chapter Summary\n\nThis chapter introduced the core concepts of Physical AI. In the next chapter, we will explore the foundations of robotics: systems, structure, and core mechanisms.",
            "chapter_number": 1,
            "section_number": "1.1",
            "language": "en",
            "level": "intermediate",
            "prerequisites": []
        },
        2: {
            "id": "ch2-foundations-of-robotics",
            "title": "Chapter 2: Foundations of Robotics: Systems, Structure & Core Mechanisms",
            "content": "# Chapter 2: Foundations of Robotics: Systems, Structure & Core Mechanisms\n\n## Introduction\n\nRobotics is the branch of technology that deals with the design, construction, operation, and application of robots. At its core, robotics combines mechanical engineering, electrical engineering, and computer science to create machines that can assist and work alongside humans.\n\n## Robot Systems\n\nA robot typically consists of several key subsystems:\n\n### Mechanical System\nThe mechanical system includes the robot's physical structure and actuators (motors, pistons, etc.) that enable movement. The design must consider:\n\n- Degrees of freedom: The number of independent movements a robot can perform\n- Range of motion: The physical limits of the robot's movement\n- Payload capacity: The maximum weight the robot can handle\n- Structural integrity: The ability to withstand forces during operation\n\n[Content continues...]",
            "chapter_number": 2,
            "section_number": "2.1",
            "language": "en",
            "level": "intermediate",
            "prerequisites": ["ch1-introduction-to-physical-ai"]
        },
        3: {
            "id": "ch3-human-inspired-design",
            "title": "Chapter 3: Human-Inspired Design Principles in Humanoid Robotics",
            "content": "# Chapter 3: Human-Inspired Design Principles in Humanoid Robotics\n\n## Introduction\n\nHumanoid robotics aims to create machines with human-like form and capabilities. The field draws heavily from our understanding of human anatomy, physiology, and cognition to inform design decisions. This biomimetic approach leverages millions of years of evolutionary optimization for navigating human environments and interacting with human-designed tools and spaces.\n\n[Content continues...]",
            "chapter_number": 3,
            "section_number": "3.1",
            "language": "en",
            "level": "intermediate",
            "prerequisites": ["ch1-introduction-to-physical-ai", "ch2-foundations-of-robotics"]
        },
        4: {
            "id": "ch4-perception-systems",
            "title": "Chapter 4: Perception Systems in Humanoids",
            "content": "# Chapter 4: Perception Systems in Humanoids\n\n## Introduction\n\nPerception systems are the foundation of intelligent behavior in humanoid robots. These systems enable robots to understand their environment, recognize objects and people, navigate spaces, and interact safely with humans and objects. A humanoid robot's perception capabilities must replicate and often exceed human sensory abilities to operate effectively in human environments.\n\n[Content continues...]",
            "chapter_number": 4,
            "section_number": "4.1",
            "language": "en",
            "level": "intermediate",
            "prerequisites": ["ch1-introduction-to-physical-ai", "ch3-human-inspired-design"]
        },
        5: {
            "id": "ch5-ai-deep-learning-control",
            "title": "Chapter 5: AI, Deep Learning & Control Systems",
            "content": "# Chapter 5: AI, Deep Learning & Control Systems\n\n## Introduction\n\nThe integration of AI and control systems is fundamental to creating intelligent humanoid robots that can perceive, reason, and act autonomously. This chapter explores the intersection of artificial intelligence, deep learning, and control theory as applied to humanoid robotics. The goal is to create systems that can learn from experience, adapt to new situations, and execute complex behaviors with human-like flexibility.\n\n[Content continues...]",
            "chapter_number": 5,
            "section_number": "5.1",
            "language": "en",
            "level": "advanced",
            "prerequisites": ["ch1-introduction-to-physical-ai", "ch4-perception-systems"]
        },
        6: {
            "id": "ch6-humanoid-locomotion-manipulation",
            "title": "Chapter 6: Humanoid Locomotion and Manipulation",
            "content": "# Chapter 6: Humanoid Locomotion and Manipulation\n\n## Introduction\n\nHumanoid locomotion and manipulation represent some of the most challenging aspects of humanoid robotics. These systems must replicate the remarkable capabilities of human movement and interaction with objects. This chapter covers the principles, technologies, and challenges involved in creating robots that can walk, balance, grasp, and manipulate in human-like ways.\n\n[Content continues...]",
            "chapter_number": 6,
            "section_number": "6.1",
            "language": "en",
            "level": "advanced",
            "prerequisites": ["ch2-foundations-of-robotics", "ch5-ai-deep-learning-control"]
        }
    }
    
    if chapter_number not in chapters_content:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = chapters_content[chapter_number]
    
    # Return the chapter content
    return TextbookContentResponse(
        id=chapter["id"],
        title=chapter["title"],
        content=chapter["content"],
        chapter_number=chapter["chapter_number"],
        section_number=chapter["section_number"],
        language=chapter["language"],
        level=chapter["level"],
        prerequisites=chapter["prerequisites"]
    )