#!/bin/bash
set -euo pipefail

# Test Docker image locally
# Usage: ./scripts/test-local.sh [tag]

TAG="${1:-latest}"
IMAGE_NAME="gdpr-anonymizer"
PORT="8000"

echo "Testing Docker image: ${IMAGE_NAME}:${TAG}"

# Check if image exists
if ! docker images "${IMAGE_NAME}:${TAG}" | grep -q "${IMAGE_NAME}"; then
  echo "Error: Image ${IMAGE_NAME}:${TAG} not found."
  echo "Build it first: ./scripts/build.sh ${TAG}"
  exit 1
fi

# Stop any existing container
if docker ps -a | grep -q "gdpr-anonymizer-test"; then
  echo "Stopping existing test container..."
  docker stop gdpr-anonymizer-test 2>/dev/null || true
  docker rm gdpr-anonymizer-test 2>/dev/null || true
fi

# Run container
echo "Starting container..."
docker run -d \
  --name gdpr-anonymizer-test \
  -p ${PORT}:8000 \
  -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-test-key}" \
  -e OPENAI_API_KEY="${OPENAI_API_KEY:-test-key}" \
  "${IMAGE_NAME}:${TAG}"

# Wait for container to be ready
echo "Waiting for container to be ready..."
sleep 5

# Test health endpoint
echo ""
echo "Testing health endpoint..."
curl -f http://localhost:${PORT}/health || {
  echo "Health check failed!"
  docker logs gdpr-anonymizer-test
  exit 1
}

# Test readiness endpoint
echo ""
echo "Testing readiness endpoint..."
curl -f http://localhost:${PORT}/health/ready || {
  echo "Readiness check failed!"
  docker logs gdpr-anonymizer-test
  exit 1
}

# Test UI (root path)
echo ""
echo "Testing UI..."
curl -f http://localhost:${PORT}/ > /dev/null || {
  echo "UI serving failed!"
  docker logs gdpr-anonymizer-test
  exit 1
}

echo ""
echo "✅ All tests passed!"
echo ""
echo "Container is running at http://localhost:${PORT}"
echo "Open in browser: http://localhost:${PORT}"
echo ""
echo "To view logs: docker logs -f gdpr-anonymizer-test"
echo "To stop: docker stop gdpr-anonymizer-test"
echo "To clean up: ./scripts/cleanup.sh"
