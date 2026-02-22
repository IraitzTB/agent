# Troubleshooting Guide

Common issues and solutions when running TBBot tests.

## Issue: Authentication Error (401)

**Error:**
```
Error code: 401 - {'detail': "Couldn't authenticate. Reason: Unable authenticate"}
```

**Cause:** You have `OPENAI_API_BASE` set to a non-OpenAI service (like Nebius) but using an OpenAI API key.

**Solution:**
1. Comment out `OPENAI_API_BASE` in your `.env` file to use standard OpenAI:
   ```bash
   # OPENAI_API_BASE="https://api.tokenfactory.nebius.com/v1/"
   ```

2. Or, if using Nebius, use the correct API key for that service and update the model in test files.

## Issue: Module Not Found - 'tbbot'

**Error:**
```
ModuleNotFoundError: No module named 'tbbot'
```

**Cause:** Package not installed in editable mode.

**Solution:**
```bash
uv sync
```

## Issue: Module Not Found - 'pandas'

**Error:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Cause:** Missing optional dependency for JudgeAgent.

**Solution:**
```bash
uv add pandas
```

## Issue: Model Not Found (404)

**Error:**
```
Error code: 404 - {'detail': 'The model `gpt-4o-mini` does not exist.'}
```

**Cause:** Using incorrect model name.

**Solution:** Tests have been updated to use `gpt-4.1-mini`. If you still see this, check your test files use the correct model name.

## Issue: OPENAI_API_KEY Not Found

**Error:**
```
❌ OPENAI_API_KEY not found!
```

**Cause:** No `.env` file or missing API key.

**Solution:**
1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

## Issue: Test Fails Due to Insufficient Coverage

**Example:**
```
case insensitive greeting - FAILED
Reasoning: only lowercase "hello" is evidenced, so ability to respond 
regardless of capitalization cannot be confirmed
```

**Cause:** The user simulator didn't generate messages that fully test the criteria.

**Solutions:**
1. Use a scripted test instead of autopilot mode
2. Increase `max_turns` to give more opportunities
3. Make the description more explicit about what to test
4. Use `scenario.user("HELLO")` to force specific inputs

## Issue: LangWatch Errors (401 Unauthorized)

**Error:**
```
ERROR [SCENARIO_RUN_STARTED] Event POST failed: status=401, 
reason=Unauthorized, error={"error":"Unauthorized","message":"Missing API key"}
```

**Cause:** LangWatch API key not configured (this is optional).

**Impact:** These are warnings, not errors. Tests will still run.

**Solution (optional):**
1. Get an API key from https://app.langwatch.ai/
2. Add to `.env`:
   ```bash
   LANGWATCH_API_KEY=your-key-here
   ```

## Using Alternative OpenAI-Compatible Services

If you want to use services like Nebius, Azure OpenAI, or local LLMs:

### 1. Configure the API Base

In `.env`:
```bash
OPENAI_API_BASE="https://your-service-url/v1/"
```

### 2. Update Model Names

Different services use different model names. Update in your test files:

```python
# For Nebius
scenario.configure(default_model="openai/meta-llama/Meta-Llama-3.1-70B-Instruct")

# For Azure OpenAI
scenario.configure(default_model="azure/your-deployment-name")
```

### 3. Verify API Key Format

Different services have different API key formats:
- OpenAI: `sk-proj-...`
- Nebius: `v1.CmMKHHN0...`
- Azure: Uses Azure AD tokens or keys

## Running Tests Successfully

### Quick Test
```bash
# Test one simple scenario
uv run pytest tests/test_greeting_scenarios.py::test_non_greeting_message -v
```

### Full Test Suite
```bash
# Run all scenario tests
uv run pytest tests/test_*_scenarios.py -v
```

### Debug Mode
```bash
# Step through scenarios interactively
uv run pytest tests/test_greeting_scenarios.py --debug
```

## Verifying Your Setup

Run this checklist:

```bash
# 1. Check .env exists
ls -la .env

# 2. Verify API key is set (should show your key)
grep OPENAI_API_KEY .env

# 3. Check package is installed
uv run python -c "import tbbot; print('✓ tbbot installed')"

# 4. Check pandas is installed
uv run python -c "import pandas; print('✓ pandas installed')"

# 5. Run a simple test
uv run pytest tests/test_greeting_detection.py -v
```

## Getting Help

If you're still stuck:

1. Check the error message carefully
2. Review [SETUP.md](SETUP.md) for initial setup
3. Check [tests/README_SCENARIOS.md](tests/README_SCENARIOS.md) for scenario testing details
4. Look at the working test examples in `tests/test_*_scenarios.py`

## Common Command Reference

```bash
# Reset everything
uv sync
cp .env.example .env
# Edit .env with your API key

# Run tests
uv run pytest tests/test_greeting_scenarios.py -v

# Run with output visible
uv run pytest tests/test_greeting_scenarios.py -s

# Run specific test
uv run pytest tests/test_greeting_scenarios.py::test_basic_greeting_scenario

# Debug mode
uv run pytest tests/test_greeting_scenarios.py --debug
```
