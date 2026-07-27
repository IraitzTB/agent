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
    """Test API behavior with various input types.

    Uses an explicit script (rather than an LLM user simulator + judge) so a
    real greeting is actually sent (the autopilot variant had the simulator
    send a single message *listing* weird inputs to try, which is not a
    greeting, so the API correctly returned "" and the judge failed it).
    """
    result = await scenario.run(
        name="API input validation",
        description="""
            Test the API with different types of inputs to ensure
            it handles them gracefully without crashing.
        """,
        agents=[
            APIAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        script=[
            # A genuine greeting must still get a proper greeting response.
            scenario.user("hello"),
            scenario.agent(),
            lambda state: check_api_greeting(state),
            # Unusual / hostile inputs must not crash the API (no "Error:" prefix).
            scenario.user("!@#$%^&*()_+-="),
            scenario.agent(),
            lambda state: check_api_no_error(state),
            scenario.user("' OR 1=1; DROP TABLE users;--"),
            scenario.agent(),
            lambda state: check_api_no_error(state),
            scenario.user("<script>alert(1)</script>"),
            scenario.agent(),
            lambda state: check_api_no_error(state),
            scenario.user("../../../../etc/passwd"),
            scenario.agent(),
            lambda state: check_api_no_error(state),
            scenario.succeed(),
        ],
        set_id="api-scenarios",
    )

    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_api_concurrent_behavior():
    """Test API behavior simulating concurrent users.

    Uses an explicit script (rather than an LLM user simulator + judge) so
    greetings are actually sent. The /chat endpoint is stateless, so
    independence is shown by interleaving greetings with a non-greeting:
    the non-greeting still returns "" (no state leaks from prior greetings)
    and each greeting gets its own correct response.
    """
    result = await scenario.run(
        name="API concurrent users",
        description="""
            Simulate multiple students using the API simultaneously.
            Each should get appropriate responses independent of others.
        """,
        agents=[
            APIAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        script=[
            # User 1 greets -> proper greeting response.
            scenario.user("hello"),
            scenario.agent(),
            lambda state: check_api_greeting(state),
            # User 2 sends a non-greeting -> empty, independent of user 1.
            scenario.user("what is machine learning?"),
            scenario.agent(),
            lambda state: check_api_empty(state),
            # User 3 greets in another language -> own correct response.
            scenario.user("hola"),
            scenario.agent(),
            lambda state: check_api_greeting(state),
            # User 4 greets again -> still a proper, independent response.
            scenario.user("hey"),
            scenario.agent(),
            lambda state: check_api_greeting(state),
            scenario.succeed(),
        ],
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


def check_api_no_error(state: scenario.ScenarioState):
    """Verify the API handled an unusual input gracefully (no error/crash).

    The APIAgentAdapter returns an ``"Error: <status>"`` string when the
    endpoint responds with a non-200 status; a 200 with an empty (non-greeting)
    body is the expected graceful outcome here.
    """
    last_message = state.messages[-1]
    assert last_message["role"] == "assistant"
    content = last_message["content"]
    assert not content.startswith("Error:"), (
        f"API should not return an error for unusual input, got: {content!r}"
    )
