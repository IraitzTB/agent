"""Unit tests for GreetingAgent class.

Tests the GreetingAgent class to ensure it correctly initializes,
processes greeting and non-greeting messages, and handles multiple
messages in order according to requirements 3.1, 3.2, 4.1, 2.1, 2.3, 5.1, 5.2.
"""

from src.tbbot.greeting import GreetingAgent


class TestAgentInitialization:
    """Test GreetingAgent initialization."""
    
    def test_agent_initializes_successfully(self):
        """Test that GreetingAgent initializes without errors.
        
        Validates: Requirements 3.1, 3.2
        """
        agent = GreetingAgent()
        assert agent is not None
    
    def test_agent_has_initialized_flag(self):
        """Test that GreetingAgent sets _initialized flag after initialization.
        
        Validates: Requirements 3.2
        """
        agent = GreetingAgent()
        assert hasattr(agent, '_initialized')
        assert agent._initialized is True
    
    def test_agent_has_logger(self):
        """Test that GreetingAgent initializes with a logger.
        
        Validates: Requirements 3.1, 3.3
        """
        agent = GreetingAgent()
        assert hasattr(agent, 'logger')
        assert agent.logger is not None


class TestGreetingMessageProcessing:
    """Test GreetingAgent processing of greeting messages."""
    
    def test_hello_returns_greeting_response(self):
        """Test that 'hello' message returns the correct greeting response.
        
        Validates: Requirements 2.1, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("hello")
        
        expected = "Hi, my name is TBBot. I am here to help you with your questions"
        assert response == expected
    
    def test_hi_returns_greeting_response(self):
        """Test that 'hi' message returns the correct greeting response.
        
        Validates: Requirements 2.1, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("hi")
        
        expected = "Hi, my name is TBBot. I am here to help you with your questions"
        assert response == expected
    
    def test_hey_returns_greeting_response(self):
        """Test that 'hey' message returns the correct greeting response.
        
        Validates: Requirements 2.1, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("hey")
        
        expected = "Hi, my name is TBBot. I am here to help you with your questions"
        assert response == expected
    
    def test_greeting_case_insensitive(self):
        """Test that greeting detection is case-insensitive.
        
        Validates: Requirements 2.1, 5.2
        """
        agent = GreetingAgent()
        
        assert agent.process_message("HELLO") == "Hi, my name is TBBot. I am here to help you with your questions"
        assert agent.process_message("Hi") == "Hi, my name is TBBot. I am here to help you with your questions"
        assert agent.process_message("HeY") == "Hi, my name is TBBot. I am here to help you with your questions"
    
    def test_greeting_with_extra_text(self):
        """Test that greetings within longer messages are processed correctly.
        
        Validates: Requirements 2.1, 5.2
        """
        agent = GreetingAgent()
        
        response = agent.process_message("hello there!")
        expected = "Hi, my name is TBBot. I am here to help you with your questions"
        assert response == expected


class TestNonGreetingMessageProcessing:
    """Test GreetingAgent processing of non-greeting messages."""
    
    def test_question_returns_empty_string(self):
        """Test that a question message returns an empty string.
        
        Validates: Requirements 2.3, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("What is an AI agent?")
        
        assert response == ""
    
    def test_statement_returns_empty_string(self):
        """Test that a statement message returns an empty string.
        
        Validates: Requirements 2.3, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("I need help with my code")
        
        assert response == ""
    
    def test_random_text_returns_empty_string(self):
        """Test that random text returns an empty string.
        
        Validates: Requirements 2.3, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("xyz abc 123")
        
        assert response == ""
    
    def test_empty_string_returns_empty_string(self):
        """Test that an empty string input returns an empty string.
        
        Validates: Requirements 2.3, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("")
        
        assert response == ""


class TestMultipleMessageProcessing:
    """Test GreetingAgent processing of multiple messages in order."""
    
    def test_multiple_greetings_processed_in_order(self):
        """Test that multiple greeting messages are processed in order.
        
        Validates: Requirements 4.1, 2.1, 2.3
        """
        agent = GreetingAgent()
        
        expected = "Hi, my name is TBBot. I am here to help you with your questions"
        
        # Process multiple greetings
        response1 = agent.process_message("hello")
        response2 = agent.process_message("hi")
        response3 = agent.process_message("hey")
        
        # Each should return the greeting response
        assert response1 == expected
        assert response2 == expected
        assert response3 == expected
    
    def test_mixed_messages_processed_in_order(self):
        """Test that mixed greeting and non-greeting messages are processed in order.
        
        Validates: Requirements 4.1, 2.1, 2.3
        """
        agent = GreetingAgent()
        
        expected_greeting = "Hi, my name is TBBot. I am here to help you with your questions"
        
        # Process messages in order
        response1 = agent.process_message("hello")
        response2 = agent.process_message("What is an AI agent?")
        response3 = agent.process_message("hi there")
        response4 = agent.process_message("I need help")
        
        # Verify responses
        assert response1 == expected_greeting
        assert response2 == ""
        assert response3 == expected_greeting
        assert response4 == ""
    
    def test_sequential_non_greetings_processed_in_order(self):
        """Test that multiple non-greeting messages are processed in order.
        
        Validates: Requirements 4.1, 2.3
        """
        agent = GreetingAgent()
        
        # Process multiple non-greetings
        response1 = agent.process_message("What is Python?")
        response2 = agent.process_message("How do I code?")
        response3 = agent.process_message("Tell me about agents")
        
        # Each should return empty string
        assert response1 == ""
        assert response2 == ""
        assert response3 == ""
    
    def test_agent_state_persists_across_messages(self):
        """Test that agent maintains state across multiple message calls.
        
        Validates: Requirements 4.1, 3.2
        """
        agent = GreetingAgent()
        
        # Process several messages
        agent.process_message("hello")
        agent.process_message("What is an AI?")
        agent.process_message("hi")
        
        # Agent should still be initialized
        assert agent._initialized is True
        
        # Agent should still process messages correctly
        response = agent.process_message("hey")
        expected = "Hi, my name is TBBot. I am here to help you with your questions"
        assert response == expected


class TestScenarioFrameworkCompatibility:
    """Test that GreetingAgent is compatible with scenario framework."""
    
    def test_agent_can_be_instantiated_in_test(self):
        """Test that GreetingAgent can be instantiated within a test.
        
        Validates: Requirements 5.1
        """
        agent = GreetingAgent()
        assert agent is not None
    
    def test_agent_process_message_returns_string(self):
        """Test that process_message returns a string type.
        
        Validates: Requirements 5.1, 5.2
        """
        agent = GreetingAgent()
        response = agent.process_message("hello")
        
        assert isinstance(response, str)
    
    def test_agent_accepts_string_input(self):
        """Test that process_message accepts string input.
        
        Validates: Requirements 5.1, 5.2
        """
        agent = GreetingAgent()
        
        # Should not raise any exceptions
        try:
            agent.process_message("test message")
            success = True
        except Exception:
            success = False
        
        assert success is True
