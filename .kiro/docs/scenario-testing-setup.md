# Scenario Testing Setup - Summary

This document summarizes the scenario testing implementation for TBBot.

## What Was Added

### 1. Environment Configuration
- **python-dotenv** dependency for managing environment variables
- **.env.example** template showing all configuration options
- **src/tbbot/config.py** module for loading and validating configuration
- **.gitignore** updated to exclude `.env` files

### 2. Scenario Test Files
Three comprehensive test suites using the Scenario framework:

- **tests/test_greeting_scenarios.py** - Basic greeting functionality
  - Basic greeting recognition
  - Greeting variations (hi, hello, hey)
  - Non-greeting message handling
  - Case-insensitive detection

- **tests/test_conversation_scenarios.py** - Multi-turn conversations
  - Greeting followed by questions
  - Multiple greetings in one session
  - Greetings embedded in longer messages
  - Edge cases and autopilot mode

- **tests/test_api_scenarios.py** - API endpoint testing
  - FastAPI /chat endpoint scenarios
  - Multiple sequential requests
  - Error handling validation
  - Concurrent user simulation

### 3. Test Configuration
- **tests/conftest.py** - Pytest configuration with environment validation
- **pyproject.toml** updated with:
  - Correct package name (`tbbot`)
  - Build system configuration
  - Pytest settings (pythonpath, asyncio mode)

### 4. Documentation
- **docs/README_SCENARIOS.md** - Comprehensive scenario testing guide
- **SETUP.md** - Quick setup guide for new developers
- **README.md** updated with testing instructions

## Key Features

### Environment Management
```python
# Automatic .env loading
from tbbot.config import config

# Access configuration
api_key = config.OPENAI_API_KEY
api_base = config.OPENAI_API_BASE  # Optional
```

### Scenario Testing Patterns

**Autopilot Mode** - Let the user simulator generate messages:
```python
result = await scenario.run(
    name="test name",
    description="what to test",
    agents=[
        YourAgent(),
        scenario.UserSimulatorAgent(),
        scenario.JudgeAgent(criteria=[...]),
    ],
)
```

**Scripted Mode** - Full control over conversation:
```python
result = await scenario.run(
    name="test name",
    agents=[...],
    script=[
        scenario.user("Hello!"),
        scenario.agent(),
        lambda state: check_response(state),
        scenario.succeed(),
    ],
)
```

## Configuration Options

### Required
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional
- `OPENAI_API_BASE` - Custom API endpoint (for Azure, local LLMs, etc.)
- `LANGWATCH_API_KEY` - For test visualization at app.langwatch.ai
- `SCENARIO_BATCH_RUN_ID` - Group test runs
- `SCENARIO_CACHE_KEY` - Make tests deterministic

## Running Tests

```bash
# Setup
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run all scenario tests
uv run pytest tests/test_*_scenarios.py -v

# Run specific test file
uv run pytest tests/test_greeting_scenarios.py -v

# Debug mode (step-by-step)
uv run pytest tests/test_greeting_scenarios.py --debug

# With visible output
uv run pytest tests/test_greeting_scenarios.py -s
```

## Test Results

The scenario tests validate:
- ✅ Greeting detection across multiple formats
- ✅ Case-insensitive matching
- ✅ Non-greeting message handling
- ✅ Multi-turn conversation flows
- ✅ API endpoint behavior
- ✅ Error handling
- ✅ Concurrent request handling

## Integration with CI/CD

Set environment variables in your CI pipeline:

```yaml
# GitHub Actions example
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  SCENARIO_BATCH_RUN_ID: ${{ github.run_id }}
```

## Next Steps

1. Add more scenario tests for new features
2. Enable LangWatch for visual debugging
3. Set up CI/CD with scenario tests
4. Create scenarios for edge cases
5. Add performance benchmarking scenarios

## Resources

- [Scenario Documentation](https://scenario.langwatch.ai)
- [LangWatch Platform](https://app.langwatch.ai)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [docs/README_SCENARIOS.md](../../docs/README_SCENARIOS.md) - Detailed guide
