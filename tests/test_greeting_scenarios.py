"""Scenario-based tests for TBBot greeting functionality.

This module uses the Scenario framework to simulate real user interactions
and test the greeting agent's behavior in various scenarios.
"""

import pytest
import scenario
from tbbot.greeting import GreetingAgent
from tbbot.config import config

# Load environment variables and configure scenario
scenario.configure(default_model="openai/gpt-5.2")


class GreetingAgentAdapter(scenario.AgentAdapter):
    """Adapter to integrate GreetingAgent with Scenario framework."""
    
    def __init__(self):
        self.agent = GreetingAgent()
    
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        """Process the last user message through the greeting agent."""
        # Get the last user message
        last_message = input.messages[-1]["content"]
        
        # Process through the agent
        response = self.agent.process_message(last_message)
        
        return response


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_basic_greeting_scenario():
    """Test that agent responds appropriately to a basic greeting."""
    result = await scenario.run(
        name="basic greeting",
        description="""
            A student opens TBBot for the first time and says hello.
            The agent should respond with a friendly greeting introducing itself.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should respond to the greeting",
                    "Agent should introduce itself as TBBot",
                    "Response should be friendly and welcoming",
                ]
            ),
        ],
        set_id="greeting-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_greeting_variations():
    """Test that agent recognizes different greeting formats."""
    result = await scenario.run(
        name="greeting variations",
        description="""
            A student tries different ways of greeting the bot:
            "hi", "hello", "hey there", etc.
            The agent should recognize all common greeting patterns.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should respond to various greeting formats",
                    "Agent should consistently introduce itself",
                    "Agent should not ignore any greeting attempt",
                ]
            ),
        ],
        max_turns=6,
        set_id="greeting-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_non_greeting_message():
    """Test that agent doesn't respond to non-greeting messages."""
    result = await scenario.run(
        name="non-greeting message",
        description="""
            A student sends a technical question without greeting first.
            The agent should not respond with a greeting to non-greeting messages.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        script=[
            scenario.user("What is an AI agent?"),
            scenario.agent(),
            # Check that response is empty for non-greeting
            lambda state: assert_empty_response(state),
            scenario.succeed(),
        ],
        set_id="greeting-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_case_insensitive_greeting():
    """Test that greetings work regardless of case."""
    result = await scenario.run(
        name="case insensitive greeting",
        description="""
            A student types greetings in various cases: "HELLO", "HeLLo", "hello".
            The agent should recognize greetings regardless of capitalization.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should respond to greetings in any case",
                    "Agent should provide consistent greeting response",
                ]
            ),
        ],
        max_turns=4,
        set_id="greeting-scenarios",
    )
    
    assert result.success


def assert_empty_response(state: scenario.ScenarioState):
    """Assert that the last agent response is empty."""
    last_message = state.messages[-1]
    assert last_message["role"] == "assistant"
    assert last_message["content"] == "", "Agent should not respond to non-greeting messages"
