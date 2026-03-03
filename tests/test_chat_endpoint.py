"""Tests for the /chat endpoint aligned with Greeting Agent tasks."""

from fastapi.testclient import TestClient
from src.tbbot.api import app

client = TestClient(app)


def test_chat_endpoint_with_english_greetings():
    """Test /chat endpoint with English greeting messages.
    
    Validates: Task 6.2 - English greeting message processing returns correct response
    Requirements: 1.1, 2.1, 5.1
    """
    english_greetings = ["hello", "hi", "hey"]
    expected_response = "Hi, my name is TBBot. I am here to help you with your questions"
    
    for greeting in english_greetings:
        response = client.post("/chat", json={"message": greeting})
        
        assert response.status_code == 200
        assert "response" in response.json()
        assert response.json()["response"] == expected_response


def test_chat_endpoint_with_catalan_greeting():
    """Test /chat endpoint with Catalan greeting message.
    
    Validates: Task 6.2 - Multilingual greeting processing (Catalan) returns correct response
    Requirements: 1.2, 2.1, 5.2
    """
    response = client.post("/chat", json={"message": "hola"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Hola, el meu nom és TBBot. Estic aquí per ajudar-te amb les teves preguntes"


def test_chat_endpoint_with_basque_greeting():
    """Test /chat endpoint with Basque greeting message.
    
    Validates: Task 6.2 - Multilingual greeting processing (Basque) returns correct response
    Requirements: 1.3, 2.1, 5.3
    """
    response = client.post("/chat", json={"message": "kaixo"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Kaixo, nire izena TBBot da. Hemen nago zure galderekin laguntzeko"


def test_chat_endpoint_with_galician_greeting():
    """Test /chat endpoint with Galician greeting message.
    
    Validates: Task 6.2 - Multilingual greeting processing (Galician) returns correct response
    Requirements: 1.4, 2.1, 5.4
    """
    response = client.post("/chat", json={"message": "ola"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Ola, o meu nome é TBBot. Estou aquí para axudarche coas túas preguntas"


def test_chat_endpoint_case_insensitive_greetings():
    """Test /chat endpoint with case-insensitive greeting detection.
    
    Validates: Task 2.2 - Case-insensitivity for all languages
    Requirements: 1.5, 5.1, 5.2, 5.3, 5.4
    """
    test_cases = [
        ("HELLO", "Hi, my name is TBBot. I am here to help you with your questions"),
        ("HOLA", "Hola, el meu nom és TBBot. Estic aquí per ajudar-te amb les teves preguntes"),
        ("KAIXO", "Kaixo, nire izena TBBot da. Hemen nago zure galderekin laguntzeko"),
        ("OLA", "Ola, o meu nome é TBBot. Estou aquí para axudarche coas túas preguntas"),
    ]
    
    for greeting, expected_response in test_cases:
        response = client.post("/chat", json={"message": greeting})
        
        assert response.status_code == 200
        assert "response" in response.json()
        assert response.json()["response"] == expected_response


def test_chat_endpoint_with_non_greeting():
    """Test /chat endpoint with non-greeting message.
    
    Validates: Task 6.2 - Non-greeting message processing returns empty string
    Requirements: 2.1, 2.6, 2.7
    """
    non_greeting_messages = [
        "what is AI?",
        "help me with coding",
        "explain machine learning",
        "how do I create an agent?"
    ]
    
    for message in non_greeting_messages:
        response = client.post("/chat", json={"message": message})
        
        assert response.status_code == 200
        assert "response" in response.json()
        assert response.json()["response"] == ""


def test_chat_endpoint_language_priority():
    """Test /chat endpoint with multiple greetings to verify language priority.
    
    Validates: Task 2.2 - Language priority when multiple greetings present
    Requirements: 1.1, 1.2, 1.3, 1.4, 5.5
    """
    # Test that first match determines the language (English has priority)
    response = client.post("/chat", json={"message": "hello hola"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Hi, my name is TBBot. I am here to help you with your questions"


def test_chat_endpoint_edge_cases():
    """Test /chat endpoint with edge cases.
    
    Validates: Task 2.2 - Edge cases (empty string, whitespace, mixed content)
    Requirements: 5.1, 5.2
    """
    # Test whitespace-only message
    response = client.post("/chat", json={"message": "   "})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == ""
    
    # Test greeting with extra content
    response = client.post("/chat", json={"message": "hello there, how are you?"})
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Hi, my name is TBBot. I am here to help you with your questions"


def test_chat_endpoint_multiple_sequential_messages():
    """Test /chat endpoint with multiple sequential messages.
    
    Validates: Task 6.2 - Multiple message processing in order
    Requirements: 6.1, 6.2
    """
    # First greeting
    response1 = client.post("/chat", json={"message": "hello"})
    assert response1.status_code == 200
    assert response1.json()["response"] == "Hi, my name is TBBot. I am here to help you with your questions"
    
    # Non-greeting
    response2 = client.post("/chat", json={"message": "what is AI?"})
    assert response2.status_code == 200
    assert response2.json()["response"] == ""
    
    # Another greeting in different language
    response3 = client.post("/chat", json={"message": "hola"})
    assert response3.status_code == 200
    assert response3.json()["response"] == "Hola, el meu nom és TBBot. Estic aquí per ajudar-te amb les teves preguntes"


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
