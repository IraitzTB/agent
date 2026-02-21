"""Basic tests for the /chat endpoint to verify task 3.2 implementation."""

from fastapi.testclient import TestClient
from src.tbbot.api import app

client = TestClient(app)


def test_chat_endpoint_with_greeting():
    """Test /chat endpoint with a greeting message.
    
    Validates: Requirements 2.1, 2.2, 2.5, 2.7
    """
    response = client.post("/chat", json={"message": "hello"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Hi, my name is TBBot. I am here to help you with your questions"


def test_chat_endpoint_with_non_greeting():
    """Test /chat endpoint with a non-greeting message.
    
    Validates: Requirements 2.1, 2.2, 2.6, 2.7
    """
    response = client.post("/chat", json={"message": "what is AI?"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == ""


def test_chat_endpoint_missing_message_field():
    """Test /chat endpoint with missing message field.
    
    Validates: Requirements 5.2
    """
    response = client.post("/chat", json={})
    
    assert response.status_code == 422


def test_chat_endpoint_empty_message():
    """Test /chat endpoint with empty message string.
    
    Validates: Requirements 5.1
    """
    response = client.post("/chat", json={"message": ""})
    
    assert response.status_code == 422
