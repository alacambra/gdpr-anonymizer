# Software Design Requirements

## SD-001: Data Models and DTOs

### SD-001.1: Pydantic Models for Entity Detection

- **Requirement**: Use Pydantic models for type-safe serialization/deserialization of entity detection data
- **Rationale**: Provides automatic validation, clear error messages, and type safety
- **Implementation**:
  - `Entity` model with `type` (EntityType enum) and `value` (str) fields
  - `EntityList` container model with serialization methods
  - `EntityType` enum for supported entity types (NAME, EMAIL, PHONE, ADDRESS)
- **Dependencies**: `pydantic>=2.0.0`
- **Status**: ✅ Implemented in `src/anonymization/models.py`

### SD-001.2: Entity Model Validation

- **Requirement**: Automatic validation of entity data
- **Rules**:
  - Entity type must be one of: NAME, EMAIL, PHONE, ADDRESS
  - Entity value must be non-empty string
  - Whitespace is automatically stripped from values
- **Status**: ✅ Implemented

### SD-001.3: Serialization Methods

- **Requirement**: Provide convenient methods for JSON serialization/deserialization
- **Methods**:
  - `EntityList.from_json(json_str)` - Parse JSON string to EntityList
  - `EntityList.from_list(items)` - Create from list of dicts
  - `to_dict_list()` - Convert to list of dictionaries
  - `model_dump_json()` - Pydantic built-in JSON serialization
- **Status**: ✅ Implemented

## SD-002: Development Dependencies

### SD-002.1: Testing Framework

- **Requirement**: `pytest>=7.0.0` for unit and integration testing
- **Status**: ✅ Added to requirements.txt

### SD-002.2: Code Coverage

- **Requirement**: `pytest-cov>=4.0.0` for test coverage reporting
- **Status**: ✅ Added to requirements.txt

### SD-002.3: Test Utilities

- **Requirement**: `pytest-mock>=3.10.0` for mocking in tests
- **Status**: ✅ Added to requirements.txt

### SD-002.4: Code Formatting

- **Requirement**: `black>=23.0.0` for consistent code formatting
- **Status**: ✅ Added to requirements.txt

### SD-002.5: Import Sorting

- **Requirement**: `isort>=5.12.0` for consistent import ordering
- **Status**: ✅ Added to requirements.txt

### SD-002.6: Linting

- **Requirement**: `flake8>=6.0.0` for code quality checks
- **Status**: ✅ Added to requirements.txt

### SD-002.7: Type Checking

- **Requirement**: `mypy>=1.0.0` for static type analysis
- **Status**: ✅ Added to requirements.txt
