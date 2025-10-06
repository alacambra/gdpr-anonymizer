# GDPR Anonymizer - Iteration 4

## Hexagonal Architecture Implementation

This is Iteration 4 of the GDPR Anonymizer, featuring a production-ready hexagonal architecture with FastAPI REST interface.

### What's New in Iteration 4

- **Hexagonal Architecture**: Clean separation of Domain, Application, Infrastructure, and Interface layers
- **FastAPI REST API**: Production-ready HTTP interface with OpenAPI documentation
- **Async/Await**: Full asynchronous support throughout the stack
- **Configuration System**: YAML-based configuration with environment variable substitution
- **Dependency Injection**: Clean DI pattern using FastAPI dependencies
- **Swappable LLM Providers**: Easy switching between Claude, OpenAI, and Ollama

### Architecture Overview

```
src/anonymization/
├── domain/                    # Domain Layer (zero external dependencies)
│   ├── models/                # Domain entities and value objects
│   ├── ports/                 # Interfaces for infrastructure
│   └── agents/                # Agent definitions and prompts
├── application/               # Application Layer
│   ├── orchestrator.py        # Workflow coordination
│   └── config.py              # Configuration models
├── infrastructure/            # Infrastructure Layer
│   ├── adapters/llm/          # LLM provider adapters
│   ├── agents/                # Agent implementations
│   └── config_loader.py       # YAML configuration loader
└── interfaces/rest/           # Interface Layer
    ├── main.py                # FastAPI application
    ├── routers/               # API route handlers
    ├── schemas/               # Request/response models
    └── dependencies.py        # Dependency injection
```

### Quick Start

#### 1. Install Dependencies

```bash
# Install base dependencies
poetry install

# Install with specific LLM provider
poetry install -E claude    # For Anthropic Claude
poetry install -E openai    # For OpenAI
poetry install -E ollama    # For Ollama
```

#### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# For Claude:
export ANTHROPIC_API_KEY=your-key-here

# For OpenAI:
export OPENAI_API_KEY=your-key-here
```

#### 3. Configure Application

```bash
# Copy example config
cp config/config.yaml.example config/config.yaml

# Edit config/config.yaml to set your LLM provider
```

#### 4. Run the API Server

```bash
# Using the run script
python run_api.py

# Or using uvicorn directly
uvicorn anonymization.interfaces.rest.main:app --reload
```

#### 5. Access API Documentation

Open your browser to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### API Usage Examples

#### Anonymize a Single Document

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact John Smith at john@email.com or call 555-1234",
    "document_id": "doc-123"
  }'
```

Response:
```json
{
  "document_id": "doc-123",
  "anonymized_text": "Contact [NAME_1] at [EMAIL_1] or call [PHONE_1]",
  "mappings": {
    "John Smith": "[NAME_1]",
    "john@email.com": "[EMAIL_1]",
    "555-1234": "[PHONE_1]"
  },
  "validation": {
    "passed": true,
    "issues": [],
    "reasoning": "All identifiers properly anonymized",
    "confidence": 0.95
  },
  "risk_assessment": {
    "overall_score": 5,
    "risk_level": "NEGLIGIBLE",
    "gdpr_compliant": true,
    "confidence": 1.0,
    "reasoning": "Stub implementation..."
  },
  "iterations": 1,
  "success": true
}
```

#### Batch Anonymization

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {"text": "Call Jane at 555-1111", "document_id": "doc-1"},
      {"text": "Email bob@company.com", "document_id": "doc-2"}
    ]
  }'
```

### Configuration

Edit `config/config.yaml`:

```yaml
llm:
  provider: "claude"  # or "openai" or "ollama"
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.1
  max_tokens: 4096

agents:
  agent1:
    name: "ANON-EXEC"
    enabled: true
  agent2:
    name: "DIRECT-CHECK"
    enabled: true
  agent3:
    name: "RISK-ASSESS"
    enabled: true

orchestration:
  max_iterations: 3  # Retry attempts for validation failures
  timeout_seconds: 300
```

### Agent Workflow

1. **Agent 1 (ANON-EXEC)**: Identifies and replaces personal data entities
2. **Agent 2 (DIRECT-CHECK)**: Validates that no identifiers remain
3. **Retry Loop**: If validation fails, retry Agent 1 (up to max_iterations)
4. **Agent 3 (RISK-ASSESS)**: Assesses GDPR compliance risk (currently stub)

### Switching LLM Providers

The system supports three LLM providers. To switch:

1. Update `config/config.yaml`:
   ```yaml
   llm:
     provider: "openai"  # Change provider
     model: "gpt-4"      # Update model
   ```

2. Set appropriate environment variable:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```

3. Install provider package:
   ```bash
   poetry install -E openai
   ```

### Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Simple anonymization test
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text": "My name is John and my email is john@test.com"}'
```

### Development

#### Project Structure

- **Domain Layer**: Core business logic, zero external dependencies
- **Application Layer**: Orchestration and use cases
- **Infrastructure Layer**: External integrations (LLM providers, agents)
- **Interface Layer**: REST API with FastAPI

#### Adding a New LLM Provider

1. Create adapter in `infrastructure/adapters/llm/`
2. Implement `ILLMProvider` interface
3. Add to factory in `factory.py`
4. Update configuration schema

### Backward Compatibility

The old POC functions from Iteration 1-3 are still available:

```python
from anonymization.simple import anonymize_simple
from anonymization.validation import validate_anonymization
from anonymization.risk import assess_risk

# These still work but are deprecated
result = anonymize_simple("Contact John at john@email.com")
```

**Recommended**: Use the new hexagonal architecture via the REST API or by importing the orchestrator.

### Known Limitations (Iteration 4)

- **Agent 3 is a stub**: Always returns NEGLIGIBLE risk (real implementation in future iteration)
- **No persistence**: Results are not stored (in-memory only)
- **No authentication**: API is open (add auth in production)
- **No rate limiting**: No request throttling (add for production)
- **Basic error handling**: Production deployment should enhance error handling

### Migration from Previous Iterations

If you were using Iteration 1-3:

**Before (Iteration 1-3)**:
```python
from anonymization.simple import anonymize_simple
result = anonymize_simple("Contact John")
print(result.anonymized_text)
```

**After (Iteration 4 - Programmatic)**:
```python
from anonymization.application.orchestrator import AnonymizationOrchestrator
from anonymization.domain.models import Document
from anonymization.infrastructure.adapters.llm import create_llm_provider
from anonymization.infrastructure.agents import (
    Agent1Implementation,
    Agent2Implementation,
    Agent3Implementation
)

# Create components
llm = create_llm_provider("claude", {"model": "claude-3-5-sonnet-20241022"})
agent1 = Agent1Implementation(llm)
agent2 = Agent2Implementation(llm)
agent3 = Agent3Implementation(llm)
orchestrator = AnonymizationOrchestrator(agent1, agent2, agent3)

# Use orchestrator
doc = Document(content="Contact John")
result = await orchestrator.anonymize_document(doc)
print(result.anonymization.anonymized_text)
```

**After (Iteration 4 - REST API)**:
```bash
curl -X POST http://localhost:8000/api/v1/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text": "Contact John"}'
```

### Performance Targets

- Small documents (<100 words): <10 seconds
- Medium documents (100-500 words): <30 seconds
- API response time (P95): <15 seconds
- Health check: <100ms

### Next Steps (Future Iterations)

- Implement real Agent 3 risk assessment with 5-dimensional scoring
- Add comprehensive testing suite (>85% coverage)
- Add database persistence
- Add authentication and authorization
- Add rate limiting
- Add CLI interface
- Add batch file processing
- Production logging and monitoring

### Support

For issues or questions:
- Check API documentation: http://localhost:8000/docs
- Review configuration: `config/config.yaml`
- Check logs for errors

---

**Version**: 0.4.0
**Status**: Production-ready architecture (Agent 3 stub)
**Architecture**: Hexagonal (Ports and Adapters)
