# Iteration 1 Requirements - Minimal Viable Anonymization

## Document Information

**Version**: 1.0  
**Status**: Ready for Implementation  
**Iteration Goal**: Prove core anonymization concept with absolute minimum code  
**Target Completion**: Single development sprint  
**Related Documents**: 
- Functional Requirements v1.0
- Architectural Requirements v1.0

---

## 1. Iteration Overview

### 1.1 Purpose

Deliver a working proof-of-concept that demonstrates:

- Text anonymization is technically feasible
- LLM can identify personal data reliably
- Placeholder replacement works consistently
- The core concept provides value to users

### 1.2 Success Criteria

**USER PERSPECTIVE:**

- ✅ I can input text containing personal information
- ✅ I get back anonymized text with placeholders
- ✅ I can see what was replaced (mapping log)
- ✅ Setup takes < 5 minutes
- ✅ Results are immediately visible and understandable

**ARCHITECT PERSPECTIVE:**

- ✅ Core anonymization algorithm validated
- ✅ LLM integration pattern proven
- ✅ Basic domain model established
- ✅ Foundation for hexagonal architecture prepared
- ✅ Technical risks identified early

### 1.3 Explicit Non-Goals

This iteration deliberately EXCLUDES:

- ❌ No multi-agent workflow (only Agent 1 basic version)
- ❌ No verification or risk assessment
- ❌ No configuration files or CLI
- ❌ No file I/O (only in-memory strings)
- ❌ No chunking strategies
- ❌ No async/await
- ❌ No comprehensive error handling
- ❌ No logging infrastructure
- ❌ No automated tests
- ❌ No GDPR compliance verification
- ❌ No production-ready features

### 1.4 Constraints

- **Code Limit**: Maximum 150 lines of implementation code
- **Dependencies**: Minimal - only LLM provider library + standard library
- **Time to First Result**: < 30 seconds after running demo
- **Setup Complexity**: Single command installation

---

## 2. Functional Requirements - Iteration 1

### 2.1 Core Anonymization (Simplified Agent 1)

#### REQ-I1-F-001: Direct Identifier Detection (PARTIAL)

**Source**: REQ-F-001  
**Status**: PARTIAL IMPLEMENTATION

**Scope for Iteration 1:**

- ✅ **MUST** detect: Names (person names)
- ✅ **MUST** detect: Email addresses
- ✅ **MUST** detect: Phone numbers (basic formats)
- ✅ **MUST** detect: Physical addresses (street addresses)

**Explicitly OUT of Scope:**

- ❌ National IDs (DNI, SSN, passport numbers)
- ❌ IP addresses
- ❌ Device identifiers
- ❌ Account numbers
- ❌ License plates
- ❌ Complex phone number formats (only basic: +X-XXX-XXXX or (XXX) XXX-XXXX)

**User Expectation:**
"I can anonymize common personal data like names, emails, phone numbers, and addresses in a text document."

**Architect Expectation:**
"The LLM prompt effectively identifies the 4 core entity types with >90% accuracy in simple documents."

#### REQ-I1-F-002: Placeholder Format (FULL)

**Source**: REQ-F-002  
**Status**: FULL IMPLEMENTATION

**Specification:**

- Format: `[TYPE_NUMBER]`
- Examples: `[NAME_1]`, `[EMAIL_1]`, `[PHONE_1]`, `[ADDRESS_1]`
- Sequential numbering per type starting from 1
- Uppercase type names
- Square brackets required

**User Expectation:**
"Replaced values are clearly marked with readable placeholders that show what type of data was removed."

**Architect Expectation:**
"Placeholder generation is deterministic and follows a consistent, parseable format."

#### REQ-I1-F-003: Consistency Guarantee (FULL)

**Source**: REQ-F-003  
**Status**: FULL IMPLEMENTATION

**Specification:**

- Same original value → same placeholder throughout document
- Example: "John Smith" appears 3 times → all become `[NAME_1]`
- Mapping maintained in dictionary structure
- No duplicate placeholders for same original value

**User Expectation:**
"If a name appears multiple times in my text, it's replaced with the same placeholder everywhere."

**Architect Expectation:**
"A hash map ensures O(1) lookup and guaranteed consistency across all replacements."

#### REQ-I1-F-004: Basic Readability Preservation (FULL)

**Source**: REQ-F-006  
**Status**: FULL IMPLEMENTATION

**Specification:**

- Sentence structure unchanged
- Punctuation preserved
- Whitespace maintained
- No grammatical errors introduced by replacement

**Scope Limitation:**

- Simple string replacement only
- No advanced NLP for pronoun handling
- No relationship context preservation

**User Expectation:**
"The anonymized text is still readable and makes sense, even though names are replaced."

**Architect Expectation:**
"String replacement algorithm preserves document structure without introducing formatting issues."

### 2.2 Input/Output Interface

#### REQ-I1-F-005: Simple Text Input

**Status**: NEW REQUIREMENT

**Specification:**

- Input: Python string (str type)
- Length: No explicit limit (practical limit ~10KB for iteration 1)
- Encoding: UTF-8
- Format: Plain text only (no markdown, HTML, or rich text)

**User Expectation:**
"I can pass a string of text directly to the function."

**Architect Expectation:**
"Input is a simple Python string with no special preprocessing required."

#### REQ-I1-F-006: Structured Output
**Status**: NEW REQUIREMENT

**Specification:**
Output must be a structured object containing:

- `anonymized_text` (str): The anonymized version of input
- `mappings` (dict): Original value → placeholder mapping
- `original_text` (str): Copy of original for reference

**User Expectation:**
"I get back the anonymized text and can see exactly what was replaced."

**Architect Expectation:**
"Result is a strongly-typed data structure (dataclass or similar) with clear field names."

#### REQ-I1-F-007: Single Function API
**Status**: NEW REQUIREMENT

**Specification:**
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

**User Expectation:**
"There's one simple function I call with my text, and I get results back."

**Architect Expectation:**
"Public API is a single, well-documented function with clear type hints."

### 2.3 LLM Integration (Minimal Agent 1)

#### REQ-I1-F-008: Single LLM Call Strategy
**Source**: REQ-F-013 (simplified)  
**Status**: SIMPLIFIED

**Scope for Iteration 1:**

- Single LLM call to identify all entities at once
- No multiple rounds of refinement
- No self-verification
- No conversation/session management

**Note**: The full system (REQ-F-013) will use 4 consecutive LLM calls (identify, registry, replace, verify), but Iteration 1 simplifies this to a single call that returns JSON with all identified entities and performs replacement in-memory.

**OUT of Scope:**

- Multiple consecutive calls (deferred to Iteration 2)
- Chunking strategies (deferred to Iteration 3)
- Self-verification loop (deferred to Iteration 2)

**User Expectation:**
"The system quickly processes my text without multiple back-and-forth calls."

**Architect Expectation:**
"One synchronous LLM API call returns JSON with all identified entities. The implementation will be refactored in Iteration 2 to support the full multi-call strategy."

#### REQ-I1-F-009: Entity Identification Prompt
**Status**: NEW REQUIREMENT

**Specification:**
LLM prompt must:

- Request JSON format output
- Specify 4 entity types: NAME, EMAIL, PHONE, ADDRESS
- Provide clear examples in prompt
- Request list of objects: `[{"type": "...", "value": "..."}]`

**Quality Target:**

-Parse success rate: >95%
- False positive rate: <10%
- False negative rate: <10% (for the 4 core types)

**User Expectation:**
"The system correctly identifies most names, emails, phones, and addresses in my text."

**Architect Expectation:**
"Prompt engineering produces reliable, parseable JSON output with consistent schema."

#### REQ-I1-F-010: Automatic LLM Provider Selection
**Status**: NEW REQUIREMENT

**Specification:**
System automatically selects first available LLM provider in order:
1. Ollama (if installed and running locally)
2. Claude (if ANTHROPIC_API_KEY environment variable set)
3. OpenAI (if OPENAI_API_KEY environment variable set)

**User Expectation:**
"I don't have to configure anything - it uses whatever LLM I have available."

**Architect Expectation:**
"Simple auto-detection logic with clear error message if no provider available."

### 2.4 Basic Error Handling

#### REQ-I1-F-011: Minimum Viable Error Handling
**Status**: NEW REQUIREMENT

**Specification:**
Handle only critical errors:

- ✅ No LLM provider available → raise ValueError with helpful message
- ✅ LLM returns invalid JSON → raise ValueError with response excerpt
- ✅ Empty input text → return result with empty mappings (no error)

**OUT of Scope:**

-Retry mechanisms
- Graceful degradation
- Partial result recovery
- Detailed error logging

**User Expectation:**
"I get a clear error message if something is misconfigured (like missing API key)."

**Architect Expectation:**
"Basic exception handling prevents cryptic errors; detailed error handling deferred to Iteration 2."

---

## 3. Architectural Requirements - Iteration 1

### 3.1 Code Organization (Minimal Structure)

#### REQ-I1-A-001: Simplified Package Structure
**Source**: REQ-A-092 (simplified)  
**Status**: SIMPLIFIED

**Structure:**
```
anonymization-system/
├── pyproject.toml              # Minimal dependencies only
├── README.md                   # Quick start guide
├── .env.example                # API key examples
├── src/
│   └── anonymization/
│       ├── __init__.py         # Exports: anonymize_simple
│       ├── simple.py           # Main implementation (~80 lines)
│       └── llm.py              # LLM client wrapper (~50 lines)
├── demo.py                     # Runnable examples
└── examples/
    └── sample_texts.py         # 3-4 sample texts for testing
```

**Architect Expectation:**
"Flat structure with minimal files; proper layering deferred to Iteration 2."

#### REQ-I1-A-002: Single Responsibility Files
**Status**: NEW REQUIREMENT

**File Responsibilities:**

-`simple.py`: Core anonymization logic only
  - Entity identification
  - Mapping creation
  - Text replacement
  
- `llm.py`: LLM client abstraction only
  - Provider detection
  - Client initialization
  - Response handling

**Architect Expectation:**
"Clear separation between anonymization logic and LLM communication."

### 3.2 Domain Model (Minimal)

#### REQ-I1-A-003: Basic Domain Model
**Source**: REQ-A-004, REQ-A-005 (minimal)  
**Status**: BASIC IMPLEMENTATION

**Required Model:**
```python
@dataclass
class AnonymizationResult:
    anonymized_text: str
    mappings: Dict[str, str]
    original_text: str
```

**Architect Expectation:**
"Single domain model using dataclass; rich domain model deferred to Iteration 2."

#### REQ-I1-A-004: No External Dependencies in Domain
**Source**: REQ-A-003  
**Status**: PARTIAL

**Specification:**

-`AnonymizationResult` depends only on Python standard library
- No LLM library imports in domain model
- No framework dependencies in domain model

**Architect Expectation:**
"Domain model is pure Python; foundation for dependency inversion in Iteration 2."

### 3.3 LLM Abstraction (Minimal)

#### REQ-I1-A-005: Simple LLM Client Interface
**Source**: REQ-A-018 (simplified)  
**Status**: SIMPLIFIED

**Specification:**
Each LLM client class must provide:

```python
def generate(self, prompt: str) -> str:
    """Send prompt, return text response"""
```

**OUT of Scope:**

-Protocol/interface definitions (Iteration 2)
- Async methods (Iteration 2)
- Session management (Iteration 2)
- Configuration objects (Iteration 2)

**Architect Expectation:**
"Duck-typed interface; formal Protocol definitions in Iteration 2."

#### REQ-I1-A-006: Three LLM Client Implementations
**Source**: REQ-A-020 (simplified)  
**Status**: BASIC IMPLEMENTATION

**Required Clients:**
1. `OllamaClient`: Wraps ollama Python library
2. `ClaudeClient`: Wraps anthropic Python library
3. `OpenAIClient`: Wraps openai Python library

**Each must:**

-Implement `generate(prompt) -> str` method
- Handle library-specific initialization
- Return plain text response

**Architect Expectation:**
"Three concrete classes with identical interface; proper adapter pattern in Iteration 2."

### 3.4 Synchronous Architecture

#### REQ-I1-A-007: Synchronous Execution Only
**Source**: REQ-A-025 (deferred)  
**Status**: SIMPLIFIED

**Specification:**

-All functions are synchronous (no async/await)
- Sequential execution only
- Blocking I/O acceptable

**OUT of Scope:**

-Async/await (Iteration 2)
- Concurrent processing (Iteration 3)
- Event loops (Iteration 2)

**Architect Expectation:**
"Synchronous code for simplicity; async refactoring in Iteration 2 will be straightforward."

### 3.5 Dependency Management

#### REQ-I1-A-008: Minimal Dependencies
**Source**: REQ-A-093 (minimal subset)
**Status**: MINIMAL

**Required Dependencies:**

- Python ≥3.10 (for type hints)
- ONE LLM provider library (user chooses which one to install)

**NO Other Dependencies:**

- No Pydantic (yet)
- No Click (yet)
- No Loguru (yet)
- No pytest (yet)
- No httpx (yet)

**Architect Expectation:**
"Absolute minimum to prove concept; full dependency stack in Iteration 2."

#### REQ-I1-A-009: Optional LLM Dependencies
**Status**: NEW REQUIREMENT

**Specification:**
Use Poetry extras to make LLM providers optional:

```toml
[tool.poetry.extras]
ollama = ["ollama"]
claude = ["anthropic"]
openai = ["openai"]
```

**Installation (user chooses ONE):**
```bash
poetry install -E ollama    # For Ollama users
poetry install -E claude    # For Claude/Anthropic users
poetry install -E openai    # For OpenAI users
```

**Important**: Users should install exactly ONE extra, not all three. The system will auto-detect which provider library is available and use it.

**Architect Expectation:**
"Users install only the LLM provider they have access to; no forced dependency on all providers."

### 3.6 Code Quality (Minimal)

#### REQ-I1-A-010: Documentation Requirements
**Source**: REQ-A-070  
**Status**: FULL IMPLEMENTATION

**Required Documentation:**

-✅ Docstring for `anonymize_simple()` with example
- ✅ Docstrings for all LLM client classes
- ✅ README.md with quick start
- ✅ Inline comments for non-obvious logic

**Architect Expectation:**
"All public APIs documented; internal implementation comments where helpful."

#### REQ-I1-A-011: Type Hints
**Source**: REQ-A-083 (basic)  
**Status**: BASIC

**Required Type Hints:**

-Function signatures (arguments and return types)
- Class attributes in dataclass
- No need for variable annotations yet

**Architect Expectation:**
"Basic type hints for IDE support; strict mypy checking in Iteration 2."

#### REQ-I1-A-012: No Linting/Testing Requirements
**Status**: EXPLICIT EXCLUSION

**NOT Required in Iteration 1:**

-❌ No automated tests
- ❌ No pytest setup
- ❌ No linting (Black, Ruff)
- ❌ No type checking (mypy)
- ❌ No CI/CD

**Architect Expectation:**
"Manual testing only; proper testing infrastructure in Iteration 2."

---

## 4. Implementation Boundaries

### 4.1 Scope Summary

#### IN SCOPE - Must Deliver
1. ✅ `anonymize_simple(text)` function working end-to-end
2. ✅ Detection of 4 entity types: NAME, EMAIL, PHONE, ADDRESS
3. ✅ Placeholder format: `[TYPE_NUMBER]`
4. ✅ Consistency guarantee (same value → same placeholder)
5. ✅ Working integration with at least 1 LLM provider
6. ✅ Auto-detection of available LLM
7. ✅ Structured result object
8. ✅ Runnable demo script
9. ✅ Basic README with setup instructions
10. ✅ Code under 150 lines (excluding comments/blanks)

#### OUT OF SCOPE - Explicitly Deferred
1. ❌ Agent 2 (verification)
2. ❌ Agent 3 (risk assessment)
3. ❌ Multi-agent orchestration
4. ❌ Configuration files (YAML)
5. ❌ CLI interface
6. ❌ File I/O operations
7. ❌ Indirect identifiers (dates, job titles)
8. ❌ Chunking strategies
9. ❌ Async/await
10. ❌ Comprehensive error handling
11. ❌ Logging infrastructure
12. ❌ Automated tests
13. ❌ GDPR compliance verification
14. ❌ Multiple LLM calls per agent
15. ❌ Context-aware anonymization

### 4.2 Quality Targets

#### Performance
- **Target**: Process 100-word document in < 5 seconds
- **Measurement**: Manual timing with demo script
- **Rationale**: Proof of concept; optimization in Iteration 3

#### Accuracy (Manual Assessment)
- **Target**: Correctly identify >90% of names, emails, phones, addresses in demo texts
- **Measurement**: Visual inspection of 5-10 sample texts
- **Rationale**: No formal accuracy metrics yet; testing framework in Iteration 2

#### Reliability
- **Target**: Demo script runs successfully 10/10 times with valid setup
- **Measurement**: Manual repeated execution
- **Rationale**: Basic reliability check; comprehensive testing in Iteration 2

#### Usability
- **Target**: New developer can run demo in < 5 minutes following README
- **Measurement**: Time from git clone to seeing results
- **Rationale**: Early user experience validation

---

## 5. Demo Requirements

### 5.1 Demo Script Specifications

#### REQ-I1-D-001: Runnable Demo
**Status**: NEW REQUIREMENT

**Specification:**
Demo script (`demo.py`) must:

- Run without command-line arguments
- Display 2-3 example anonymizations
- Show original text, anonymized text, and mappings
- Use clear visual separators between examples
- Complete execution in < 30 seconds

**User Expectation:**
"I run one command and immediately see anonymization working with clear before/after examples."

#### REQ-I1-D-002: Example Text Variety
**Status**: NEW REQUIREMENT

**Required Examples:**

1. **Simple - Customer Support Ticket**:
   - Single person with name, email, phone, address
   - Example: "Customer John Smith (john.smith@email.com, 555-123-4567) reported an issue with his account. He lives at 123 Main Street, Springfield."

2. **Multiple People - Team Introduction**:
   - 2-3 people mentioned with various details
   - Example: "Our team consists of Sarah Johnson (sarah.j@company.com) from the New York office and Mike Chen (mike.chen@company.com, +1-415-555-9876) from San Francisco. Sarah can also be reached at 212-555-3344."

3. **Real-World - Meeting Notes**:
   - Meeting notes or email excerpt with mixed personal data
   - Example: "Meeting scheduled for next Tuesday with Dr. Emily Rodriguez at her office located at 456 Oak Avenue, Boston MA. Please confirm attendance by emailing emily.rodriguez@hospital.org or calling (617) 555-7890. Emily mentioned she'll bring documents from the last consultation."

**Each example must:**

- Be 3-10 sentences
- Contain 3-10 identifiable entities
- Demonstrate placeholder consistency (same name appearing multiple times)

**Architect Expectation:**
"Concrete examples validate different use cases and provide immediate visual proof of concept."

### 5.2 Documentation Requirements

#### REQ-I1-D-003: Quick Start README
**Status**: NEW REQUIREMENT

**Required Sections:**
1. **Installation** (5 lines max)
   - Git clone command
   - Poetry install command
   - Environment variable setup (if needed)

2. **Usage** (10 lines max)
   - How to run demo
   - How to use in Python code (1 example)

3. **Requirements** (3 lines)
   - Python version
   - LLM provider needed

**User Expectation:**
"README tells me exactly what to do in under 1 minute of reading."

#### REQ-I1-D-004: Environment Variable Example
**Status**: NEW REQUIREMENT

**File**: `.env.example`
```
# For Claude (Anthropic)
ANTHROPIC_API_KEY=your_api_key_here

# For OpenAI
OPENAI_API_KEY=your_api_key_here

# For Ollama (no key needed if running locally)
```

**User Expectation:**
"I can see exactly what environment variables I need to set."

---

## 6. Acceptance Criteria

### 6.1 Functional Acceptance

**The iteration is considered functionally complete when:**

1. ✅ A developer can run `poetry install -E <provider>` successfully
2. ✅ A developer can run `poetry run python demo.py` and see results
3. ✅ The demo displays at least 2 different text examples
4. ✅ Names are replaced with `[NAME_X]` placeholders
5. ✅ Emails are replaced with `[EMAIL_X]` placeholders
6. ✅ Phone numbers are replaced with `[PHONE_X]` placeholders
7. ✅ Addresses are replaced with `[ADDRESS_X]` placeholders
8. ✅ Same value appears with same placeholder consistently
9. ✅ Mapping log shows all replacements clearly
10. ✅ Anonymized text is readable and makes sense

### 6.2 Technical Acceptance

**The iteration is considered technically complete when:**

1. ✅ Code is ≤150 lines (excluding comments, docstrings, blank lines)
2. ✅ All public functions have docstrings
3. ✅ Type hints present on function signatures
4. ✅ Works with at least 1 LLM provider (Ollama OR Claude OR OpenAI)
5. ✅ No crashes or exceptions in normal operation
6. ✅ README instructions are accurate and complete
7. ✅ Demo completes in <30 seconds
8. ✅ Code organization follows specified structure

### 6.3 User Experience Acceptance

**The iteration is considered UX-complete when:**

1. ✅ Setup time from clone to first result: <5 minutes
2. ✅ Error message for missing API key is clear and actionable
3. ✅ Demo output is visually clear with appropriate formatting
4. ✅ Mapping log is easy to read and understand
5. ✅ A non-expert can follow README and succeed

---

## 7. Risks and Mitigations

### 7.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM returns unparseable JSON | HIGH | HIGH | Add clear JSON format examples in prompt; implement basic error handling |
| LLM misses obvious entities | MEDIUM | MEDIUM | Refine prompt with explicit instructions; accept as iteration 1 limitation |
| String replacement breaks formatting | LOW | MEDIUM | Test with various document structures; fix issues found |
| No LLM provider available | LOW | HIGH | Clear error message directing user to setup instructions |

### 7.2 Scope Creep Risks

| Risk | Mitigation |
|------|------------|
| Temptation to add Agent 2 | Strict adherence to iteration scope; defer to Iteration 2 plan |
| Temptation to add config files | Remind: goal is MINIMAL working demo |
| Temptation to add tests | Document test scenarios for Iteration 2 instead |
| Temptation to improve error handling | Fix only critical errors; comprehensive handling in Iteration 2 |

---

## 8. Definition of Done

### 8.1 Code Complete
- [ ] All code files present per structure specification
- [ ] Code compiles/runs without syntax errors
- [ ] No missing imports or undefined variables
- [ ] Code passes manual review for basic quality

### 8.2 Documentation Complete
- [ ] README.md written with all required sections
- [ ] All public functions have docstrings
- [ ] .env.example file present
- [ ] Inline comments added where logic is non-obvious

### 8.3 Demo Complete
- [ ] demo.py runs successfully
- [ ] Displays at least 2 examples
- [ ] Output is clear and formatted
- [ ] Takes <30 seconds to complete

### 8.4 Validation Complete
- [ ] Tested with at least 1 LLM provider
- [ ] Manual testing with 5+ different texts shows >90% accuracy
- [ ] README instructions verified by following exactly
- [ ] All 10 functional acceptance criteria met
- [ ] All 8 technical acceptance criteria met
- [ ] All 5 UX acceptance criteria met

---

## 9. Transition to Iteration 2

### 9.1 Handoff Artifacts

Upon completion of Iteration 1, the following must be delivered to Iteration 2:

1. **Working codebase** matching all specifications
2. **Iteration 1 Completion Report** documenting:
   - What worked well
   - What didn't work
   - Accuracy assessment results
   - Performance measurements
   - Identified technical debt
3. **Known Limitations** document listing:
   - Entity types not covered
   - Edge cases that fail
   - Error conditions not handled
4. **Lessons Learned** for prompt engineering:
   - What prompts worked best
   - What LLM behaviors were observed
   - Recommendations for Agent 2 and 3 prompts

### 9.2 Open Questions for Iteration 2

Document answers to:
1. Which LLM provider performed best for entity identification?
2. What was the false positive/negative rate in practice?
3. What prompt refinements improved accuracy most?
4. What document structures caused issues?
5. What additional entity types are most needed?

---

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-03 | Initial iteration 1 requirements | Requirements Team |

---

**NEXT DOCUMENT**: Iteration 2 Requirements (to be created after Iteration 1 completion)