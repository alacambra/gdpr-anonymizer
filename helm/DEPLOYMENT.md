# Helm Deployment Guide

This guide explains how to deploy the GDPR Anonymizer using Helm to `anonymizer.lacambra.tech`.

## Prerequisites

1. **Kubernetes cluster** with kubectl configured
2. **Helm 3.x** installed
3. **cert-manager** installed for Let's Encrypt certificates
4. **nginx-ingress-controller** installed
5. **API Keys** for your chosen LLM provider (Anthropic/OpenAI)

## Installing Prerequisites

### 1. Install cert-manager (if not already installed)

```bash
# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set installCRDs=true
```

### 2. Create Let's Encrypt ClusterIssuer

Create a file `letsencrypt-prod.yaml`:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # The ACME server URL
    server: https://acme-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: your-email@lacambra.tech  # UPDATE THIS
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
          class: nginx
```

Apply it:

```bash
kubectl apply -f letsencrypt-prod.yaml
```

### 3. Verify cert-manager is running

```bash
kubectl get pods -n cert-manager
```

## Deployment Options

### Option 1: Quick Deployment (Using production values file)

This uses the pre-configured values file with your domain settings:

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  -f ./helm/gdpr-anonymizer/values-production.yaml \
  --set secrets.anthropicApiKey="sk-ant-xxxxx"
```

### Option 2: Command Line Override

Override specific values from the command line:

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host="anonymizer.lacambra.tech" \
  --set ingress.hosts[0].paths[0].path="/" \
  --set ingress.hosts[0].paths[0].pathType="Prefix" \
  --set ingress.tls[0].secretName="gdpr-anonymizer-tls" \
  --set ingress.tls[0].hosts[0]="anonymizer.lacambra.tech" \
  --set secrets.anthropicApiKey="sk-ant-xxxxx"
```

### Option 3: Custom Values File

Create your own `my-production.yaml`:

```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-dev
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: anonymizer.lacambra.tech
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: gdpr-anonymizer-tls
      hosts:
        - anonymizer.lacambra.tech

secrets:
  anthropicApiKey: "your-key-here"  # Or use --set instead

config:
  llmProvider: "claude"
```

Deploy with:

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer -f my-production.yaml
```

## Secure Secret Management

**IMPORTANT**: Never commit API keys to Git. Use one of these methods:

### Method 1: Command Line (Recommended)

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  -f ./helm/gdpr-anonymizer/values-production.yaml \
  --set secrets.anthropicApiKey="$(cat ~/secrets/anthropic-key.txt)"
```

### Method 2: Environment Variable

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"

helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  -f ./helm/gdpr-anonymizer/values-production.yaml \
  --set secrets.anthropicApiKey="$ANTHROPIC_API_KEY"
```

### Method 3: External Secrets (Production Best Practice)

For production, consider using:
- **External Secrets Operator** with AWS Secrets Manager, GCP Secret Manager, or Vault
- **Sealed Secrets**
- **SOPS** (Secrets OPerationS)

## Verification

### 1. Check Deployment Status

```bash
# Check pods
kubectl get pods -l app.kubernetes.io/name=gdpr-anonymizer

# Check service
kubectl get svc gdpr-anonymizer

# Check ingress
kubectl get ingress
```

### 2. Check Certificate Status

```bash
# Check certificate resource
kubectl get certificate

# Check certificate details
kubectl describe certificate gdpr-anonymizer-tls

# Check cert-manager logs if issues
kubectl logs -n cert-manager deploy/cert-manager
```

### 3. Test the Endpoints

Wait for the certificate to be issued (can take 1-2 minutes), then:

```bash
# Test health endpoint
curl https://anonymizer.lacambra.tech/health

# Test anonymization
curl -X POST https://anonymizer.lacambra.tech/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text": "My name is John Smith and I live in Paris."}'
```

## DNS Configuration

Make sure your DNS is configured to point to your ingress controller's external IP:

```bash
# Get the ingress controller external IP
kubectl get svc -n ingress-nginx

# Add an A record:
# anonymizer.lacambra.tech -> <EXTERNAL-IP>
```

## Upgrading

To upgrade the deployment:

```bash
# Upgrade with new image version
helm upgrade gdpr-anonymizer ./helm/gdpr-anonymizer \
  -f ./helm/gdpr-anonymizer/values-production.yaml \
  --set image.tag="v1.1.0" \
  --reuse-values

# Or upgrade with new API key
helm upgrade gdpr-anonymizer ./helm/gdpr-anonymizer \
  -f ./helm/gdpr-anonymizer/values-production.yaml \
  --set secrets.anthropicApiKey="new-key" \
  --reuse-values
```

## Rollback

If something goes wrong:

```bash
# List releases
helm history gdpr-anonymizer

# Rollback to previous version
helm rollback gdpr-anonymizer

# Or rollback to specific revision
helm rollback gdpr-anonymizer 2
```

## Uninstalling

To remove the deployment:

```bash
helm uninstall gdpr-anonymizer

# Certificate and secret will be automatically cleaned up
```

## Troubleshooting

### Certificate not issuing

```bash
# Check certificate status
kubectl describe certificate gdpr-anonymizer-tls

# Check certificate request
kubectl get certificaterequest
kubectl describe certificaterequest <name>

# Check order
kubectl get order
kubectl describe order <name>

# Check challenge
kubectl get challenge
kubectl describe challenge <name>
```

### Common Issues

1. **Certificate stays in "pending" state**
   - Check if DNS is properly configured
   - Verify nginx-ingress-controller can reach the internet
   - Check cert-manager logs

2. **502 Bad Gateway**
   - Check if pods are running: `kubectl get pods`
   - Check pod logs: `kubectl logs <pod-name>`
   - Verify service endpoints: `kubectl get endpoints`

3. **Ingress not accessible**
   - Check ingress: `kubectl describe ingress`
   - Verify ingress controller is running
   - Check DNS resolution: `nslookup anonymizer.lacambra.tech`

### Viewing Logs

```bash
# Application logs
kubectl logs -l app.kubernetes.io/name=gdpr-anonymizer -f

# Previous pod logs (if crashed)
kubectl logs -l app.kubernetes.io/name=gdpr-anonymizer --previous

# cert-manager logs
kubectl logs -n cert-manager deploy/cert-manager -f
```

## Monitoring

### Check Resource Usage

```bash
# CPU and Memory
kubectl top pods -l app.kubernetes.io/name=gdpr-anonymizer

# Describe deployment
kubectl describe deployment gdpr-anonymizer
```

### Access API Documentation

Once deployed, access the Swagger UI:
- https://anonymizer.lacambra.tech/docs
- https://anonymizer.lacambra.tech/redoc

## Security Best Practices

1. ✅ Use Let's Encrypt for TLS certificates
2. ✅ Store secrets securely (not in Git)
3. ✅ Enable HTTPS redirect
4. ✅ Use specific image tags (not `latest`) in production
5. ✅ Set resource limits
6. ✅ Enable autoscaling
7. ✅ Run as non-root user (already configured)
8. ✅ Use network policies (if needed)
9. ✅ Regular security updates

## Next Steps

1. Set up monitoring with Prometheus/Grafana
2. Configure log aggregation (ELK/Loki)
3. Set up alerts for errors/high latency
4. Implement backup strategy
5. Set up CI/CD pipeline for automated deployments
