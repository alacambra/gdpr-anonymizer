# GDPR Anonymizer Helm Chart

A Helm chart for deploying the GDPR Anonymizer application - an LLM-powered text anonymization service.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure (optional)
- At least one LLM API key (Anthropic or OpenAI)

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release ./helm/gdpr-anonymizer
```

### Installing with API Keys

It's recommended to provide API keys during installation:

```bash
helm install my-release ./helm/gdpr-anonymizer \
  --set secrets.anthropicApiKey="your-anthropic-key" \
  --set secrets.openaiApiKey="your-openai-key"
```

Or use a values file:

```bash
helm install my-release ./helm/gdpr-anonymizer -f my-values.yaml
```

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm uninstall my-release
```

## Configuration

The following table lists the configurable parameters of the GDPR Anonymizer chart and their default values.

### General Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `2` |
| `image.repository` | Image repository | `gdpr-anonymizer` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `image.tag` | Image tag | `latest` |
| `nameOverride` | Override the chart name | `""` |
| `fullnameOverride` | Override the full name | `""` |

### Service Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `8000` |
| `service.targetPort` | Target port | `8000` |

### Ingress Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts` | Ingress hosts configuration | See values.yaml |
| `ingress.tls` | Ingress TLS configuration | `[]` |

### Resources Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `resources.limits.cpu` | CPU limit | `1000m` |
| `resources.limits.memory` | Memory limit | `1Gi` |
| `resources.requests.cpu` | CPU request | `250m` |
| `resources.requests.memory` | Memory request | `512Mi` |

### Application Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `config.llmProvider` | LLM provider to use (claude, openai, ollama) | `claude` |
| `config.claude.model` | Claude model name | `claude-3-5-sonnet-20241022` |
| `config.openai.model` | OpenAI model name | `gpt-4` |
| `config.anonymization.maxIterations` | Max anonymization iterations | `3` |
| `config.anonymization.validationThreshold` | Validation threshold | `0.8` |
| `config.logging.level` | Log level | `INFO` |

### Secrets

| Parameter | Description | Default |
|-----------|-------------|---------|
| `secrets.anthropicApiKey` | Anthropic API key | `""` |
| `secrets.openaiApiKey` | OpenAI API key | `""` |

### Autoscaling

| Parameter | Description | Default |
|-----------|-------------|---------|
| `autoscaling.enabled` | Enable autoscaling | `false` |
| `autoscaling.minReplicas` | Minimum replicas | `2` |
| `autoscaling.maxReplicas` | Maximum replicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization | `80` |

## Examples

### Basic Installation with Anthropic

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  --set secrets.anthropicApiKey="sk-ant-xxxxx"
```

### Installation with Custom Configuration

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  --set secrets.anthropicApiKey="sk-ant-xxxxx" \
  --set config.llmProvider="claude" \
  --set config.claude.model="claude-3-5-sonnet-20241022" \
  --set replicaCount=3
```

### Installation with Ingress Enabled

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  --set secrets.anthropicApiKey="sk-ant-xxxxx" \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host="anonymizer.example.com" \
  --set ingress.hosts[0].paths[0].path="/" \
  --set ingress.hosts[0].paths[0].pathType="Prefix"
```

### Installation with Autoscaling

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer \
  --set secrets.anthropicApiKey="sk-ant-xxxxx" \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=10 \
  --set autoscaling.targetCPUUtilizationPercentage=80
```

### Using a Custom Values File

Create `my-values.yaml`:

```yaml
replicaCount: 3

image:
  repository: myregistry/gdpr-anonymizer
  tag: "v1.0.0"

secrets:
  anthropicApiKey: "sk-ant-xxxxx"

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: anonymizer.mycompany.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: anonymizer-tls
      hosts:
        - anonymizer.mycompany.com

config:
  llmProvider: "claude"
  anonymization:
    maxIterations: 5
    validationThreshold: 0.9

resources:
  limits:
    cpu: 2000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi
```

Install with:

```bash
helm install gdpr-anonymizer ./helm/gdpr-anonymizer -f my-values.yaml
```

## Upgrading

To upgrade an existing release:

```bash
helm upgrade gdpr-anonymizer ./helm/gdpr-anonymizer
```

Or to update specific values:

```bash
helm upgrade gdpr-anonymizer ./helm/gdpr-anonymizer \
  --reuse-values \
  --set image.tag="v1.1.0"
```

## Testing the Deployment

After installation, you can test the deployment:

```bash
# Port forward to access the service locally
kubectl port-forward svc/gdpr-anonymizer 8000:8000

# Test the health endpoint
curl http://localhost:8000/health

# Test anonymization
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text": "My name is John Smith and I live in Paris."}'
```

## Security Considerations

- Never commit API keys to version control
- Use Kubernetes Secrets or external secret management (e.g., HashiCorp Vault, AWS Secrets Manager)
- Consider using RBAC to restrict access to secrets
- Enable TLS for ingress in production
- Review and adjust security contexts as needed

## Troubleshooting

### Check pod status
```bash
kubectl get pods -l app.kubernetes.io/name=gdpr-anonymizer
```

### View logs
```bash
kubectl logs -l app.kubernetes.io/name=gdpr-anonymizer
```

### Check configuration
```bash
kubectl describe configmap gdpr-anonymizer
```

### Verify secrets
```bash
kubectl get secret gdpr-anonymizer -o yaml
```

## License

See the main project LICENSE file.
