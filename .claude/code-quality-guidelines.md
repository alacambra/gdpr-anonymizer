# Code Quality Guidelines for GDPR Anonymizer Project

## Pylance/Type Checking Requirements

### ✅ MANDATORY: Zero Pylance Errors

All code MUST be free of Pylance errors before considering implementation complete.

**Requirements:**
1. **No Pylance errors** - Red squiggly lines must be resolved
2. **Minimal Pylance warnings** - Yellow warnings should be addressed where reasonable
3. **Type hints required** - All public functions must have complete type hints
4. **Import statements valid** - All imports must resolve correctly

### Common Pylance Issues to Fix

#### 1. Missing Type Stubs
```python
# ❌ BAD - Will cause "reportMissingTypeStubs" error
import ollama  # If ollama doesn't have type stubs

# ✅ GOOD - Add type: ignore comment with explanation
import ollama  # type: ignore[import-untyped]
```

#### 2. Missing Imports
```python
# ❌ BAD - Using Optional without importing
def foo(x: Optional[str]) -> str:
    ...

# ✅ GOOD - Import from typing
from typing import Optional

def foo(x: Optional[str]) -> str:
    ...
```

#### 3. Incomplete Type Hints
```python
# ❌ BAD - Missing return type
def process_data(text):
    return text.upper()

# ✅ GOOD - Complete type hints
def process_data(text: str) -> str:
    return text.upper()
```

#### 4. Incorrect Type Annotations
```python
# ❌ BAD - Wrong type
def get_config() -> str:
    return {"key": "value"}  # Returns dict, not str

# ✅ GOOD - Correct type
from typing import Dict

def get_config() -> Dict[str, str]:
    return {"key": "value"}
```

### Pre-Commit Checklist

Before considering any code complete:

- [ ] Run Pylance type check (VS Code will show errors)
- [ ] Resolve all red error squiggles
- [ ] Add `# type: ignore` comments ONLY when necessary with explanation
- [ ] Ensure all public functions have type hints
- [ ] Verify all imports resolve correctly
- [ ] Test that imports work: `python -c "import module"`

### Type Ignore Guidelines

When you MUST use `# type: ignore`:

1. **Always specify the error code**:
   ```python
   import ollama  # type: ignore[import-untyped]
   ```

2. **Add explanation for why it's needed**:
   ```python
   # Ollama library doesn't provide type stubs
   import ollama  # type: ignore[import-untyped]
   ```

3. **Use sparingly** - Only when:
   - Third-party library lacks type stubs
   - Dynamic typing is genuinely necessary
   - Working around a known limitation

### Iteration-Specific Rules

#### Iteration 1
- Basic type hints required
- Third-party library type issues can be suppressed with `type: ignore`
- Focus on zero Pylance errors

#### Iteration 2+
- Strict type checking with mypy
- Minimize `type: ignore` usage
- Add type stubs for third-party libraries if possible
- Use `Protocol` for interfaces

### Tools

**Recommended VS Code Settings:**
```json
{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.diagnosticMode": "workspace",
  "python.analysis.autoImportCompletions": true
}
```

**Future: mypy configuration** (Iteration 2+):
```ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## General Code Quality Standards

### 1. Imports Organization
```python
# Standard library first
import os
import sys
from typing import Dict, List, Optional

# Third-party libraries second
import anthropic  # type: ignore[import-untyped]

# Local imports last
from .models import AnonymizationResult
```

### 2. Docstrings
All public functions MUST have docstrings:
```python
def anonymize_simple(text: str) -> AnonymizationResult:
    """
    Anonymize text containing personal information.

    Args:
        text: Plain text string to anonymize

    Returns:
        AnonymizationResult with anonymized_text, mappings, original_text
    """
```

### 3. Error Messages
Provide clear, actionable error messages:
```python
# ❌ BAD
raise ValueError("Error")

# ✅ GOOD
raise ValueError(
    "No LLM provider available. Please install one:\n"
    "  poetry install -E ollama\n"
    "  poetry install -E claude\n"
    "  poetry install -E openai"
)
```

### 4. Comments and Self-Documenting Code
Avoid inline comments. Use self-defining functions instead. If several lines require a comment, extract them into a self-defining function.

```python
# ❌ BAD - Inline comments explaining logic
def process_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    # Validate email format
    if not re.match(r'^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,3}$', data['email']):
        raise ValueError("Invalid email")

    # Check if user is adult
    if data['age'] < 18:
        data['requires_consent'] = True

    # Format phone number to international format
    data['phone'] = '+1' + data['phone'].replace('-', '')

    return data

# ✅ GOOD - Self-defining functions
def process_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    validate_email_format(data['email'])
    data = add_consent_requirement_if_minor(data)
    data['phone'] = format_phone_to_international(data['phone'])
    return data

def validate_email_format(email: str) -> None:
    if not re.match(r'^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,3}$', email):
        raise ValueError("Invalid email")

def add_consent_requirement_if_minor(data: Dict[str, Any]) -> Dict[str, Any]:
    if data['age'] < 18:
        data['requires_consent'] = True
    return data

def format_phone_to_international(phone: str) -> str:
    return '+1' + phone.replace('-', '')
```

## Summary

**Before marking any task complete:**
1. ✅ Zero Pylance errors in VS Code
2. ✅ All type hints in place
3. ✅ All imports resolve correctly
4. ✅ Code passes manual review
5. ✅ Docstrings on all public APIs

**When in doubt**: Fix the Pylance error properly rather than suppressing it.
