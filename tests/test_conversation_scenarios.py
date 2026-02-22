"""Advanced conversation scenarios for TBBot.

This module tests multi-turn conversations and edge cases
using the Scenario framework's autopilot and script features.
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
        last_message = input.messages[-1]["content"]
        response = self.agent.process_message(last_message)
        return response


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_greeting_then_question_flow():
    """Test a natural conversation flow: greeting followed by questions."""
    result = await scenario.run(
        name="greeting then question",
        description="""
            A student first greets the bot, then asks a technical question.
            The agent should respond to the greeting but not to the technical question
            (since it only handles greetings currently).
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        script=[
            # User greets
            scenario.user("Hello!"),
            # Agent should respond with greeting
            scenario.agent(),
            lambda state: check_greeting_response(state),
            
            # User asks a question
            scenario.user("What is an AI agent?"),
            # Agent should not respond (empty response)
            scenario.agent(),
            lambda state: check_empty_response(state),
            
            scenario.succeed(),
        ],
        set_id="conversation-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_multiple_greetings():
    """Test handling of multiple greetings in one conversation."""
    result = await scenario.run(
        name="multiple greetings",
        description="""
            A student greets the bot multiple times during the conversation.
            The agent should respond to each greeting consistently.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should respond to each greeting",
                    "Agent should maintain consistent greeting message",
                    "Agent should not get confused by repeated greetings",
                ]
            ),
        ],
        max_turns=8,
        set_id="conversation-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_greeting_with_extra_text():
    """Test greetings embedded in longer messages."""
    result = await scenario.run(
        name="greeting with context",
        description="""
            A student sends messages that contain greetings along with other text,
            like "Hello, I have a question about agents" or "Hi there, can you help me?"
            The agent should still detect and respond to the greeting.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should detect greetings even when mixed with other text",
                    "Agent should respond with its standard greeting",
                ]
            ),
        ],
        max_turns=4,
        set_id="conversation-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_empty_message_handling():
    """Test agent behavior with edge case inputs."""
    result = await scenario.run(
        name="edge case inputs",
        description="""
            Test how the agent handles unusual inputs like empty messages,
            very long messages, or messages with special characters.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        script=[
            # Test with a greeting
            scenario.user("hi"),
            scenario.agent(),
            lambda state: check_greeting_response(state),
            
            # Test with special characters
            scenario.user("!@#$%"),
            scenario.agent(),
            lambda state: check_empty_response(state),
            
            scenario.succeed(),
        ],
        set_id="conversation-scenarios",
    )
    
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_autopilot_conversation():
    """Test a full conversation on autopilot with judge evaluation."""
    result = await scenario.run(
        name="autopilot greeting conversation",
        description="""
            A student interacts with TBBot naturally, starting with a greeting
            and potentially asking follow-up questions. The agent should handle
            greetings appropriately and not respond to non-greeting messages.
        """,
        agents=[
            GreetingAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should respond appropriately to greetings",
                    "Agent should introduce itself as TBBot",
                    "Agent should not respond to non-greeting messages",
                    "Agent should maintain consistent behavior throughout",
                ]
            ),
        ],
        max_turns=6,
        set_id="conversation-scenarios",
    )
    
    assert result.success


# Helper functions for assertions

def check_greeting_response(state: scenario.ScenarioState):
    """Verify that the last agent response is a proper greeting."""
    last_message = state.messages[-1]
    assert last_message["role"] == "assistant", "Last message should be from assistant"
    content = last_message["content"]
    assert content != "", "Agent should respond to greeting"
    assert "TBBot" in content, "Greeting should mention TBBot"


def check_empty_response(state: scenario.ScenarioState):
    """Verify that the last agent response is empty."""
    last_message = state.messages[-1]
    assert last_message["role"] == "assistant", "Last message should be from assistant"
    assert last_message["content"] == "", "Agent should not respond to non-greeting"
