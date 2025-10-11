#!/bin/bash
set -euo pipefail

# Cleanup Kubernetes resources or Docker containers
# Usage: ./scripts/cleanup.sh [k8s|docker] [environment]

TYPE="${1:-docker}"
ENV="${2:-dev}"

if [ "$TYPE" == "docker" ]; then
  echo "Cleaning up Docker resources..."

  # Stop and remove test container
  if docker ps -a | grep -q "gdpr-anonymizer-test"; then
    echo "Stopping test container..."
    docker stop gdpr-anonymizer-test 2>/dev/null || true
    docker rm gdpr-anonymizer-test 2>/dev/null || true
  fi

  # Remove dangling images
  echo "Removing dangling images..."
  docker image prune -f

  echo "Docker cleanup complete!"

elif [ "$TYPE" == "k8s" ]; then
  NAMESPACE="gdpr-anonymizer-${ENV}"

  echo "Cleaning up Kubernetes resources in namespace: $NAMESPACE"

  # Confirm deletion
  read -p "This will delete all resources in $NAMESPACE. Continue? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi

  # Delete resources
  echo "Deleting resources..."
  kubectl delete -k "k8s/overlays/${ENV}" || true

  # Delete namespace
  echo "Deleting namespace..."
  kubectl delete namespace "$NAMESPACE" || true

  echo "Kubernetes cleanup complete!"

else
  echo "Usage: ./scripts/cleanup.sh [k8s|docker] [environment]"
  exit 1
fi
