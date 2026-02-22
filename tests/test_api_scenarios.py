"""Scenario tests for TBBot API endpoints.

This module tests the FastAPI endpoints using scenario simulations
to ensure the API behaves correctly under various conditions.
"""

import pytest
import scenario
from fastapi.testclient import TestClient
from tbbot.api import app
from tbbot.config import config

# Load environment variables and configure scenario
scenario.configure(default_model="openai/gpt-5.2")


class APIAgentAdapter(scenario.AgentAdapter):
    """Adapter to test TBBot through its FastAPI endpoints."""
    
    def __init__(self):
        self.client = TestClient(app)
    
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        """Send message through the /chat API endpoint."""
        last_message = input.messages[-1]["content"]
        
        # Call the API
        response = self.client.post(
            "/chat",
            json={"message": last_message}
        )
        
        # Return the response content
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_api_greeting_scenario():
    """Test greeting functionality through the API."""
    result = await scenario.run(
        name="API greeting",
        description="""
            A student sends a greeting through the /chat API endpoint.
            The API should return a proper greeting response.
        """,
        agents=[
            APIAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "API should return a greeting response",
                    "Response should introduce TBBot",
                    "Response should be friendly and welcoming",
                ]
            ),
        ],
        set_id="api-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_api_multiple_requests():
    """Test multiple API requests in sequence."""
    result = await scenario.run(
        name="API multiple requests",
        description="""
            A student makes multiple requests to the API:
            first a greeting, then a question, then another greeting.
            The API should handle each request independently and correctly.
        """,
        agents=[
            APIAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        script=[
            # First greeting
            scenario.user("Hello!"),
            scenario.agent(),
            lambda state: check_api_greeting(state),
            
            # Non-greeting message
            scenario.user("What is machine learning?"),
            scenario.agent(),
            lambda state: check_api_empty(state),
            
            # Another greeting
            scenario.user("Hi again!"),
            scenario.agent(),
            lambda state: check_api_greeting(state),
            
            scenario.succeed(),
        ],
        set_id="api-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_api_error_handling():
    """Test API behavior with various input types."""
    result = await scenario.run(
        name="API input validation",
        description="""
            Test the API with different types of inputs to ensure
            it handles them gracefully without crashing.
        """,
        agents=[
            APIAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "API should handle all inputs without errors",
                    "API should respond appropriately to greetings",
                    "API should not crash on unusual inputs",
                ]
            ),
        ],
        max_turns=6,
        set_id="api-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_api_concurrent_behavior():
    """Test API behavior simulating concurrent users."""
    result = await scenario.run(
        name="API concurrent users",
        description="""
            Simulate multiple students using the API simultaneously.
            Each should get appropriate responses independent of others.
        """,
        agents=[
            APIAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "API should handle requests independently",
                    "Each greeting should get a proper response",
                    "No cross-contamination between requests",
                ]
            ),
        ],
        max_turns=8,
        set_id="api-scenarios",
    )
    
    assert result.success


# Helper functions

def check_api_greeting(state: scenario.ScenarioState):
    """Verify API returned a greeting response."""
    last_message = state.messages[-1]
    assert last_message["role"] == "assistant"
    content = last_message["content"]
    assert content != "", "API should return greeting response"
    assert "TBBot" in content, "Greeting should mention TBBot"
    assert not content.startswith("Error:"), "API should not return error"


def check_api_empty(state: scenario.ScenarioState):
    """Verify API returned empty response for non-greeting."""
    last_message = state.messages[-1]
    assert last_message["role"] == "assistant"
    content = last_message["content"]
    assert content == "", "API should return empty for non-greeting"
