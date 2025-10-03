# GDPR Text Anonymization System - Iteration 1

**Minimal Proof-of-Concept** for GDPR-compliant text anonymization using LLMs.

## Overview

This is a simple, working prototype that demonstrates text anonymization by:
- Detecting personal data (names, emails, phone numbers, addresses)
- Replacing them with standardized placeholders like `[NAME_1]`, `[EMAIL_1]`
- Maintaining consistency across the document

## Installation

### Requirements
- Python ≥3.10
- Poetry (install from [python-poetry.org](https://python-poetry.org))
- ONE of: Ollama, Claude API key, or OpenAI API key

### Install Steps

1. **Clone the repository**:
```bash
git clone <repository-url>
cd gdpr-anonymizer
```

2. **Install with your LLM provider** (choose ONE):
```bash
# For Ollama (local, free)
poetry install -E ollama

# For Claude (Anthropic)
poetry install -E claude

# For OpenAI
poetry install -E openai
```

3. **Set up environment** (if using Claude or OpenAI):
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Usage

### Run the Demo

```bash
poetry run python demo.py
```

This will process 3 example texts and show you:
- Original text
- Anonymized text with placeholders
- Mapping of what was replaced

### Use in Your Code

```python
from anonymization import anonymize_simple

text = "Contact John Smith at john@email.com or call 555-1234"
result = anonymize_simple(text)

print(result.anonymized_text)
# Output: Contact [NAME_1] at [EMAIL_1] or call [PHONE_1]

print(result.mappings)
# Output: {'John Smith': '[NAME_1]', 'john@email.com': '[EMAIL_1]', '555-1234': '[PHONE_1]'}
```

## What's Included (Iteration 1)

✅ Detects: Names, Emails, Phone Numbers, Addresses
✅ Consistent placeholders across document
✅ Works with Ollama, Claude, or OpenAI
✅ Simple single-function API
✅ Runnable demo with examples

## What's NOT Included (Coming in Iteration 2+)

❌ Multi-agent verification
❌ Risk assessment
❌ Configuration files
❌ CLI interface
❌ File I/O
❌ Chunking for large documents
❌ Async processing
❌ Comprehensive error handling
❌ Automated tests

## Troubleshooting

**Error: "No LLM provider available"**
- Install an LLM provider: `poetry install -E ollama` (or claude/openai)
- If using Claude/OpenAI, set API key in `.env`

**Error: "Failed to parse LLM response as JSON"**
- The LLM might need a better model or different prompt
- Try using Claude or GPT-4 for more reliable results

## Architecture (Simplified)

```
src/anonymization/
├── __init__.py          # Domain model (AnonymizationResult)
├── llm.py              # LLM client wrapper (~70 lines)
├── simple.py           # Core anonymization logic (~120 lines)

demo.py                 # Runnable examples
examples/
└── sample_texts.py     # Sample texts for testing
```

## Next Steps

See [requirements/iteration1.md](requirements/iteration1.md) for full iteration 1 scope.

Iteration 2 will add:
- Multi-agent workflow (verification + risk assessment)
- Configuration system
- Better error handling
- Async processing

## License

MIT - See [LICENSE](LICENSE)
