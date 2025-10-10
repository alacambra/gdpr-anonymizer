# LLM Provider Info in API Response ✅

## What Was Added

The API now returns which LLM provider and model were used for anonymization in every response!

## Changes Made (Very Simple!)

### 1. Response Schema Updated
**File**: `src/anonymization/interfaces/rest/schemas/responses.py`

Added two new fields to `AnonymizeResponse`:
```python
llm_provider: str = Field(description="LLM provider used (ollama, claude, openai)")
llm_model: str = Field(description="Specific LLM model used")
```

### 2. Router Updated
**File**: `src/anonymization/interfaces/rest/routers/anonymization.py`

- Injected `config` dependency to access LLM settings
- Added `llm_provider` and `llm_model` to response
- Updated both `/anonymize` and `/anonymize/batch` endpoints

## Example Response

### Before:
```json
{
  "anonymized_text": "Contact [NAME_1] at [EMAIL_1]",
  "mappings": {...},
  "validation": {...},
  "success": true
}
```

### After:
```json
{
  "anonymized_text": "Contact [NAME_1] at [EMAIL_1]",
  "mappings": {...},
  "validation": {...},
  "success": true,
  "llm_provider": "claude",
  "llm_model": "claude-3-5-sonnet-20241022"
}
```

## Test It

### Using curl:
```bash
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact John Smith at john@email.com"
  }' | python -m json.tool
```

### Using test script:
```bash
./test_llm_info.sh
```

### Look for these fields in the response:
```json
{
  ...
  "llm_provider": "claude",
  "llm_model": "claude-3-5-sonnet-20241022"
  ...
}
```

## Different Providers

The response will show different values based on your `config.yaml`:

### Claude:
```json
"llm_provider": "claude",
"llm_model": "claude-3-5-sonnet-20241022"
```

### OpenAI:
```json
"llm_provider": "openai",
"llm_model": "gpt-4"
```

### Ollama:
```json
"llm_provider": "ollama",
"llm_model": "gemma-custom"
```

## Why This Is Useful

1. **Transparency**: Users know exactly which LLM processed their data
2. **Debugging**: Easy to see if the right model was used
3. **Auditing**: Track which models are being used in production
4. **Billing**: Know which provider/model for cost tracking
5. **Compliance**: Document which AI model processed sensitive data

## Complexity: VERY LOW ✅

Total changes:
- **2 new fields** in response schema
- **1 dependency injection** (config)
- **2 lines** added to populate the fields
- **~5 minutes** to implement

No breaking changes, fully backward compatible if clients ignore new fields!

---

**Status**: ✅ Complete and tested
**Lines of Code Changed**: ~10
**Complexity**: Very Low
**Breaking Changes**: None
