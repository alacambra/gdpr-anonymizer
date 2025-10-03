# GDPR Anonymization System

A professional Python application that uses AutoGen to orchestrate three specialized AI agents for GDPR-compliant document anonymization.

## System Overview

This system implements a multi-agent workflow for document anonymization:

1. **ANON-EXEC**: Anonymization Executor - Replaces personal data with placeholders
2. **DIRECT-CHECK**: Direct Data Verification - Verifies no direct identifiers remain
3. **RISK-ASSESS**: Risk Assessment - Evaluates re-identification risks

## Features

- 🤖 **Multi-Agent Orchestration**: Uses AutoGen for coordinated agent workflow
- 🔒 **GDPR Compliance**: Follows GDPR anonymization standards
- 📊 **Risk Assessment**: Evaluates re-identification probability
- 📝 **Detailed Logging**: Complete audit trail of anonymization process
- ✅ **Quality Assurance**: Built-in verification and validation
- 🏗️ **Professional Architecture**: Modular, testable, and maintainable code
- 🐳 **Docker Support**: Containerized deployment
- 🧪 **Comprehensive Testing**: Unit and integration tests
- 📋 **Rich CLI**: Beautiful command-line interface with progress indicators

## Installation

### Development Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd gdpr-anonymizer
```

2. Install in development mode:
```bash
# Install with all development dependencies
make install-dev

# Or manually
pip install -e ".[dev,test,docs]"
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Production Installation

```bash
pip install gdpr-anonymizer
```

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t gdpr-anonymizer .
docker run -e OPENAI_API_KEY=your_key gdpr-anonymizer
```

## Usage

### Command Line Interface

The system provides a rich CLI for easy document processing:

```bash
# Get help
gdpr-anonymizer --help

# Anonymize a document file
gdpr-anonymizer anonymize document.txt

# Anonymize with custom settings
gdpr-anonymizer --config config.yaml anonymize document.txt --format json

# Initialize configuration file
gdpr-anonymizer init-config --output my_config.yaml

# Display system information
gdpr-anonymizer info
```

### Python API

```python
from gdpr_anonymizer import GDPRAnonymizationOrchestrator

# Initialize the system
orchestrator = GDPRAnonymizationOrchestrator()

# Anonymize a document
document = "John Smith works at TechCorp. Email: john@techcorp.com"
result = orchestrator.anonymize_document(document)

print(f"Anonymized: {result.anonymized_document}")
print(f"Risk Level: {result.final_risk_level.value}")
print(f"Compliance: {result.compliance_status.value}")
```

### Example Script

Run the included example:
```bash
# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run example
python scripts/run_example.py
```

## Configuration

### Configuration File

Create a YAML configuration file:

```yaml
# config.yaml
llm_provider: openai
openai:
  model: gpt-4
  temperature: 0.1
  api_key: ${OPENAI_API_KEY}

logging:
  level: INFO
  file_path: logs/gdpr_anonymizer.log

anonymization:
  risk_threshold: MEDIUM
  preserve_structure: true

output_dir: ./output
save_reports: true
```

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `AZURE_OPENAI_API_KEY`: Azure OpenAI key (optional)
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint (optional)
- `ENV`: Environment (development/production)
- `DEBUG`: Enable debug mode

### Programmatic Configuration

```python
from gdpr_anonymizer.config import Settings

settings = Settings(
    llm_provider="openai",
    openai={"model": "gpt-3.5-turbo"},
    anonymization={"risk_threshold": "LOW"}
)

orchestrator = GDPRAnonymizationOrchestrator(settings)
```

## Agent Specifications

### ANON-EXEC (Anonymization Executor)
- **Purpose**: Replace personal data with standardized placeholders
- **Placeholders**: Uses sequential numbering (e.g., [NAME_1], [EMAIL_1])
- **Coverage**: Direct identifiers (names, emails, phones) and indirect identifiers

### DIRECT-CHECK (Direct Data Verification)
- **Purpose**: Verify no direct personal identifiers remain
- **Validation**: Scans for missed names, emails, phones, addresses, IDs
- **Output**: Binary PASS/FAIL with specific findings

### RISK-ASSESS (Re-identification Risk Assessment)
- **Purpose**: Evaluate re-identification risks from remaining data
- **Scoring**: 5-dimension risk matrix (1-25 total score)
- **Categories**: CRITICAL/HIGH/MEDIUM/LOW/NEGLIGIBLE

## Output Format

The system returns an `AnonymizationResult` object with:

- `anonymized_document`: The processed document
- `anonymization_logs`: Detailed mapping of replacements
- `processing_summary`: Statistics on changes made
- `agent_reports`: Complete reports from all three agents
- `risk_assessment`: Overall risk assessment with detailed scoring
- `compliance_status`: GDPR compliance determination

## Example Workflow

```
Original Document → ANON-EXEC → Anonymized Document
                                       ↓
                    DIRECT-CHECK ← Anonymized Document
                         ↓ (PASS)
                    RISK-ASSESS → Final Risk Assessment
                         ↓
                 Compliance Decision
```

## Risk Assessment Matrix

| Score | Risk Level | Description |
|-------|------------|-------------|
| 20-25 | CRITICAL   | Likely re-identification |
| 15-19 | HIGH       | Possible with effort |
| 10-14 | MEDIUM     | Difficult but possible |
| 5-9   | LOW        | Very difficult |
| 5     | NEGLIGIBLE | Practically impossible |

## Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Setup pre-commit hooks
make dev-setup
```

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/unit/test_orchestrator.py -v
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Run all quality checks
make check
```

### Building

```bash
# Build package
make build

# Clean build artifacts
make clean
```

## Project Structure

```
gdpr-anonymizer/
├── gdpr_anonymizer/          # Main package
│   ├── agents/               # Agent implementations
│   ├── cli/                  # Command-line interface
│   ├── config/               # Configuration management
│   ├── core/                 # Core orchestration
│   ├── models/               # Data models
│   └── utils/                # Utilities
├── tests/                    # Test suite
├── scripts/                  # Utility scripts
├── docs/                     # Documentation
└── config/                   # Configuration files
```

## Limitations

- Requires OpenAI API access (or Azure OpenAI)
- Processing time depends on document length and complexity
- Quality depends on the underlying language model capabilities
- Currently supports text documents only

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run quality checks (`make check`)
5. Submit a pull request

### Future Enhancements

- Support for multiple document formats (PDF, DOCX, etc.)
- Local/offline anonymization models
- Batch processing capabilities
- Web interface
- Database integration for result storage
- Advanced ML-based personal data detection

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Please ensure compliance with relevant data protection regulations in your jurisdiction.