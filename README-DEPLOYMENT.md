# GDPR Anonymizer - Deployment Guide

This guide covers deploying the GDPR Anonymizer application using Docker and Kubernetes.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

The GDPR Anonymizer is packaged as a single Docker image containing:
- **Preact UI**: Built static files served from `/`
- **FastAPI Backend**: REST API served from `/api/v1/*`
- **Health Checks**: Liveness (`/health`) and Readiness (`/health/ready`) probes

### Architecture

```
┌─────────────────────────────────────┐
│  Docker Image: gdpr-anonymizer      │
│  ┌───────────────────────────────┐  │
│  │  FastAPI (Port 8000)          │  │
│  │  ├─ Static Files (/)          │  │
│  │  ├─ API (/api/v1/*)           │  │
│  │  └─ Health (/health)          │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Prerequisites

### Required Tools

- **Docker**: 20.10+ (Docker Engine or Docker Desktop)
- **Kubernetes**: 1.24+ (minikube, kind, EKS, GKE, AKS)
- **kubectl**: 1.24+
- **kustomize**: 4.5+ (or use `kubectl apply -k`)
- **bash**: 4.0+
- **curl**: for health checks

### Optional Tools

- **trivy**: Security scanning
- **hadolint**: Dockerfile linting
- **kubeval**: Manifest validation

## Quick Start

### 1. Build Docker Image

```bash
./scripts/build.sh dev
```

### 2. Test Locally

```bash
./scripts/test-local.sh dev
```

Open http://localhost:8000 in your browser.

### 3. Deploy to Kubernetes

```bash
# Create namespace and secrets
kubectl create namespace gdpr-anonymizer-dev

kubectl create secret generic gdpr-anonymizer-secrets \
  --from-literal=anthropic-api-key="YOUR_ANTHROPIC_KEY" \
  --from-literal=openai-api-key="YOUR_OPENAI_KEY" \
  -n gdpr-anonymizer-dev

# Deploy
./scripts/deploy.sh dev
```

### 4. Access Application

```bash
# Port-forward service
kubectl port-forward svc/gdpr-anonymizer 8000:8000 -n gdpr-anonymizer-dev

# Open in browser
open http://localhost:8000
```

## Docker Deployment

### Building the Image

The Dockerfile uses a multi-stage build:

**Stage 1**: Build Preact UI with Node.js
```bash
FROM node:20-alpine AS ui-builder
WORKDIR /ui
COPY client/ ./
RUN npm ci && npm run build
```

**Stage 2**: Python backend + static files
```bash
FROM python:3.11-slim
COPY server/ ./
COPY --from=ui-builder /ui/dist ./static
```

### Build Commands

```bash
# Build with default tag (latest)
./scripts/build.sh

# Build with custom tag
./scripts/build.sh v1.0.0

# Build with registry
export DOCKER_REGISTRY="your-registry.io/your-org"
./scripts/build.sh v1.0.0
```

### Running Locally

```bash
# Run with test script
./scripts/test-local.sh dev

# Or run manually
docker run -d \
  --name gdpr-anonymizer \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY="your-key" \
  -e OPENAI_API_KEY="your-key" \
  gdpr-anonymizer:dev
```

### Testing the Container

```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/health/ready

# UI
curl http://localhost:8000/

# API
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Contact John Smith at john@example.com"}'
```

### Cleanup Docker

```bash
./scripts/cleanup.sh docker
```

## Kubernetes Deployment

### Directory Structure

```
k8s/
├── base/                     # Base manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── dev/                  # Dev environment
│   ├── staging/              # Staging environment
│   └── prod/                 # Production environment
└── ingress.yaml              # Optional Ingress
```

### Deployment Steps

#### 1. Create Namespace

```bash
kubectl create namespace gdpr-anonymizer-dev
```

#### 2. Create Secrets

**IMPORTANT**: Never commit secrets to Git!

```bash
kubectl create secret generic gdpr-anonymizer-secrets \
  --from-literal=anthropic-api-key="YOUR_ANTHROPIC_KEY" \
  --from-literal=openai-api-key="YOUR_OPENAI_KEY" \
  -n gdpr-anonymizer-dev
```

Or use a secret file:

```bash
# Create secret.env file (don't commit!)
cat > secret.env <<EOF
anthropic-api-key=YOUR_ANTHROPIC_KEY
openai-api-key=YOUR_OPENAI_KEY
EOF

kubectl create secret generic gdpr-anonymizer-secrets \
  --from-env-file=secret.env \
  -n gdpr-anonymizer-dev

rm secret.env
```

#### 3. Deploy Application

```bash
# Using deploy script (recommended)
./scripts/deploy.sh dev

# Or manually with kubectl
kubectl apply -k k8s/overlays/dev

# Wait for deployment
kubectl rollout status deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
```

#### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n gdpr-anonymizer-dev

# Check service
kubectl get svc -n gdpr-anonymizer-dev

# View logs
kubectl logs -f deployment/gdpr-anonymizer -n gdpr-anonymizer-dev

# Describe deployment
kubectl describe deployment gdpr-anonymizer -n gdpr-anonymizer-dev
```

#### 5. Access Application

```bash
# Port-forward
kubectl port-forward svc/gdpr-anonymizer 8000:8000 -n gdpr-anonymizer-dev

# Test health
curl http://localhost:8000/health

# Open in browser
open http://localhost:8000
```

### Environment-Specific Deployments

#### Development

```bash
./scripts/deploy.sh dev
```

- Namespace: `gdpr-anonymizer-dev`
- Replicas: 1
- Resources: 100m CPU, 256Mi RAM

#### Staging

```bash
./scripts/deploy.sh staging
```

- Namespace: `gdpr-anonymizer-staging`
- Replicas: 2
- Resources: 200m CPU, 512Mi RAM

#### Production

```bash
./scripts/deploy.sh prod
```

- Namespace: `gdpr-anonymizer-prod`
- Replicas: 3
- Resources: 500m CPU, 1Gi RAM

### Scaling

```bash
# Manual scaling
kubectl scale deployment gdpr-anonymizer --replicas=5 -n gdpr-anonymizer-dev

# Check status
kubectl get pods -n gdpr-anonymizer-dev
```

### Updates and Rollbacks

#### Rolling Update

```bash
# Update image tag in kustomization.yaml
# Then apply
kubectl apply -k k8s/overlays/dev

# Watch rollout
kubectl rollout status deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
```

#### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/gdpr-anonymizer -n gdpr-anonymizer-dev

# Rollback to specific revision
kubectl rollout undo deployment/gdpr-anonymizer --to-revision=2 -n gdpr-anonymizer-dev

# Check rollout history
kubectl rollout history deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
```

### Cleanup Kubernetes

```bash
# Delete all resources
./scripts/cleanup.sh k8s dev

# Or manually
kubectl delete -k k8s/overlays/dev
kubectl delete namespace gdpr-anonymizer-dev
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | `8000` | No |
| `PYTHONUNBUFFERED` | Python output buffering | `1` | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | Optional* |
| `OPENAI_API_KEY` | OpenAI API key | - | Optional* |

*At least one LLM provider API key is required.

### ConfigMap

Configuration is managed via ConfigMap (`k8s/base/configmap.yaml`):

```yaml
data:
  config.yaml: |
    llm_provider: "claude"
    claude:
      model: "claude-3-5-sonnet-20241022"
      max_tokens: 4096
      temperature: 0.0
    # ... more config
```

To update configuration:

```bash
# Edit ConfigMap
kubectl edit configmap gdpr-anonymizer-config -n gdpr-anonymizer-dev

# Restart deployment to apply changes
kubectl rollout restart deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
```

### Resource Limits

Resource limits are defined per environment in overlay patches:

**Dev**: 100m CPU, 256Mi RAM
**Staging**: 200m CPU, 512Mi RAM
**Prod**: 500m CPU, 1Gi RAM

Adjust in `k8s/overlays/{env}/patches/deployment-{env}.yaml`.

## Troubleshooting

### Docker Issues

#### Build Fails

```bash
# Clear Docker cache
docker builder prune

# Build with no cache
docker build --no-cache -t gdpr-anonymizer:dev -f docker/Dockerfile .
```

#### Container Exits Immediately

```bash
# Check logs
docker logs gdpr-anonymizer-test

# Run interactively
docker run -it --rm gdpr-anonymizer:dev /bin/bash

# Check uvicorn installation
docker run --rm gdpr-anonymizer:dev pip list | grep uvicorn
```

#### UI Not Loading

```bash
# Check if static files exist
docker run --rm gdpr-anonymizer:dev ls -la /app/static

# Check main.py configuration
docker run --rm gdpr-anonymizer:dev cat /app/src/anonymization/interfaces/rest/main.py
```

### Kubernetes Issues

#### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n gdpr-anonymizer-dev

# Check pod logs
kubectl logs <pod-name> -n gdpr-anonymizer-dev

# Check resource constraints
kubectl describe node <node-name>
```

#### Health Checks Failing

```bash
# Exec into pod
kubectl exec -it <pod-name> -n gdpr-anonymizer-dev -- /bin/bash

# Test health endpoint from inside pod
curl http://localhost:8000/health

# Check if config mounted
ls -la /app/config/

# Check environment variables
env | grep API_KEY
```

#### ConfigMap Changes Not Applied

```bash
# ConfigMaps don't auto-reload
# Restart deployment to pick up changes
kubectl rollout restart deployment/gdpr-anonymizer -n gdpr-anonymizer-dev

# Or delete pods to force recreation
kubectl delete pods -l app=gdpr-anonymizer -n gdpr-anonymizer-dev
```

#### Service Not Accessible

```bash
# Check service
kubectl get svc gdpr-anonymizer -n gdpr-anonymizer-dev

# Check endpoints
kubectl get endpoints gdpr-anonymizer -n gdpr-anonymizer-dev

# Port-forward to test directly
kubectl port-forward pod/<pod-name> 8000:8000 -n gdpr-anonymizer-dev
```

### Common Errors

#### ImagePullBackOff

```bash
# Check image exists
docker images | grep gdpr-anonymizer

# Check imagePullPolicy
kubectl describe deployment gdpr-anonymizer -n gdpr-anonymizer-dev
```

#### CrashLoopBackOff

```bash
# Check pod logs
kubectl logs <pod-name> -n gdpr-anonymizer-dev

# Check previous container logs
kubectl logs <pod-name> -n gdpr-anonymizer-dev --previous

# Check liveness probe settings
kubectl describe deployment gdpr-anonymizer -n gdpr-anonymizer-dev
```

## Security Best Practices

1. **Secrets Management**
   - Never commit secrets to Git
   - Use external secret management (Vault, AWS Secrets Manager, etc.)
   - Rotate API keys regularly

2. **Image Security**
   - Scan images with trivy: `trivy image gdpr-anonymizer:dev`
   - Use non-root user (already configured)
   - Keep base images updated

3. **Network Security**
   - Use NetworkPolicies to restrict traffic
   - Enable TLS for Ingress
   - Use private container registries

4. **RBAC**
   - Follow principle of least privilege
   - Create service accounts per application
   - Limit namespace access

## Next Steps

- [ ] Set up CI/CD pipeline (GitHub Actions, GitLab CI)
- [ ] Configure Ingress controller
- [ ] Set up TLS/SSL certificates
- [ ] Implement Horizontal Pod Autoscaler (HPA)
- [ ] Add monitoring (Prometheus + Grafana)
- [ ] Set up logging aggregation (ELK, Loki)
- [ ] Implement external secret management

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review Kubernetes events: `kubectl get events -n gdpr-anonymizer-dev --sort-by='.lastTimestamp'`
- Check application logs: `kubectl logs -f deployment/gdpr-anonymizer -n gdpr-anonymizer-dev`

## License

See main README for license information.
