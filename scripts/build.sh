#!/bin/bash
set -euo pipefail

# Build Docker image for GDPR Anonymizer
# Usage: ./scripts/build.sh [tag]

TAG="${1:-latest}"
IMAGE_NAME="gdpr-anonymizer"
REGISTRY="${DOCKER_REGISTRY:-}"  # Set via env var if using registry
PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"  # Default to amd64 for most K8s clusters

echo "Building Docker image: ${IMAGE_NAME}:${TAG}"

# Build UI first (optional - already done in Dockerfile)
echo "Building UI..."
cd client
npm install
npm run build
cd ..

# Build Docker image
echo "Building Docker image for platform: ${PLATFORM}..."
docker build \
  --platform "${PLATFORM}" \
  -t "${IMAGE_NAME}:${TAG}" \
  -f docker/Dockerfile \
  .

# Tag with registry if specified
if [ -n "$REGISTRY" ]; then
  echo "Tagging for registry: ${REGISTRY}/${IMAGE_NAME}:${TAG}"
  docker tag "${IMAGE_NAME}:${TAG}" "${REGISTRY}/${IMAGE_NAME}:${TAG}"
fi

# Display image info
echo ""
echo "Image built successfully!"
docker images | grep "${IMAGE_NAME}"

# Display image size
SIZE=$(docker images "${IMAGE_NAME}:${TAG}" --format "{{.Size}}")
echo ""
echo "Image size: $SIZE"

# Security scan (optional - requires trivy)
if command -v trivy &> /dev/null; then
  echo ""
  echo "Running security scan..."
  trivy image "${IMAGE_NAME}:${TAG}"
fi

echo ""
echo "Build complete!"
echo "To test locally: ./scripts/test-local.sh ${TAG}"
echo "To push: docker push ${REGISTRY}/${IMAGE_NAME}:${TAG}"
