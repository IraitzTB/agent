# TBBot - Educational AI Agent

An educational AI agent that helps students learn how to code AI agents for various purposes.

## Overview

TBBot is a FastAPI-based REST API that provides an interactive Q&A system for teaching AI agent development concepts. Built with Kiro AI-assisted development environment, it demonstrates practical patterns for building educational agents.

## Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Agent Framework**: Agno
- **Testing**: langwatch-scenario (pytest-based)
- **Package Manager**: uv
- **Development**: Kiro IDE with spec-driven workflow

## Quick Start

**New to TBBot?** See [SETUP.md](SETUP.md) for detailed setup instructions.

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment (copy .env.example to .env and add your OpenAI API key)
cp .env.example .env

# 3. Run tests
uv run pytest

# 4. Run the API server
uv run fastapi dev src/tbbot/api.py

# 5. Run scenario tests
uv run pytest tests/test_*_scenarios.py -v
```

## API Endpoints

- `POST /chat` - Send student questions and receive agent responses
- `GET /health` - Health check endpoint

## Project Structure

```
src/tbbot/          # Main application code
  ├── api.py        # FastAPI REST endpoints
  ├── greeting.py   # Agent logic
  └── models.py     # Pydantic models
tests/              # Test suite
.kiro/steering/     # AI assistant guidance
.kiro/specs/        # Feature specifications
```

## Development Workflow

This project follows spec-driven development:
1. Define requirements in `.kiro/specs/{feature}/requirements.md`
2. Create design in `design.md`
3. Break down into tasks in `tasks.md`
4. Implement with Kiro's autonomous coding support

## Testing

Tests use pytest with the Scenario framework for agent simulation testing.

For detailed testing documentation, see [tests/README_SCENARIOS.md](tests/README_SCENARIOS.md).

```bash
# Run all tests
uv run pytest

# Run only scenario tests
uv run pytest tests/test_*_scenarios.py -v

# Run specific test file
uv run pytest tests/test_greeting_scenarios.py

# Run with visible output
uv run pytest -s

# Verbose output
uv run pytest -v
```

### Environment Setup for Tests

Scenario tests require an OpenAI API key:

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=your-key-here
```

## Key Features

- Educational focus on AI agent development
- RESTful API for easy integration
- Comprehensive test coverage
- CORS support for browser-based clients
- Structured error handling and logging
