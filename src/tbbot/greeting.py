"""Greeting functionality for TBBot.

This module contains the greeting detection logic and agent handler
for processing student greetings and generating appropriate responses.
"""

import logging
from dataclasses import dataclass
from time import time


@dataclass
class Message:
    """Represents a student message."""
    content: str
    timestamp: float


@dataclass
class Response:
    """Represents an agent response."""
    content: str
    timestamp: float


def is_greeting(message: str) -> bool:
    """
    Detects if a message contains a greeting keyword.
    
    Args:
        message: The student's input message
        
    Returns:
        True if message contains greeting keywords, False otherwise
    """
    if not message:
        return False
    
    # Convert to lowercase for case-insensitive matching
    message_lower = message.lower()
    
    # Check for greeting keywords
    greeting_keywords = ["hello", "hi", "hey"]
    return any(keyword in message_lower for keyword in greeting_keywords)


def generate_greeting_response() -> str:
    """
    Generate the standard TBBot greeting message.
    
    Returns:
        The greeting response string
    """
    return "Hi, my name is TBBot. I am here to help you with your questions"


class GreetingAgent:
    """
    TBBot agent that handles greeting detection and response.
    """
    
    def __init__(self):
        """Initialize the agent with Agno framework."""
        try:
            # Initialize logging
            self.logger = logging.getLogger(__name__)
            self.logger.info("GreetingAgent initialized successfully")
            
            # Agent is ready to process messages
            self._initialized = True
            
        except Exception as e:
            # Log initialization failure with details
            logging.error(f"GreetingAgent initialization failed: {e}")
            raise
        
    def process_message(self, message: str) -> str:
        """
        Process a student message and return appropriate response.
        
        Args:
            message: The student's input message
            
        Returns:
            Response string (greeting or empty)
        """
        # Detect if the message is a greeting
        if is_greeting(message):
            # Generate and return greeting response
            return generate_greeting_response()
        
        # Return empty string for non-greeting messages
        return ""
