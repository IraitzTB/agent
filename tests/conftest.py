"""Pytest configuration and fixtures for TBBot tests.

This module provides shared test configuration and fixtures,
including environment variable validation for scenario tests.
"""

import pytest
import os
from pathlib import Path


def pytest_configure(config):
    """Configure pytest and validate environment for scenario tests."""
    # Register custom markers
    config.addinivalue_line(
        "markers", "agent_test: mark test as an agent scenario test"
    )
    
    # Check if running scenario tests
    test_args = config.args
    running_scenarios = any(
        "scenario" in str(arg) for arg in test_args
    ) if test_args else False
    
    # Validate OpenAI API key for scenario tests
    if running_scenarios and not os.getenv("OPENAI_API_KEY"):
        pytest.exit(
            "\n\n"
            "❌ OPENAI_API_KEY not found!\n\n"
            "Scenario tests require an OpenAI API key.\n"
            "Please create a .env file with your API key:\n\n"
            "  1. Copy .env.example to .env:\n"
            "     cp .env.example .env\n\n"
            "  2. Edit .env and add your OpenAI API key:\n"
            "     OPENAI_API_KEY=your-key-here\n\n"
            "  3. Get your API key from: https://platform.openai.com/api-keys\n\n"
        )


@pytest.fixture(scope="session")
def check_env_config():
    """Fixture to ensure environment is properly configured."""
    from tbbot.config import config
    
    if not config.is_configured():
        pytest.skip("Environment not configured - OPENAI_API_KEY required")
    
    return config
