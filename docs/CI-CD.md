# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for continuous integration and deployment. The pipeline automatically tests, builds, and publishes both Python packages and Docker images.

## Workflow Triggers

The CI/CD pipeline runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- GitHub releases (for publishing)

## Pipeline Jobs

### 1. Test Job
Runs the full test suite to validate code quality.

**Steps:**
- Checkout code
- Set up Python 3.12
- Install uv package manager
- Install dependencies with `uv sync`
- Run pytest with verbose output

**Requirements:**
- `OPENAI_API_KEY` secret must be configured in GitHub repository settings

### 2. Build Package Job
Creates distributable Python packages (wheel and sdist).

**Steps:**
- Checkout code
- Set up Python and uv
- Build package with `uv build`
- Upload artifacts for 30 days

**Outputs:**
- Python wheel (`.whl`)
- Source distribution (`.tar.gz`)

### 3. Build Docker Job
Builds and pushes Docker images to GitHub Container Registry.

**Steps:**
- Checkout code
- Set up Docker Buildx
- Log in to GitHub Container Registry
- Extract metadata and generate tags
- Build and push multi-platform image

**Image Tags:**
- `latest` - Latest commit on default branch
- `main` / `develop` - Branch-specific tags
- `pr-<number>` - Pull request tags
- `v<version>` - Semantic version tags (on release)
- `<branch>-<sha>` - Commit-specific tags

**Registry:** `ghcr.io/<owner>/<repo>`

### 4. Publish Package Job
Publishes to PyPI on GitHub releases (optional).

**Requirements:**
- Only runs on release events
- Requires `PYPI_API_TOKEN` secret

## Setup Instructions

### Required Secrets

Configure these in GitHub repository settings (Settings → Secrets and variables → Actions):

1. **OPENAI_API_KEY** (Required for tests)
   - Get from: https://platform.openai.com/api-keys
   - Used by: Test job

2. **PYPI_API_TOKEN** (Optional, for PyPI publishing)
   - Get from: https://pypi.org/manage/account/token/
   - Used by: Publish package job
   - Only needed if publishing to PyPI

### GitHub Container Registry

Docker images are automatically pushed to GitHub Container Registry (ghcr.io). No additional setup required - uses `GITHUB_TOKEN` automatically.

**Image visibility:**
- Public repositories → Public images
- Private repositories → Private images

To make images public: Repository Settings → Packages → Change visibility

## Using the Docker Image

### Pull the image

```bash
# Latest version
docker pull ghcr.io/<owner>/<repo>:latest

# Specific version
docker pull ghcr.io/<owner>/<repo>:v0.1.0
```

### Run the container

```bash
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  --name tbbot \
  ghcr.io/<owner>/<repo>:latest
```

### Environment variables

- `OPENAI_API_KEY` - Required for agent functionality
- `PORT` - Server port (default: 8000)

### Health check

The container includes a health check that pings `/health` every 30 seconds.

## Local Testing

### Test the workflow locally

```bash
# Run tests
uv run pytest -v

# Build package
uv build

# Build Docker image
docker build -t tbbot:local .

# Run locally
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key tbbot:local
```

### Verify the image

```bash
# Check image size
docker images tbbot:local

# Inspect layers
docker history tbbot:local

# Test health endpoint
curl http://localhost:8000/health
```

## Troubleshooting

### Tests fail with "OPENAI_API_KEY not set"
- Add `OPENAI_API_KEY` secret in GitHub repository settings
- For local testing, create `.env` file with the key

### Docker build fails
- Check Dockerfile syntax
- Verify all required files are present
- Check `.dockerignore` isn't excluding necessary files

### Package build fails
- Verify `pyproject.toml` is valid
- Check that `src/tbbot/` structure is correct
- Ensure version number follows semantic versioning

### Image push fails
- Verify repository has packages write permission
- Check that workflow has `packages: write` permission
- Ensure GitHub Container Registry is enabled

## Best Practices

1. **Branch Protection**: Require CI to pass before merging
2. **Semantic Versioning**: Use proper version tags for releases
3. **Security**: Never commit API keys or secrets
4. **Testing**: Keep test coverage high
5. **Image Size**: Monitor Docker image size (currently ~200MB)

## Monitoring

View workflow runs:
- Repository → Actions tab
- Click on specific workflow run for details
- Download artifacts from successful builds

View published images:
- Repository → Packages
- Click on package for version history and pull commands
