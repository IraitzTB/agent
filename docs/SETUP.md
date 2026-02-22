# TBBot Setup Guide

Quick guide to get TBBot up and running with scenario tests.

## Prerequisites

- Python 3.12+
- uv package manager
- OpenAI API key (or compatible service)

## Installation Steps

### 1. Install Dependencies

```bash
uv sync
```

This installs all required packages including:
- FastAPI for the REST API
- langwatch-scenario for agent testing
- python-dotenv for environment management

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional - for OpenAI-compatible services
# OPENAI_API_BASE=https://api.openai.com/v1

# Optional - for test visualization
# LANGWATCH_API_KEY=your-langwatch-key
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### 3. Verify Installation

Run the existing unit tests (non-scenario):

```bash
uv run pytest tests/test_greeting_detection.py -v
```

### 4. Run Scenario Tests

Run all scenario tests:

```bash
uv run pytest tests/test_*_scenarios.py -v
```

Run specific scenario test file:

```bash
uv run pytest tests/test_greeting_scenarios.py -v
```

Run with visible output (useful for debugging):

```bash
uv run pytest tests/test_greeting_scenarios.py -s
```

## Running the API Server

Start the development server:

```bash
uv run fastapi dev src/tbbot/api.py
```

The API will be available at: http://localhost:8000

Test the endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

## Project Structure

```
.
├── src/tbbot/           # Main application code
│   ├── api.py          # FastAPI endpoints
│   ├── greeting.py     # Agent logic
│   ├── models.py       # Pydantic models
│   └── config.py       # Environment configuration
├── tests/              # Test suite
│   ├── test_*_scenarios.py  # Scenario-based tests
│   └── test_*.py            # Unit tests
├── .env.example        # Environment template
└── pyproject.toml      # Project configuration
```

## Troubleshooting

### Module Not Found Error

If you see `ModuleNotFoundError: No module named 'tbbot'`:

```bash
uv sync
```

This reinstalls the package in editable mode.

### OpenAI API Key Missing

If scenario tests fail with "OPENAI_API_KEY not found":

1. Make sure you created `.env` from `.env.example`
2. Add your API key to `.env`
3. Verify the file is in the project root

### Model Not Found Error

If you see `Error code: 404 - The model 'gpt-4o-mini' does not exist`:

The tests have been updated to use `gpt-4.1-mini`. If you still see this error, check that you're using the latest test files.

### LangWatch Errors (401 Unauthorized)

These are warnings, not errors. LangWatch is optional for test visualization. To enable it:

1. Get an API key from https://app.langwatch.ai/
2. Add to `.env`: `LANGWATCH_API_KEY=your-key`

## Next Steps

- Read `tests/README_SCENARIOS.md` for detailed scenario testing documentation
- Check out the example scenarios in `tests/test_*_scenarios.py`
- Start building your own agent features!

## Common Commands Reference

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run only scenario tests
uv run pytest tests/test_*_scenarios.py

# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_greeting_scenarios.py::test_basic_greeting_scenario

# Start API server
uv run fastapi dev src/tbbot/api.py

# Run in debug mode (step-by-step)
uv run pytest tests/test_greeting_scenarios.py --debug
```
