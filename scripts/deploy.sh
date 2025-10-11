#!/bin/bash
set -euo pipefail

# Deploy to Kubernetes
# Usage: ./scripts/deploy.sh [environment]

ENV="${1:-dev}"
NAMESPACE="gdpr-anonymizer-${ENV}"

echo "Deploying to environment: $ENV"
echo "Namespace: $NAMESPACE"

# Validate environment
if [[ ! "$ENV" =~ ^(dev|staging|prod)$ ]]; then
  echo "Error: Invalid environment. Must be dev, staging, or prod."
  exit 1
fi

# Check if namespace exists
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
  echo "Creating namespace: $NAMESPACE"
  kubectl create namespace "$NAMESPACE"
fi

# Check if secrets exist
if ! kubectl get secret gdpr-anonymizer-secrets -n "$NAMESPACE" &> /dev/null; then
  echo ""
  echo "WARNING: Secret 'gdpr-anonymizer-secrets' not found!"
  echo "Create it with:"
  echo "  kubectl create secret generic gdpr-anonymizer-secrets \\"
  echo "    --from-literal=anthropic-api-key=YOUR_KEY \\"
  echo "    --from-literal=openai-api-key=YOUR_KEY \\"
  echo "    -n $NAMESPACE"
  echo ""
  read -p "Continue without secrets? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Apply manifests with kustomize
echo "Applying manifests..."
kubectl apply -k "k8s/overlays/${ENV}"

# Wait for deployment
echo ""
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/gdpr-anonymizer -n "$NAMESPACE" --timeout=5m

# Display status
echo ""
echo "Deployment status:"
kubectl get all -n "$NAMESPACE"

# Display pod logs
echo ""
echo "Recent logs:"
kubectl logs -l app=gdpr-anonymizer -n "$NAMESPACE" --tail=20

echo ""
echo "Deployment complete!"
echo ""
echo "To port-forward: kubectl port-forward svc/gdpr-anonymizer 8000:8000 -n $NAMESPACE"
echo "To view logs: kubectl logs -f deployment/gdpr-anonymizer -n $NAMESPACE"
echo "To scale: kubectl scale deployment gdpr-anonymizer --replicas=3 -n $NAMESPACE"
