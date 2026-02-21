"""FastAPI application for TBBot REST API.

This module provides HTTP endpoints for interacting with TBBot's
educational AI agent functionality through a REST API.
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .greeting import GreetingAgent
from .models import ChatRequest, ChatResponse, HealthResponse

# Configure logger for API module
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="TBBot API",
    description="Educational AI agent for teaching AI agent development",
    version="1.0.0"
)

# Initialize agent instance
agent = GreetingAgent()


def configure_cors(app: FastAPI, origins: list[str]) -> None:
    """
    Configure CORS middleware for the FastAPI application.
    
    This function enables Cross-Origin Resource Sharing (CORS) to allow
    browser-based applications to call TBBot's API from different origins.
    CORS is disabled by default and must be explicitly enabled by calling
    this function.
    
    Args:
        app: The FastAPI application instance to configure
        origins: List of allowed origin URLs (e.g., ["http://localhost:3000"])
                Use ["*"] to allow all origins (not recommended for production)
    
    Example:
        configure_cors(app, ["http://localhost:3000", "https://example.com"])
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
        allow_headers=["*"],  # Allow all headers
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process student message and return agent response.
    
    Args:
        request: ChatRequest containing the student's message
        
    Returns:
        ChatResponse with the agent's response
        
    Raises:
        HTTPException: 500 status if internal error occurs during processing
    """
    try:
        # Process message through the agent
        response_text = agent.process_message(request.message)
        
        # Return response wrapped in ChatResponse model
        return ChatResponse(response=response_text)
        
    except Exception as e:
        # Log the error with full context for debugging
        logger.error(
            f"Error processing message in chat endpoint: {e}",
            exc_info=True,
            extra={"message_length": len(request.message)}
        )
        
        # Return 500 status with generic error message
        # (don't expose internal error details to clients)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Health check endpoint to verify service availability.
    
    Returns:
        HealthResponse with status "healthy"
    """
    return HealthResponse(status="healthy")
