# Scenario-Based Testing for TBBot

This directory contains scenario-based tests using the [Scenario framework](https://scenario.langwatch.ai) to simulate real user interactions with TBBot.

## Test Files

### `test_greeting_scenarios.py`
Basic greeting detection and response tests:
- Basic greeting recognition
- Greeting variations (hi, hello, hey)
- Non-greeting message handling
- Case-insensitive greeting detection

### `test_conversation_scenarios.py`
Advanced multi-turn conversation tests:
- Greeting followed by questions
- Multiple greetings in one conversation
- Greetings embedded in longer messages
- Edge case inputs (empty, special characters)
- Autopilot conversation simulation

### `test_api_scenarios.py`
API endpoint testing through scenarios:
- API greeting functionality
- Multiple sequential requests
- Error handling and input validation
- Concurrent user simulation

## Running the Tests

### Run all scenario tests
```bash
uv run pytest tests/test_*_scenarios.py -v
```

### Run specific scenario test file
```bash
uv run pytest tests/test_greeting_scenarios.py -v
```

### Run with output visible (useful for debugging)
```bash
uv run pytest tests/test_greeting_scenarios.py -s
```

### Run in debug mode (step-by-step with intervention)
```bash
uv run pytest tests/test_greeting_scenarios.py -s --debug
```

### Run tests in parallel (requires pytest-asyncio-concurrent)
```bash
# First install the plugin
uv add --dev pytest-asyncio-concurrent

# Then run tests
uv run pytest tests/test_*_scenarios.py -v
```

## Configuration

Scenario tests are configured with:
- **Model**: `openai/gpt-4o-mini` (set in each test file)
- **Set ID**: Groups related scenarios for organization in LangWatch
- **Max Turns**: Limits conversation length (default varies by test)

## Environment Variables

### Required
```bash
export OPENAI_API_KEY="your-api-key"
```

### Optional - LangWatch Visualization
```bash
export LANGWATCH_API_KEY="your-langwatch-key"
```

With LangWatch enabled, you can visualize scenarios in real-time at https://app.langwatch.ai/

### Optional - Batch Tracking
```bash
export SCENARIO_BATCH_RUN_ID="my-test-run-id"
```

## Test Structure

Each scenario test follows this pattern:

```python
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_example():
    result = await scenario.run(
        name="test name",
        description="what the test simulates",
        agents=[
            YourAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[...]),
        ],
        set_id="test-group",
    )
    assert result.success
```

## Key Features

### Autopilot Mode
Tests without a `script` parameter run on autopilot - the user simulator generates messages automatically until success or max_turns is reached.

### Scripted Mode
Tests with a `script` parameter have full control over the conversation flow:
```python
script=[
    scenario.user("Hello!"),
    scenario.agent(),
    lambda state: check_response(state),
    scenario.succeed(),
]
```

### Judge Agent
The Judge Agent evaluates conversations based on criteria:
```python
scenario.JudgeAgent(
    criteria=[
        "Agent should respond to greetings",
        "Agent should introduce itself",
    ]
)
```

## Caching

To make tests deterministic and faster:

```python
# Set cache key globally
scenario.configure(default_model="openai/gpt-4o-mini", cache_key="42")

# Or cache specific functions
@scenario.cache()
def my_llm_call():
    # ...
```

Cache files are stored in `~/.scenario/cache/`

## Debugging Tips

1. Use `-s` flag to see output: `pytest -s`
2. Enable debug mode: `pytest --debug`
3. Check specific assertions with custom functions
4. Use LangWatch for visual debugging
5. Set `verbose=True` in scenario.configure()

## Best Practices

1. Group related tests with the same `set_id`
2. Use descriptive test names and descriptions
3. Keep scenarios focused on specific behaviors
4. Use Judge Agent for complex evaluation criteria
5. Add custom assertion functions for specific checks
6. Use autopilot for exploratory testing
7. Use scripts for precise control and edge cases

## Adding New Scenarios

1. Create a new test file: `test_<feature>_scenarios.py`
2. Import scenario and create an adapter for your agent
3. Write test functions with `@pytest.mark.agent_test` and `@pytest.mark.asyncio`
4. Use descriptive names and clear criteria
5. Group related tests with the same `set_id`

Example:
```python
import pytest
import scenario
from tbbot.greeting import GreetingAgent

scenario.configure(default_model="openai/gpt-4o-mini")

class MyAgentAdapter(scenario.AgentAdapter):
    def __init__(self):
        self.agent = GreetingAgent()
    
    async def call(self, input: scenario.AgentInput):
        return self.agent.process_message(input.messages[-1]["content"])

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_my_scenario():
    result = await scenario.run(
        name="my test",
        description="what this tests",
        agents=[
            MyAgentAdapter(),
            scenario.UserSimulatorAgent(),
        ],
        set_id="my-tests",
    )
    assert result.success
```
