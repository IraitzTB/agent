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

```bash
# Install dependencies
uv sync

# Run the API server
uv run fastapi dev src/tbbot/api.py

# Run tests
uv run scenario
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

Tests use the scenario framework for agent functionality testing:

```bash
# Run all tests
uv run scenario

# Run specific test
uv run scenario tests/test_greeting_agent.py

# Verbose output
uv run scenario -v
```

## Key Features

- Educational focus on AI agent development
- RESTful API for easy integration
- Comprehensive test coverage
- CORS support for browser-based clients
- Structured error handling and logging
