# Stage 1: Build Preact UI
FROM --platform=$BUILDPLATFORM node:20-alpine AS ui-builder

WORKDIR /ui

# Copy UI package files
COPY client/package*.json ./

# Copy UI source code
COPY client/ ./

# Install dependencies and build UI
# Note: Using npm install instead of npm ci to handle optional dependencies properly
RUN npm install && npm run build
# Output: /ui/dist/

# Stage 2: Python backend + built UI
FROM --platform=$TARGETPLATFORM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip and Poetry (separate layer for better caching)
RUN pip install --no-cache-dir --upgrade pip poetry

# Copy only dependency files first (for better layer caching)
COPY server/pyproject.toml ./
COPY server/poetry.lock* ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install Python dependencies (this layer is cached if pyproject.toml doesn't change)
RUN poetry install --no-interaction --no-ansi --no-root --extras "ollama claude openai"

# Copy server source code (separate layer - changes frequently)
COPY server/src/ ./src/
COPY server/config/ ./config/

# Copy built UI from Stage 1
COPY --from=ui-builder /ui/dist ./static

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "src.anonymization.interfaces.rest.main:app", "--host", "0.0.0.0", "--port", "8000"]
