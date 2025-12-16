import os
import asyncpg
import logging
from typing import Optional
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Database configuration
NEON_DB_URL = os.getenv("NEON_DB_URL")


class DatabaseManager:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def init_pool(self):
        """Initialize the connection pool."""
        if not NEON_DB_URL:
            logging.warning("NEON_DB_URL not set, using mock database for development")
            return
        
        try:
            self.pool = await asyncpg.create_pool(
                dsn=NEON_DB_URL,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
            logging.info("Database connection pool created successfully")
        except Exception as e:
            logging.error(f"Failed to create database connection pool: {e}")
            raise

    async def close_pool(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            logging.info("Database connection pool closed")

    async def create_tables(self):
        """Create required tables in the database."""
        if not self.pool:
            logging.warning("No database pool available, skipping table creation")
            return
        
        # SQL to create the conversations table
        create_conversations_table = """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            session_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            messages JSONB NOT NULL,
            source_references TEXT[] DEFAULT '{}',
            language TEXT DEFAULT 'en'
        );
        """
        
        # SQL to create personalization settings table
        create_personalization_table = """
        CREATE TABLE IF NOT EXISTS personalization_settings (
            user_id TEXT PRIMARY KEY,
            preferred_language TEXT DEFAULT 'en',
            difficulty_level TEXT,
            interests TEXT[] DEFAULT '{}',
            learning_goals TEXT[] DEFAULT '{}',
            reading_history JSONB DEFAULT '[]',
            quiz_performance JSONB DEFAULT '{"total_questions_answered": 0, "correct_answer_rate": 0.0}',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # SQL to create user interactions table
        create_interactions_table = """
        CREATE TABLE IF NOT EXISTS user_interactions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            session_id TEXT NOT NULL,
            interaction_type TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_resource TEXT NOT NULL,
            action_details JSONB DEFAULT '{}'
        );
        """
        
        async with self.pool.acquire() as connection:
            await connection.execute(create_conversations_table)
            await connection.execute(create_personalization_table)
            await connection.execute(create_interactions_table)
            logging.info("Tables created successfully")


# Create a singleton instance
db_manager = DatabaseManager()