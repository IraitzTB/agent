"""Pydantic models for FastAPI request/response validation."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, description="Student's message")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="Agent's response")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(default="healthy", description="Service status")
