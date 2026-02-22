"""Configuration management for TBBot.

This module handles loading environment variables from .env files
and provides configuration settings for the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
# Search for .env in current directory and parent directories
load_dotenv(find_dotenv(), override=True)


class Config:
    """Application configuration loaded from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str | None = os.getenv("OPENAI_API_BASE")
    
    # LangWatch Configuration (optional)
    LANGWATCH_API_KEY: str | None = os.getenv("LANGWATCH_API_KEY")
    
    # Scenario Testing Configuration
    SCENARIO_BATCH_RUN_ID: str | None = os.getenv("SCENARIO_BATCH_RUN_ID")
    SCENARIO_CACHE_KEY: str | None = os.getenv("SCENARIO_CACHE_KEY")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if minimum required configuration is present."""
        return bool(cls.OPENAI_API_KEY)


# Create a singleton instance
config = Config()
