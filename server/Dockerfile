# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY gdpr_anonymizer/ gdpr_anonymizer/
COPY README.md .
COPY LICENSE .

# Install the package in development mode
RUN pip install -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash gdpr_user
RUN chown -R gdpr_user:gdpr_user /app
USER gdpr_user

# Create output directory
RUN mkdir -p /app/output

# Expose port (if needed for future web interface)
EXPOSE 8000

# Default command
CMD ["gdpr-anonymizer", "--help"]