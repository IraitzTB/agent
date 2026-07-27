"""Greeting functionality for TBBot.

This module contains the greeting detection logic and agent handler
for processing student greetings and generating appropriate responses.
"""

import logging
import re
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


def detect_greeting_language(message: str) -> str | None:
    """
    Detects if a message contains a greeting and returns the language.
    
    Args:
        message: The student's input message
        
    Returns:
        Language code ('en', 'ca', 'eu', 'gl') if greeting detected, None otherwise
    """
    if not message or not message.strip():
        return None
    
    # Convert to lowercase for case-insensitive matching
    message_lower = message.lower()
    
    # Define greetings by language with priority order
    # Order matters: first match wins
    greetings = [
        (["hello", "hi", "hey"], "en"),  # English
        (["hola"], "ca"),  # Catalan
        (["kaixo"], "eu"),  # Basque
        (["ola"], "gl"),  # Galician
    ]
    
    # Split message into words and strip punctuation. A greeting is detected
    # when a cleaned token *starts with* one of the greeting keywords. This is
    # intentionally more permissive than exact whole-word matching (so "hiya",
    # "hello123" and "heya" are still detected as greetings) but more precise
    # than a naive substring search (so "machine" is NOT treated as "hi").
    words = [re.sub(r"[^\w]", "", w) for w in message_lower.split()]
    words = [w for w in words if w]  # drop empty tokens left by punctuation-only input

    # Check each language's greetings in priority order
    for keywords, language in greetings:
        if any(any(w.startswith(keyword) for w in words) for keyword in keywords):
            return language

    return None


def is_greeting(message: str) -> bool:
    """
    Return True if `message` contains a greeting, False otherwise.

    A thin boolean wrapper around :func:`detect_greeting_language` for callers
    that only need to know *whether* a message is a greeting (not which
    language the greeting is in).

    Args:
        message: The student's input message

    Returns:
        True if a greeting is detected, False otherwise (including for
        empty or whitespace-only input)
    """
    return detect_greeting_language(message) is not None


def generate_greeting_response(language: str = "en") -> str:
    """
    Generate the TBBot greeting message in the specified language.

    Args:
        language: Language code ('en', 'ca', 'eu', 'gl'). Defaults to 'en'
            so the common no-argument call returns the English greeting.

    Returns:
        The greeting response string in the specified language
    """
    responses = {
        "en": "Hi, my name is TBBot. I am here to help you with your questions",
        "ca": "Hola, el meu nom és TBBot. Estic aquí per ajudar-te amb les teves preguntes",
        "eu": "Kaixo, nire izena TBBot da. Hemen nago zure galderekin laguntzeko",
        "gl": "Ola, o meu nome é TBBot. Estou aquí para axudarche coas túas preguntas",
    }
    
    return responses.get(language, responses["en"])


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
            Response string (greeting in detected language or empty)
        """
        # Detect if the message is a greeting and get the language
        language = detect_greeting_language(message)
        
        if language:
            # Generate and return greeting response in detected language
            return generate_greeting_response(language)
        
        # Return empty string for non-greeting messages
        return ""
