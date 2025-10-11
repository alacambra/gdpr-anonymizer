# Iteration Package 6: Kubernetes Deployment & Containerization

## Document Control

**Version**: 1.0
**Date**: 2025-10-10
**Status**: Active
**Dependencies**: Iteration 5 (Complete - Preact UI + Server repackaging)
**Target**: DevOps engineer / Backend developer with Kubernetes experience

---

## 1. Iteration Overview

### 1.1 Purpose

Implement production-ready containerization and Kubernetes deployment for the GDPR Anonymizer application:

1. Create multi-stage Dockerfile that builds both UI and server
2. Configure FastAPI to serve the built UI static files
3. Create comprehensive Kubernetes manifests for deployment
4. Provide deployment automation scripts
5. Implement health checks and monitoring readiness

This iteration makes the application production-ready for Kubernetes environments while maintaining local development workflows.

### 1.2 Business Value

- Production deployment capability
- Scalable infrastructure for handling multiple users
- Container-based deployment for consistency across environments
- Cloud-native architecture supporting HA and auto-scaling
- Simplified deployment process for operations teams
- Foundation for CI/CD pipelines

### 1.3 Success Criteria

✅ Single Docker image contains both UI (built) and server (Python)
✅ FastAPI serves UI static files at root path `/`
✅ API endpoints remain accessible at `/api/v1/*`
✅ Kubernetes deployment manifest supports multiple replicas
✅ Health checks (liveness/readiness probes) configured
✅ ConfigMap and Secret management for configuration
✅ Build and deployment scripts provided
✅ Image size optimized (<500MB final image)

---

## 2. Requirements Implemented

This iteration implements the following requirements:

### From Architectural Requirements (REQ-A-090)

**REQ-A-090** (Partial): Web API + Web UI deployment
- **Scope in this iteration**: Containerization and K8s deployment
- **Out of scope**: Database storage, WebSockets, multi-tenancy

### From Architectural Requirements (REQ-A-096)

**REQ-A-096**: The system SHALL scale
- Multiple replica support in Kubernetes
- Horizontal scaling via K8s deployment
- Resource limits and requests defined

### From Architectural Requirements (REQ-A-097)

**REQ-A-097**: The system SHALL be reliable
- Health check endpoints
- Liveness and readiness probes
- Graceful shutdown handling
- Rolling update strategy

### New Deployment Requirements

**REQ-D-001**: The system SHALL be packaged as a single Docker image
- Multi-stage build: Stage 1 (Node.js for UI), Stage 2 (Python for server + static files)
- Final image based on `python:3.11-slim`
- UI built during Docker build (not at runtime)
- Final image size <500MB

**REQ-D-002**: The UI SHALL be served by FastAPI
- Static files served from `/` (root path)
- SPA routing support (fallback to index.html)
- API endpoints at `/api/v1/*` remain accessible
- Static file caching headers configured

**REQ-D-003**: The system SHALL provide health check endpoints
- `/health` - basic liveness probe (service is running)
- `/health/ready` - readiness probe (dependencies available, e.g., LLM provider reachable)
- Response format: JSON with status and details

**REQ-D-004**: Kubernetes manifests SHALL support production deployment
- Deployment with configurable replicas (default: 2)
- Service (ClusterIP) for internal access
- Optional Ingress for external access
- ConfigMap for non-sensitive configuration
- Secret for API keys and sensitive data

**REQ-D-005**: Configuration SHALL be externalized
- LLM provider settings via ConfigMap
- API keys via Secret
- Environment-specific overrides via Kustomize
- Config file mounted from ConfigMap

**REQ-D-006**: The system SHALL support multiple environments
- Kustomize overlays for dev/staging/prod
- Environment-specific resource limits
- Environment-specific replica counts
- Environment-specific configuration

---

## 3. Architecture & Design

### 3.1 Container Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Docker Image: gdpr-anonymizer:latest                   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  FastAPI Server (Port 8000)                     │   │
│  │  ┌──────────────┐         ┌─────────────────┐  │   │
│  │  │   Static     │         │   API Endpoints │  │   │
│  │  │   Files      │         │   /api/v1/*     │  │   │
│  │  │   Serving    │         │                 │  │   │
│  │  │   / (root)   │         │ /health         │  │   │
│  │  │              │         │ /health/ready   │  │   │
│  │  └──────────────┘         └─────────────────┘  │   │
│  │                                                  │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │  Anonymization Service                   │  │   │
│  │  │  - Domain logic                          │  │   │
│  │  │  - LLM adapters (Claude, OpenAI, Ollama) │  │   │
│  │  │  - Agent orchestration                   │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  Built UI Files: /app/static/                           │
│  Server Code: /app/src/anonymization/                   │
│  Config: /app/config/config.yaml                        │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Kubernetes Architecture

```
┌───────────────────────────────────────────────────────────┐
│  Kubernetes Namespace: gdpr-anonymizer                    │
│                                                             │
│  ┌────────────┐         ┌──────────────────────────────┐ │
│  │  Ingress   │────────▶│  Service: gdpr-anonymizer    │ │
│  │  (optional)│         │  Type: ClusterIP             │ │
│  │            │         │  Port: 8000                  │ │
│  └────────────┘         └──────────────┬───────────────┘ │
│                                          │                 │
│                                          ▼                 │
│                         ┌────────────────────────────────┐│
│                         │  Deployment: gdpr-anonymizer   ││
│                         │  Replicas: 2 (configurable)    ││
│                         │                                ││
│                         │  ┌───────────┐  ┌───────────┐ ││
│                         │  │  Pod 1    │  │  Pod 2    │ ││
│                         │  │  App      │  │  App      │ ││
│                         │  └───────────┘  └───────────┘ ││
│                         └────────────────────────────────┘│
│                                 ▲         ▲                │
│                                 │         │                │
│  ┌──────────────────┐          │         │                │
│  │  ConfigMap       │──────────┘         │                │
│  │  - config.yaml   │                    │                │
│  │  - env vars      │                    │                │
│  └──────────────────┘                    │                │
│                                           │                │
│  ┌──────────────────┐                    │                │
│  │  Secret          │────────────────────┘                │
│  │  - ANTHROPIC_KEY │                                     │
│  │  - OPENAI_KEY    │                                     │
│  └──────────────────┘                                     │
└───────────────────────────────────────────────────────────┘
```

### 3.3 Directory Structure

```
gdpr-anonymizer/
├── client/                      # Preact UI (from Iteration 5)
│   ├── src/
│   ├── dist/                    # Built files (created during Docker build)
│   ├── package.json
│   └── vite.config.ts
│
├── server/                      # Python backend (from Iteration 5)
│   ├── src/anonymization/
│   ├── config/
│   │   └── config.yaml
│   ├── requirements.txt
│   └── run_api.py
│
├── docker/                      # NEW - Docker configuration
│   ├── Dockerfile               # Multi-stage Dockerfile
│   └── .dockerignore            # Files to exclude from build context
│
├── k8s/                         # NEW - Kubernetes manifests
│   ├── base/                    # Base manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   └── kustomization.yaml
│   ├── overlays/
│   │   ├── dev/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   ├── staging/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   └── prod/
│   │       ├── kustomization.yaml
│   │       └── patches/
│   └── ingress.yaml             # Optional Ingress resource
│
├── scripts/                     # NEW - Deployment scripts
│   ├── build.sh                 # Build Docker image
│   ├── deploy.sh                # Deploy to Kubernetes
│   ├── test-local.sh            # Test Docker image locally
│   └── cleanup.sh               # Cleanup K8s resources
│
└── README-DEPLOYMENT.md         # NEW - Deployment documentation
```

---

## 4. Interface Specifications

### 4.1 Dockerfile (Multi-Stage Build)

**Purpose**: Build both UI and server in a single optimized image.

**Key Requirements**:
- Stage 1: Node.js builder for client UI
- Stage 2: Python image with server + static files
- Non-root user for security
- Health check command included
- Environment variables configurable

**File**: `docker/Dockerfile`

```dockerfile
# Stage 1: Build Preact UI
FROM node:20-alpine AS ui-builder

WORKDIR /ui

# Copy UI package files
COPY client/package*.json ./
RUN npm ci --only=production

# Copy UI source code
COPY client/ ./

# Build UI
RUN npm run build
# Output: /ui/dist/

# Stage 2: Python backend + built UI
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY server/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy server source code
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
```

### 4.2 FastAPI Static File Configuration

**Purpose**: Serve UI static files from FastAPI.

**File**: `server/src/anonymization/interfaces/rest/main.py` (modifications)

```python
"""FastAPI application - Main entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .routers import anonymization, health

# Create FastAPI application
app = FastAPI(
    title="GDPR Anonymizer API",
    description="Production-ready text anonymization system",
    version="0.5.0",
    docs_url="/api/docs",      # Move docs to /api/docs
    redoc_url="/api/redoc"     # Move redoc to /api/redoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router)
app.include_router(anonymization.router)

# Serve static files (UI)
static_dir = Path("/app/static")
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.get("/")
    async def serve_spa():
        """Serve the SPA index.html for the root path."""
        return FileResponse(static_dir / "index.html")

    @app.get("/{full_path:path}")
    async def serve_spa_routes(full_path: str):
        """Catch-all route to serve SPA for client-side routing."""
        # Exclude API routes
        if full_path.startswith("api/"):
            return {"error": "Not found"}

        # Check if file exists
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # Fallback to index.html for SPA routing
        return FileResponse(static_dir / "index.html")
```

### 4.3 Health Check Endpoints

**Purpose**: Support Kubernetes liveness and readiness probes.

**File**: `server/src/anonymization/interfaces/rest/routers/health.py` (enhancements)

```python
"""Health check endpoints for Kubernetes probes."""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    details: Dict[str, Any] = {}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Basic health check - liveness probe.

    Returns 200 if service is running.
    Used by Kubernetes liveness probe.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="0.5.0"
    )


@router.get("/health/ready", response_model=HealthResponse)
async def readiness_check():
    """
    Readiness check - readiness probe.

    Returns 200 if service is ready to accept traffic.
    Checks:
    - Configuration loaded
    - LLM provider connectivity (optional - may be slow)

    Used by Kubernetes readiness probe.
    """
    details = {
        "config_loaded": True,  # Check if config.yaml loaded
        "dependencies": {
            "llm_provider": "unknown"  # Could check LLM availability
        }
    }

    # TODO: Add actual checks for:
    # - Config file existence
    # - Environment variables set
    # - (Optional) LLM provider reachability

    return HealthResponse(
        status="ready",
        timestamp=datetime.utcnow().isoformat(),
        version="0.5.0",
        details=details
    )
```

### 4.4 Kubernetes Deployment Manifest

**File**: `k8s/base/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gdpr-anonymizer
  labels:
    app: gdpr-anonymizer
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gdpr-anonymizer
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: gdpr-anonymizer
        version: v1
    spec:
      containers:
      - name: gdpr-anonymizer
        image: gdpr-anonymizer:latest  # Replace with actual registry/image:tag
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP

        env:
        - name: PORT
          value: "8000"
        - name: PYTHONUNBUFFERED
          value: "1"
        # LLM Provider API Keys from Secret
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: gdpr-anonymizer-secrets
              key: anthropic-api-key
              optional: true
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gdpr-anonymizer-secrets
              key: openai-api-key
              optional: true

        # Mount config from ConfigMap
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true

        # Resource limits
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi

        # Liveness probe - is the service running?
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe - is the service ready to accept traffic?
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]

      volumes:
      - name: config
        configMap:
          name: gdpr-anonymizer-config

      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
```

### 4.5 Kubernetes Service Manifest

**File**: `k8s/base/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gdpr-anonymizer
  labels:
    app: gdpr-anonymizer
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: gdpr-anonymizer
```

### 4.6 Kubernetes ConfigMap

**File**: `k8s/base/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gdpr-anonymizer-config
  labels:
    app: gdpr-anonymizer
data:
  config.yaml: |
    # LLM Provider Configuration
    llm_provider: "claude"  # claude, openai, or ollama

    claude:
      model: "claude-3-5-sonnet-20241022"
      max_tokens: 4096
      temperature: 0.0

    openai:
      model: "gpt-4"
      max_tokens: 4096
      temperature: 0.0

    ollama:
      model: "llama2"
      base_url: "http://localhost:11434"

    # Anonymization Settings
    anonymization:
      max_iterations: 3
      validation_threshold: 0.8
      risk_threshold: 0.7

    # Logging
    logging:
      level: "INFO"
      format: "json"
```

### 4.7 Kubernetes Secret (Template)

**File**: `k8s/base/secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gdpr-anonymizer-secrets
  labels:
    app: gdpr-anonymizer
type: Opaque
stringData:
  # Base64 encoded values (or use stringData for plain text)
  # IMPORTANT: Replace with actual values or use external secret management
  anthropic-api-key: "REPLACE_WITH_ACTUAL_KEY"
  openai-api-key: "REPLACE_WITH_ACTUAL_KEY"
```

**Note**: In production, use external secret management (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) instead of committing secrets to Git.

### 4.8 Kustomization (Base)

**File**: `k8s/base/kustomization.yaml`

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: gdpr-anonymizer

resources:
- deployment.yaml
- service.yaml
- configmap.yaml
- secret.yaml

commonLabels:
  app: gdpr-anonymizer
  managed-by: kustomize

images:
- name: gdpr-anonymizer
  newName: gdpr-anonymizer
  newTag: latest
```

### 4.9 Environment Overlays

**Dev Overlay** (`k8s/overlays/dev/kustomization.yaml`):

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: gdpr-anonymizer-dev

bases:
- ../../base

patchesStrategicMerge:
- patches/deployment-dev.yaml

images:
- name: gdpr-anonymizer
  newTag: dev

commonLabels:
  environment: dev
```

**Prod Overlay** (`k8s/overlays/prod/kustomization.yaml`):

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: gdpr-anonymizer-prod

bases:
- ../../base

patchesStrategicMerge:
- patches/deployment-prod.yaml

images:
- name: gdpr-anonymizer
  newTag: v1.0.0

replicas:
- name: gdpr-anonymizer
  count: 3

commonLabels:
  environment: prod
```

---

## 5. Behavioral Requirements

### 5.1 Docker Build Process

**Step 1: Build UI (Stage 1)**
- Node.js 20 Alpine base image
- Install UI dependencies (`npm ci`)
- Build Preact UI (`npm run build`)
- Output: `/ui/dist/` directory with static files

**Step 2: Build Server Image (Stage 2)**
- Python 3.11 slim base image
- Install system dependencies (gcc, g++, curl)
- Install Python dependencies from requirements.txt
- Copy server source code
- Copy built UI from Stage 1 to `/app/static`
- Create non-root user
- Configure health check
- Set entrypoint to uvicorn

**Step 3: Tag and Push**
- Tag image with version and environment
- Push to container registry (Docker Hub, ECR, GCR, ACR)

### 5.2 Kubernetes Deployment Flow

**Step 1: Prepare Secrets**
- Create namespace: `kubectl create namespace gdpr-anonymizer`
- Create secret with actual API keys (not committed to Git)
- Verify secret created: `kubectl get secrets -n gdpr-anonymizer`

**Step 2: Deploy with Kustomize**
- Choose environment: dev, staging, or prod
- Apply manifests: `kubectl apply -k k8s/overlays/dev`
- Verify deployment: `kubectl get deployments -n gdpr-anonymizer`
- Check pods: `kubectl get pods -n gdpr-anonymizer`

**Step 3: Verify Health**
- Check pod logs: `kubectl logs -f <pod-name> -n gdpr-anonymizer`
- Port-forward: `kubectl port-forward svc/gdpr-anonymizer 8000:8000 -n gdpr-anonymizer`
- Test health: `curl http://localhost:8000/health`
- Test readiness: `curl http://localhost:8000/health/ready`
- Test UI: `curl http://localhost:8000/`
- Test API: `curl -X POST http://localhost:8000/api/v1/anonymize -H "Content-Type: application/json" -d '{"text":"Test"}'`

**Step 4: Monitor**
- Watch pods: `kubectl get pods -n gdpr-anonymizer -w`
- Check events: `kubectl get events -n gdpr-anonymizer --sort-by='.lastTimestamp'`
- View logs: `kubectl logs -f deployment/gdpr-anonymizer -n gdpr-anonymizer`

### 5.3 Scaling Behavior

**Manual Scaling**:
```bash
kubectl scale deployment gdpr-anonymizer --replicas=5 -n gdpr-anonymizer
```

**Auto-scaling** (future iteration):
- Horizontal Pod Autoscaler (HPA) based on CPU/memory
- Custom metrics (requests per second)

### 5.4 Update Strategy

**Rolling Update**:
- Max surge: 1 (one extra pod during update)
- Max unavailable: 0 (no downtime)
- Health checks ensure smooth transition
- Old pods terminated only when new pods ready

**Rollback**:
```bash
kubectl rollout undo deployment/gdpr-anonymizer -n gdpr-anonymizer
```

---

## 6. Quality Criteria

### 6.1 Docker Image Quality

✅ Image size <500MB (optimized layers)
✅ Non-root user configured
✅ Health check included
✅ Multi-stage build reduces final size
✅ No unnecessary files in image (.dockerignore)
✅ Security scanning passes (no critical vulnerabilities)
✅ Minimal base image (Alpine/Slim variants)

### 6.2 Kubernetes Manifest Quality

✅ All manifests valid YAML (lint with `kubeval` or `kustomize build`)
✅ Resource limits defined for all containers
✅ Probes configured (liveness + readiness)
✅ Security context configured (non-root, read-only filesystem where possible)
✅ Labels and selectors consistent
✅ Namespace specified
✅ Secrets not committed to Git

### 6.3 Deployment Quality

✅ Zero-downtime deployments (rolling update)
✅ Health checks prevent traffic to unhealthy pods
✅ Graceful shutdown (preStop hook)
✅ Configuration externalized (ConfigMap/Secret)
✅ Environment-specific overlays work
✅ Rollback capability tested

---

## 7. Implementation Guidance

### 7.1 Setup Steps

**Prerequisites**:
- Docker installed (20.10+)
- Kubernetes cluster (local: minikube/kind, cloud: EKS/GKE/AKS)
- kubectl installed and configured
- kustomize installed (or use `kubectl apply -k`)

**Step 0: Verify Current State**
```bash
# Ensure Iteration 5 is complete
cd /Users/albert/git/gdpr-anonymizer
ls client/dist/  # Should exist after `cd client && npm run build`
ls server/src/   # Should exist

# If client/dist doesn't exist, build it:
cd client
npm install
npm run build
cd ..
```

**Step 1: Create Docker Configuration** (1 hour)
```bash
# Create docker directory
mkdir -p docker

# Create Dockerfile (see Section 4.1)
# Create .dockerignore

# Test build locally
cd docker
docker build -t gdpr-anonymizer:dev -f Dockerfile ..
docker images | grep gdpr-anonymizer
```

**Step 2: Update FastAPI for Static Files** (30 min)
```bash
# Modify server/src/anonymization/interfaces/rest/main.py
# Add static file serving (see Section 4.2)
# Update health.py with readiness probe (see Section 4.3)
```

**Step 3: Test Docker Image Locally** (30 min)
```bash
# Run container
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY="your-key" \
  gdpr-anonymizer:dev

# Test in browser
open http://localhost:8000        # Should show UI
open http://localhost:8000/health # Should return {"status":"healthy"}

# Test API
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Contact John Smith at john@example.com"}'
```

**Step 4: Create Kubernetes Manifests** (2 hours)
```bash
# Create k8s directory structure
mkdir -p k8s/base k8s/overlays/{dev,staging,prod}

# Create base manifests (see Section 4.4-4.8)
# Create overlay patches

# Validate with kustomize
kustomize build k8s/overlays/dev
```

**Step 5: Deploy to Kubernetes** (1 hour)
```bash
# Create namespace
kubectl create namespace gdpr-anonymizer-dev

# Create secret with actual API keys
kubectl create secret generic gdpr-anonymizer-secrets \
  --from-literal=anthropic-api-key="your-actual-key" \
  --from-literal=openai-api-key="your-actual-key" \
  -n gdpr-anonymizer-dev

# Apply manifests
kubectl apply -k k8s/overlays/dev

# Verify deployment
kubectl get all -n gdpr-anonymizer-dev
kubectl logs -f deployment/gdpr-anonymizer -n gdpr-anonymizer-dev

# Port-forward for testing
kubectl port-forward svc/gdpr-anonymizer 8000:8000 -n gdpr-anonymizer-dev

# Test
open http://localhost:8000
```

**Step 6: Create Deployment Scripts** (1 hour)
```bash
# Create scripts directory
mkdir -p scripts

# Create build.sh, deploy.sh, test-local.sh, cleanup.sh
# (see Section 8 for script examples)
chmod +x scripts/*.sh
```

### 7.2 Development Order

**Phase 1: Containerization** (2 hours)
1. Create Dockerfile (multi-stage)
2. Create .dockerignore
3. Build Docker image
4. Test locally
5. Optimize image size

**Phase 2: FastAPI Static Files** (1 hour)
1. Modify main.py to serve static files
2. Update health endpoints
3. Test routes (/, /api/*, /health)
4. Rebuild Docker image

**Phase 3: Kubernetes Base Manifests** (2 hours)
1. Create deployment.yaml
2. Create service.yaml
3. Create configmap.yaml
4. Create secret.yaml (template)
5. Create kustomization.yaml
6. Test with `kustomize build`

**Phase 4: Environment Overlays** (1 hour)
1. Create dev overlay
2. Create staging overlay
3. Create prod overlay
4. Test each overlay

**Phase 5: Deployment Scripts** (1 hour)
1. Create build.sh
2. Create deploy.sh
3. Create test-local.sh
4. Create cleanup.sh
5. Test all scripts

**Phase 6: Documentation** (1 hour)
1. Create README-DEPLOYMENT.md
2. Document build process
3. Document deployment process
4. Document troubleshooting
5. Add diagrams

**Total Estimated Time**: 8 hours

---

## 8. Deployment Scripts

### 8.1 Build Script

**File**: `scripts/build.sh`

```bash
#!/bin/bash
set -euo pipefail

# Build Docker image for GDPR Anonymizer
# Usage: ./scripts/build.sh [tag]

TAG="${1:-latest}"
IMAGE_NAME="gdpr-anonymizer"
REGISTRY="${DOCKER_REGISTRY:-}"  # Set via env var if using registry

echo "Building Docker image: ${IMAGE_NAME}:${TAG}"

# Build UI first (optional - already done in Dockerfile)
echo "Building UI..."
cd client
npm install
npm run build
cd ..

# Build Docker image
echo "Building Docker image..."
docker build \
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
```

### 8.2 Deploy Script

**File**: `scripts/deploy.sh`

```bash
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
```

### 8.3 Local Test Script

**File**: `scripts/test-local.sh`

```bash
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
```

### 8.4 Cleanup Script

**File**: `scripts/cleanup.sh`

```bash
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
```

---

## 9. Scope Boundaries

### 9.1 IN SCOPE

✅ Multi-stage Dockerfile (Node.js + Python)
✅ FastAPI serving static UI files
✅ Health check endpoints (/health, /health/ready)
✅ Kubernetes base manifests (Deployment, Service, ConfigMap, Secret)
✅ Kustomize overlays for dev/staging/prod
✅ Resource limits and requests
✅ Liveness and readiness probes
✅ Rolling update strategy
✅ Non-root user in container
✅ .dockerignore for build optimization
✅ Deployment scripts (build, deploy, test, cleanup)
✅ Basic deployment documentation
✅ ConfigMap for configuration
✅ Secret for API keys (template)

### 9.2 OUT OF SCOPE

❌ Container registry setup (Docker Hub, ECR, GCR, ACR)
❌ CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins)
❌ Ingress controller configuration (nginx, traefik)
❌ TLS/SSL certificate management
❌ Horizontal Pod Autoscaler (HPA)
❌ Persistent storage (databases)
❌ Service mesh (Istio, Linkerd)
❌ Observability (Prometheus, Grafana, Jaeger)
❌ External secret management (Vault, AWS Secrets Manager)
❌ Multi-region deployment
❌ Disaster recovery procedures
❌ Load testing and capacity planning

---

## 10. Acceptance Criteria

### 10.1 Docker Acceptance

1. ✅ Dockerfile builds successfully without errors
2. ✅ Final image size <500MB
3. ✅ UI files present in `/app/static/`
4. ✅ Server code present in `/app/src/`
5. ✅ Non-root user configured (UID 1000)
6. ✅ Health check command works
7. ✅ Container starts successfully
8. ✅ UI accessible at `http://localhost:8000/`
9. ✅ API accessible at `http://localhost:8000/api/v1/*`
10. ✅ Health endpoints return 200 OK

### 10.2 Kubernetes Acceptance

1. ✅ All manifests are valid YAML
2. ✅ `kustomize build` succeeds for all overlays
3. ✅ Deployment creates 2 pods (default replicas)
4. ✅ Pods reach Ready state within 2 minutes
5. ✅ Service routes traffic to pods
6. ✅ Liveness probe prevents restart loops
7. ✅ Readiness probe controls traffic routing
8. ✅ ConfigMap mounted at `/app/config/`
9. ✅ Secret environment variables accessible
10. ✅ Rolling update works without downtime
11. ✅ Rollback works correctly
12. ✅ Resource limits enforced

### 10.3 Functional Acceptance

1. ✅ UI loads successfully via Kubernetes service
2. ✅ API endpoints functional via Kubernetes service
3. ✅ Health checks pass
4. ✅ Configuration loaded from ConfigMap
5. ✅ API keys loaded from Secret
6. ✅ Application logs visible via `kubectl logs`
7. ✅ Scaling works (`kubectl scale`)
8. ✅ Graceful shutdown works (no dropped requests)
9. ✅ Zero-downtime deployment verified

### 10.4 Documentation Acceptance

1. ✅ README-DEPLOYMENT.md created
2. ✅ Build instructions documented
3. ✅ Deployment instructions documented
4. ✅ Troubleshooting guide included
5. ✅ Scripts have usage documentation
6. ✅ Environment variables documented
7. ✅ Architecture diagrams included

---

## 11. Deliverables

### 11.1 Docker Files

- `docker/Dockerfile` - Multi-stage build
- `docker/.dockerignore` - Build context exclusions

### 11.2 Kubernetes Manifests

**Base**:
- `k8s/base/deployment.yaml`
- `k8s/base/service.yaml`
- `k8s/base/configmap.yaml`
- `k8s/base/secret.yaml` (template)
- `k8s/base/kustomization.yaml`

**Overlays**:
- `k8s/overlays/dev/kustomization.yaml`
- `k8s/overlays/dev/patches/deployment-dev.yaml`
- `k8s/overlays/staging/kustomization.yaml`
- `k8s/overlays/staging/patches/deployment-staging.yaml`
- `k8s/overlays/prod/kustomization.yaml`
- `k8s/overlays/prod/patches/deployment-prod.yaml`

**Optional**:
- `k8s/ingress.yaml` - Ingress resource (example)

### 11.3 Code Modifications

- `server/src/anonymization/interfaces/rest/main.py` - Static file serving
- `server/src/anonymization/interfaces/rest/routers/health.py` - Readiness probe

### 11.4 Deployment Scripts

- `scripts/build.sh` - Build Docker image
- `scripts/deploy.sh` - Deploy to Kubernetes
- `scripts/test-local.sh` - Test Docker image locally
- `scripts/cleanup.sh` - Cleanup resources

### 11.5 Documentation

- `README-DEPLOYMENT.md` - Complete deployment guide
- Inline comments in manifests
- Usage documentation in scripts

---

## 12. Dependencies

### 12.1 Technical Dependencies

**Required**:
- Docker 20.10+ (Docker Engine or Docker Desktop)
- Kubernetes 1.24+ (minikube, kind, EKS, GKE, AKS)
- kubectl 1.24+
- kustomize 4.5+ (or use `kubectl apply -k`)
- bash 4.0+ (for scripts)
- curl (for health checks)

**Optional**:
- trivy (security scanning)
- hadolint (Dockerfile linting)
- kubeval (manifest validation)

**Cloud Provider Tools** (if using cloud):
- AWS: aws-cli, eksctl
- GCP: gcloud, gke-gcloud-auth-plugin
- Azure: az cli

### 12.2 Iteration Dependencies

**Depends On**:
- Iteration 5: Complete (Preact UI + server repackaging)
- Iteration 1-4: Complete (working API)

**Blocks**:
- None (can be developed independently)

**Enables** (Future Iterations):
- CI/CD pipeline setup
- Production monitoring
- Auto-scaling implementation
- Multi-environment deployments

---

## 13. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Docker image too large (>500MB) | MEDIUM | MEDIUM | Multi-stage build, Alpine base, optimize layers, use .dockerignore |
| Static file serving conflicts with API routes | LOW | HIGH | Clear route precedence: API first, then static, then fallback to index.html |
| Health checks fail in Kubernetes | MEDIUM | HIGH | Test probes locally first, adjust timeouts, add detailed logging |
| Secret management complexity | HIGH | HIGH | Provide clear documentation, use Secret template, suggest external secret store |
| Configuration override complexity | MEDIUM | MEDIUM | Use Kustomize overlays, test each environment separately |
| Deployment downtime | LOW | HIGH | Rolling update with maxUnavailable:0, readiness probes, test rollback |
| Resource limits too restrictive | MEDIUM | MEDIUM | Start conservative, monitor, adjust based on actual usage |
| Build time too long | MEDIUM | LOW | Layer caching, parallel builds in CI/CD, optimize npm install |

---

## 14. Testing Strategy

### 14.1 Local Docker Testing

**Test Case 1: Image Build**
```bash
./scripts/build.sh dev
docker images | grep gdpr-anonymizer
# Expected: Image size <500MB
```

**Test Case 2: Container Startup**
```bash
./scripts/test-local.sh dev
# Expected: All health checks pass
```

**Test Case 3: UI Access**
```bash
curl http://localhost:8000/
# Expected: HTML response with UI
```

**Test Case 4: API Access**
```bash
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Test John Smith"}'
# Expected: JSON response with anonymized text
```

**Test Case 5: Health Endpoints**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy",...}

curl http://localhost:8000/health/ready
# Expected: {"status":"ready",...}
```

### 14.2 Kubernetes Testing

**Test Case 1: Manifest Validation**
```bash
kustomize build k8s/overlays/dev | kubeval
# Expected: All manifests valid
```

**Test Case 2: Deployment**
```bash
./scripts/deploy.sh dev
kubectl get pods -n gdpr-anonymizer-dev
# Expected: 2 pods Running, 2/2 Ready
```

**Test Case 3: Service Connectivity**
```bash
kubectl port-forward svc/gdpr-anonymizer 8000:8000 -n gdpr-anonymizer-dev
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

**Test Case 4: Scaling**
```bash
kubectl scale deployment gdpr-anonymizer --replicas=3 -n gdpr-anonymizer-dev
kubectl get pods -n gdpr-anonymizer-dev
# Expected: 3 pods Running
```

**Test Case 5: Rolling Update**
```bash
# Update image tag in kustomization
kubectl apply -k k8s/overlays/dev
kubectl rollout status deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
# Expected: Deployment rolled out successfully, no downtime
```

**Test Case 6: Rollback**
```bash
kubectl rollout undo deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
kubectl rollout status deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
# Expected: Rollback successful
```

**Test Case 7: Pod Restart (Liveness Probe)**
```bash
# Simulate crash: exec into pod and kill process
kubectl exec -it <pod-name> -n gdpr-anonymizer-dev -- kill 1
# Expected: Pod restarts automatically
```

**Test Case 8: ConfigMap Update**
```bash
# Update ConfigMap
kubectl edit configmap gdpr-anonymizer-config -n gdpr-anonymizer-dev
# Restart deployment to pick up changes
kubectl rollout restart deployment/gdpr-anonymizer -n gdpr-anonymizer-dev
# Expected: New config loaded
```

### 14.3 Integration Testing

**Test Case 1: End-to-End Flow**
1. Deploy to Kubernetes (dev)
2. Port-forward service
3. Open UI in browser
4. Submit text for anonymization
5. Verify anonymized result
6. Check API logs

**Test Case 2: Multi-Environment**
1. Deploy to dev: `./scripts/deploy.sh dev`
2. Deploy to staging: `./scripts/deploy.sh staging`
3. Deploy to prod: `./scripts/deploy.sh prod`
4. Verify each environment isolated

---

## 15. Transition to Next Iteration

### 15.1 Foundation for Iteration 7

This iteration establishes:
- ✅ Production-ready containerization
- ✅ Kubernetes deployment manifests
- ✅ Multi-environment support
- ✅ Health check infrastructure
- ✅ Configuration management pattern
- ✅ Deployment automation

**Iteration 7** could build on this by adding:
- CI/CD pipeline (GitHub Actions, GitLab CI)
- Ingress controller setup
- TLS/SSL certificate management
- Horizontal Pod Autoscaler (HPA)
- Monitoring (Prometheus + Grafana)
- Logging aggregation (ELK, Loki)
- External secret management (Vault)
- Multi-region deployment

### 15.2 Open Questions for Iteration 7

1. Which CI/CD platform to use? (GitHub Actions, GitLab CI, Jenkins)
2. Which Ingress controller? (nginx, traefik, AWS ALB)
3. Which monitoring solution? (Prometheus, Datadog, New Relic)
4. Which secret management? (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)
5. HPA metrics: CPU/memory or custom metrics?
6. Database requirement for audit logs/history?

---

## 16. Definition of Done

### 16.1 Docker Complete

- [ ] Dockerfile created with multi-stage build
- [ ] .dockerignore created
- [ ] Image builds successfully
- [ ] Image size <500MB
- [ ] Non-root user configured
- [ ] Health check works
- [ ] Container runs locally
- [ ] UI accessible at /
- [ ] API accessible at /api/v1/*
- [ ] No critical security vulnerabilities (trivy scan)

### 16.2 FastAPI Static Files Complete

- [ ] main.py updated to serve static files
- [ ] health.py updated with readiness probe
- [ ] Routes tested (/, /api/*, /health)
- [ ] SPA routing works (fallback to index.html)
- [ ] API routes not affected by static file serving

### 16.3 Kubernetes Manifests Complete

- [ ] Base manifests created (deployment, service, configmap, secret)
- [ ] Overlays created (dev, staging, prod)
- [ ] All manifests valid (kubeval)
- [ ] Kustomize builds successfully
- [ ] Resource limits defined
- [ ] Probes configured
- [ ] Security context configured
- [ ] Labels and selectors consistent

### 16.4 Deployment Scripts Complete

- [ ] build.sh works correctly
- [ ] deploy.sh works for all environments
- [ ] test-local.sh passes all checks
- [ ] cleanup.sh removes resources
- [ ] All scripts have usage documentation
- [ ] Scripts tested on macOS and Linux

### 16.5 Testing Complete

- [ ] Local Docker tests pass
- [ ] Kubernetes deployment tests pass
- [ ] Health checks verified
- [ ] Scaling tested
- [ ] Rolling update tested
- [ ] Rollback tested
- [ ] End-to-end flow verified

### 16.6 Documentation Complete

- [ ] README-DEPLOYMENT.md created
- [ ] Build process documented
- [ ] Deployment process documented
- [ ] Troubleshooting guide included
- [ ] Architecture diagrams included
- [ ] Environment variable reference
- [ ] Secret management documented

---

## 17. Handoff Checklist

### 17.1 Architect Validation

- [ ] Architecture follows cloud-native best practices
- [ ] Multi-stage build optimized
- [ ] Kubernetes manifests follow conventions
- [ ] Security considerations addressed
- [ ] Scalability requirements met
- [ ] Health check strategy appropriate

### 17.2 Tech Lead Review

- [ ] Requirements clear and actionable
- [ ] Sufficient detail to begin implementation
- [ ] Development order makes sense
- [ ] Estimated time realistic (8 hours)
- [ ] Dependencies clearly stated
- [ ] Testing strategy comprehensive

### 17.3 DevOps Handoff

- [ ] Document delivered
- [ ] Example manifests provided
- [ ] Scripts provided and tested
- [ ] Troubleshooting guide available
- [ ] Questions channel established
- [ ] Architect available for clarifications

---

## 18. Revision History

| Version | Date       | Changes                    | Author    |
|---------|------------|----------------------------|-----------|
| 1.0     | 2025-10-10 | Initial iteration package  | Architect |

---

## Appendix A: .dockerignore

**File**: `docker/.dockerignore`

```
# Git
.git
.gitignore
.github

# Python
**/__pycache__
**/*.pyc
**/*.pyo
**/*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
eggs
.eggs
parts
bin
var
sdist
develop-eggs
.installed.cfg
lib
lib64
**/.pytest_cache
**/.mypy_cache
**/.coverage
htmlcov

# Virtual environments
venv
venv_python3
env
ENV

# Node
**/node_modules
**/.npm
**/.yarn

# IDE
.vscode
.idea
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs

# Testing
.pytest_cache
.coverage
htmlcov
.tox

# Documentation
docs
*.md
!README.md

# Examples
examples
executions

# Kubernetes (don't include in image)
k8s

# CI/CD
.github
.gitlab-ci.yml
.circleci

# Other
.env
.env.*
!.env.example
```

---

## Appendix B: Troubleshooting Guide

### Issue 1: Docker Build Fails

**Symptom**: `docker build` fails during npm install or pip install

**Solution**:
```bash
# Check Docker version
docker --version

# Clear Docker cache
docker builder prune

# Build with no cache
docker build --no-cache -t gdpr-anonymizer:dev -f docker/Dockerfile .
```

### Issue 2: Container Exits Immediately

**Symptom**: Container starts but exits immediately

**Solution**:
```bash
# Check logs
docker logs gdpr-anonymizer-test

# Run interactively to debug
docker run -it --rm gdpr-anonymizer:dev /bin/bash

# Check if uvicorn is installed
docker run --rm gdpr-anonymizer:dev pip list | grep uvicorn
```

### Issue 3: UI Not Loading

**Symptom**: API works but UI shows 404

**Solution**:
```bash
# Check if static files exist in image
docker run --rm gdpr-anonymizer:dev ls -la /app/static

# Check main.py static file configuration
docker run --rm gdpr-anonymizer:dev cat /app/src/anonymization/interfaces/rest/main.py
```

### Issue 4: Kubernetes Pods Not Starting

**Symptom**: Pods stuck in Pending or CrashLoopBackOff

**Solution**:
```bash
# Check pod events
kubectl describe pod <pod-name> -n gdpr-anonymizer-dev

# Check pod logs
kubectl logs <pod-name> -n gdpr-anonymizer-dev

# Check resource constraints
kubectl get nodes
kubectl describe node <node-name>
```

### Issue 5: Health Checks Failing

**Symptom**: Readiness probe fails, pods not ready

**Solution**:
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

### Issue 6: ConfigMap Changes Not Applied

**Symptom**: ConfigMap updated but pods use old config

**Solution**:
```bash
# ConfigMaps don't auto-reload in pods
# Restart deployment to pick up changes
kubectl rollout restart deployment/gdpr-anonymizer -n gdpr-anonymizer-dev

# Or delete pods to force recreation
kubectl delete pods -l app=gdpr-anonymizer -n gdpr-anonymizer-dev
```

---

**END OF ITERATION PACKAGE 6**

**Status**: READY FOR IMPLEMENTATION
**Estimated Effort**: 8 hours
**Next Iteration**: CI/CD Pipeline, Monitoring, and Observability
