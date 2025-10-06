# GDPR Text Anonymization System - Iteration 4

**Production-Ready Hexagonal Architecture** for GDPR-compliant text anonymization using LLMs.

> **📌 This is Iteration 4** - Full hexagonal architecture with FastAPI REST interface.
> See [README-ITERATION-4.md](README-ITERATION-4.md) for detailed documentation.

## Overview

A production-ready text anonymization system featuring:
- **Hexagonal Architecture**: Clean separation of Domain, Application, Infrastructure, and Interface layers
- **Multi-Agent Workflow**: Agent 1 (anonymization) → Agent 2 (validation) → Agent 3 (risk assessment)
- **FastAPI REST API**: Production-ready HTTP interface with OpenAPI docs
- **Async/Await**: Full asynchronous support throughout
- **Swappable LLM Providers**: Easy switching between Claude, OpenAI, and Ollama
- **Configuration System**: YAML-based config with environment variables

## Installation

### Requirements
- Python ≥3.10
- Poetry (install from [python-poetry.org](https://python-poetry.org))
- ONE of: Ollama, Claude API key, or OpenAI API key

### Quick Start

1. **Install dependencies**:
```bash
# Install base dependencies
python3 -m venv python3_venv
source python3_venv/bin/activate
pip install fastapi uvicorn pyyaml python-dotenv httpx pydantic

# Install your LLM provider
pip install anthropic  # For Claude
# OR pip install openai  # For OpenAI
# OR pip install ollama  # For Ollama
```

2. **Configure**:
```bash
# Set API key
export ANTHROPIC_API_KEY=your-key-here

# Configure application (optional - defaults to Claude)
cp config/config.yaml.example config/config.yaml
```

3. **Run the API**:
```bash
python run_api.py
```

4. **Test it**:
```bash
# Open browser to http://localhost:8000/docs
# Or use curl:
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Contact John Smith at john@email.com"}'
```

## Usage

### REST API (Recommended)

Start the API server:
```bash
python run_api.py
```

Use the API:
```bash
# Anonymize single document
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact John Smith at john@email.com or call 555-1234",
    "document_id": "doc-123"
  }'
```

Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Programmatic Usage

```python
import asyncio
from anonymization.application.orchestrator import AnonymizationOrchestrator
from anonymization.domain.models import Document
from anonymization.infrastructure.adapters.llm import create_llm_provider
from anonymization.infrastructure.agents import (
    Agent1Implementation, Agent2Implementation, Agent3Implementation
)

async def anonymize():
    # Create components
    llm = create_llm_provider("claude", {"model": "claude-3-5-sonnet-20241022"})
    agent1 = Agent1Implementation(llm)
    agent2 = Agent2Implementation(llm)
    agent3 = Agent3Implementation(llm)
    orchestrator = AnonymizationOrchestrator(agent1, agent2, agent3)

    # Anonymize document
    doc = Document(content="Contact John Smith at john@email.com")
    result = await orchestrator.anonymize_document(doc)

    print(result.anonymization.anonymized_text)
    print(result.validation.passed)
    print(result.risk_assessment.gdpr_compliant)

asyncio.run(anonymize())
```

### Legacy API (Deprecated)

The old simple functions still work but are deprecated:
```python
from anonymization.simple import anonymize_simple
result = anonymize_simple("Contact John")  # Works but deprecated
```

## What's Included (Iteration 4)

✅ **Hexagonal Architecture**: Domain, Application, Infrastructure, Interface layers
✅ **Multi-Agent Workflow**: Agent 1 (anonymization) → Agent 2 (validation) → Agent 3 (risk assessment stub)
✅ **FastAPI REST API**: Production-ready HTTP interface
✅ **Async/Await**: Full asynchronous support
✅ **Configuration System**: YAML config with environment variables
✅ **Swappable LLM Providers**: Claude, OpenAI, Ollama
✅ **Dependency Injection**: Clean DI pattern with FastAPI
✅ **OpenAPI Documentation**: Auto-generated API docs
✅ **Retry Logic**: Automatic retry on validation failures
✅ **Domain Models**: Immutable value objects and entities

## What's NOT Included (Future Iterations)

❌ Real Agent 3 risk assessment (currently stub - returns NEGLIGIBLE)
❌ Database persistence
❌ Authentication/authorization
❌ Rate limiting
❌ Comprehensive test suite
❌ CLI interface
❌ Batch file processing
❌ Production monitoring/logging

## Troubleshooting

**Error: "No LLM provider available"**
- Install an LLM provider: `poetry install -E ollama` (or claude/openai)
- If using Claude/OpenAI, set API key in `.env`

**Error: "Failed to parse LLM response as JSON"**
- The LLM might need a better model or different prompt
- Try using Claude or GPT-4 for more reliable results

## Architecture (Hexagonal)

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

config/
└── config.yaml               # Application configuration

run_api.py                    # API server startup script
test_iteration4.py            # Integration test script
```

## Documentation

- **[README-ITERATION-4.md](README-ITERATION-4.md)**: Comprehensive Iteration 4 documentation
- **[executions/execution-4/iteration-4-requeirments.md](executions/execution-4/iteration-4-requeirments.md)**: Full requirements specification
- **API Docs**: http://localhost:8000/docs (when server is running)

## Testing

```bash
# Test the hexagonal architecture
source python3_venv/bin/activate
python test_iteration4.py

# Start API and test endpoints
python run_api.py
# In another terminal:
curl http://localhost:8000/health
```

## License

MIT - See [LICENSE](LICENSE)
