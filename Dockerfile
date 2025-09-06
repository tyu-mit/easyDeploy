# easyDeploy Docker image for development and testing
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY src/ src/
COPY templates/ templates/
COPY state/ state/

# Install Python dependencies
RUN uv sync --frozen

# Create non-root user
RUN useradd --create-home --shell /bin/bash easydeploy && \
    chown -R easydeploy:easydeploy /app

USER easydeploy

# Set up environment
ENV PATH="/app/.venv/bin:$PATH"

# Default command
CMD ["easydeploy", "--help"]
