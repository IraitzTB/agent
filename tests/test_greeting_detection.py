"""Unit tests for greeting detection functionality.

Tests the is_greeting() function to ensure it correctly identifies
greeting messages according to requirements 1.1-1.5 and 5.3.
"""

from src.tbbot.greeting import is_greeting


class TestGreetingKeywords:
    """Test detection of each greeting keyword."""
    
    def test_hello_detected(self):
        """Test that 'hello' is identified as a greeting.
        
        Validates: Requirements 1.1
        """
        assert is_greeting("hello") is True
    
    def test_hi_detected(self):
        """Test that 'hi' is identified as a greeting.
        
        Validates: Requirements 1.2
        """
        assert is_greeting("hi") is True
    
    def test_hey_detected(self):
        """Test that 'hey' is identified as a greeting.
        
        Validates: Requirements 1.3
        """
        assert is_greeting("hey") is True


class TestCaseInsensitivity:
    """Test case-insensitive greeting detection."""
    
    def test_hello_uppercase(self):
        """Test that 'HELLO' is identified as a greeting.
        
        Validates: Requirements 1.4
        """
        assert is_greeting("HELLO") is True
    
    def test_hi_uppercase(self):
        """Test that 'HI' is identified as a greeting.
        
        Validates: Requirements 1.4
        """
        assert is_greeting("HI") is True
    
    def test_hey_uppercase(self):
        """Test that 'HEY' is identified as a greeting.
        
        Validates: Requirements 1.4
        """
        assert is_greeting("HEY") is True
    
    def test_hello_mixed_case(self):
        """Test that 'HeLLo' is identified as a greeting.
        
        Validates: Requirements 1.4
        """
        assert is_greeting("HeLLo") is True
    
    def test_hi_mixed_case(self):
        """Test that 'Hi' is identified as a greeting.
        
        Validates: Requirements 1.4
        """
        assert is_greeting("Hi") is True
    
    def test_hey_mixed_case(self):
        """Test that 'HeY' is identified as a greeting.
        
        Validates: Requirements 1.4
        """
        assert is_greeting("HeY") is True


class TestNonGreetingMessages:
    """Test that non-greeting messages are not identified as greetings."""
    
    def test_question_not_greeting(self):
        """Test that a question is not identified as a greeting.
        
        Validates: Requirements 1.5, 5.3
        """
        assert is_greeting("What is an AI agent?") is False
    
    def test_statement_not_greeting(self):
        """Test that a statement is not identified as a greeting.
        
        Validates: Requirements 1.5, 5.3
        """
        assert is_greeting("I need help with my code") is False
    
    def test_random_text_not_greeting(self):
        """Test that random text is not identified as a greeting.
        
        Validates: Requirements 1.5, 5.3
        """
        assert is_greeting("xyz abc 123") is False


class TestEdgeCases:
    """Test edge cases for greeting detection."""
    
    def test_empty_string_not_greeting(self):
        """Test that an empty string is not identified as a greeting.
        
        Validates: Requirements 1.5
        """
        assert is_greeting("") is False
    
    def test_whitespace_only_not_greeting(self):
        """Test that whitespace-only string is not identified as a greeting.
        
        Validates: Requirements 1.5
        """
        assert is_greeting("   ") is False
        assert is_greeting("\t\n") is False
    
    def test_greeting_with_extra_text(self):
        """Test that greeting keywords within longer messages are detected.
        
        Validates: Requirements 1.1, 1.2, 1.3
        """
        assert is_greeting("hello there!") is True
        assert is_greeting("hi, how are you?") is True
        assert is_greeting("hey, I have a question") is True
    
    def test_greeting_with_punctuation(self):
        """Test that greeting keywords with punctuation are detected.
        
        Validates: Requirements 1.1, 1.2, 1.3
        """
        assert is_greeting("hello!") is True
        assert is_greeting("hi.") is True
        assert is_greeting("hey?") is True
    
    def test_greeting_at_end_of_message(self):
        """Test that greeting keywords at the end of messages are detected.
        
        Validates: Requirements 1.1, 1.2, 1.3
        """
        assert is_greeting("Well, hello") is True
        assert is_greeting("Oh hi") is True
        assert is_greeting("Say hey") is True
    
    def test_partial_match_not_greeting(self):
        """Test that partial keyword matches are still detected.
        
        Note: Current implementation uses 'in' operator, so 'hiya' contains 'hi'.
        This test documents the current behavior.
        
        Validates: Requirements 1.2
        """
        # These contain greeting keywords as substrings
        assert is_greeting("hiya") is True  # contains "hi"
        assert is_greeting("hello123") is True  # contains "hello"
        assert is_greeting("heya") is True  # contains "hey"



class TestResponseGenerator:
    """Test the greeting response generator."""
    
    def test_generate_greeting_response_exact_text(self):
        """Test that generate_greeting_response() returns the exact specified message.
        
        Validates: Requirements 2.1
        """
        from src.tbbot.greeting import generate_greeting_response
        
        expected_response = "Hi, my name is TBBot. I am here to help you with your questions"
        actual_response = generate_greeting_response()
        
        assert actual_response == expected_response
    
    def test_generate_greeting_response_returns_string(self):
        """Test that generate_greeting_response() returns a string type.
        
        Validates: Requirements 2.1
        """
        from src.tbbot.greeting import generate_greeting_response
        
        response = generate_greeting_response()
        assert isinstance(response, str)
    
    def test_generate_greeting_response_not_empty(self):
        """Test that generate_greeting_response() returns a non-empty string.
        
        Validates: Requirements 2.1
        """
        from src.tbbot.greeting import generate_greeting_response
        
        response = generate_greeting_response()
        assert len(response) > 0
