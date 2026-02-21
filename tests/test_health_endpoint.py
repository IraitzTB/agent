"""Tests for the /health endpoint to verify task 3.3 implementation."""

from fastapi.testclient import TestClient
from src.tbbot.api import app

client = TestClient(app)


def test_health_endpoint_returns_200():
    """Test /health endpoint returns 200 status code.
    
    Validates: Requirements 3.1, 3.2
    """
    response = client.get("/health")
    
    assert response.status_code == 200


def test_health_endpoint_returns_correct_structure():
    """Test /health endpoint returns correct JSON structure.
    
    Validates: Requirements 3.3
    """
    response = client.get("/health")
    
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert json_data["status"] == "healthy"
