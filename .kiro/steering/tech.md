# Technology Stack

## Development Environment

- IDE: Kiro AI-assisted development environment
- Platform: Linux (bash shell)
- Language: Python
- Dependency Manager: uv
- Agent Framework: Agno (main agent orchestrator)
- Testing Framework: pytest

## Configuration

- MCP integration: Currently disabled (`.vscode/settings.json`)
- Steering rules: Located in `.kiro/steering/`
- Specs: Should be placed in `.kiro/specs/` following spec-driven development

## Common Commands

### Dependency Management (uv)
```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Run Python with uv
uv run python <script.py>
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_agent.py

# Run with verbose output
uv run pytest -v
```

### Development
```bash
# Run the agent
uv run python src/main.py

# Format code (if using ruff/black)
uv run ruff format .

# Lint code (if using ruff)
uv run ruff check .
```

## Development Workflow

- Use spec-driven development: Create requirements.md → design.md → tasks.md
- Leverage Kiro's autonomous coding capabilities
- Follow steering rules for consistency
- Write unit tests using scenario for agent functionalities
