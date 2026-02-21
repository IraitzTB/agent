"""Tests for error handling in the /chat endpoint.

This test file verifies that the chat endpoint properly handles internal errors,
logs them with appropriate severity, and returns correct error responses.

Validates: Requirements 5.4
"""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.tbbot.api import app

client = TestClient(app)


def test_chat_endpoint_internal_error_returns_500():
    """Test that internal errors in agent processing return 500 status.
    
    Validates: Requirements 5.4
    """
    # Mock the agent to raise an exception
    with patch('src.tbbot.api.agent.process_message') as mock_process:
        mock_process.side_effect = Exception("Simulated internal error")
        
        response = client.post("/chat", json={"message": "hello"})
        
        # Should return 500 status code
        assert response.status_code == 500
        
        # Should return JSON with detail field
        assert "detail" in response.json()
        
        # Should return generic error message (not expose internal details)
        assert response.json()["detail"] == "Internal server error"


def test_chat_endpoint_logs_errors_with_context():
    """Test that errors are logged with appropriate severity and context.
    
    Validates: Requirements 5.4
    """
    # Mock both the agent and the logger
    with patch('src.tbbot.api.agent.process_message') as mock_process, \
         patch('src.tbbot.api.logger') as mock_logger:
        
        mock_process.side_effect = ValueError("Test error")
        
        response = client.post("/chat", json={"message": "test message"})
        
        # Verify error was logged
        assert mock_logger.error.called
        
        # Verify error was logged with ERROR severity (error method)
        call_args = mock_logger.error.call_args
        
        # Check that exc_info=True was passed for stack trace
        assert call_args.kwargs.get('exc_info') is True
        
        # Check that extra context was included
        assert 'extra' in call_args.kwargs
        assert 'message_length' in call_args.kwargs['extra']


def test_chat_endpoint_error_does_not_expose_internal_details():
    """Test that error responses don't expose sensitive internal information.
    
    Validates: Requirements 5.4
    """
    with patch('src.tbbot.api.agent.process_message') as mock_process:
        # Simulate an error with sensitive information
        mock_process.side_effect = Exception("Database connection failed: password=secret123")
        
        response = client.post("/chat", json={"message": "hello"})
        
        # Should return 500
        assert response.status_code == 500
        
        # Should NOT expose the sensitive error message
        response_text = response.text.lower()
        assert "password" not in response_text
        assert "secret" not in response_text
        assert "database" not in response_text
        
        # Should only return generic message
        assert response.json()["detail"] == "Internal server error"
