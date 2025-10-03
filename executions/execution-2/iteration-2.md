# Iteration 2 Requirements Package - Validation Agent

**Project**: GDPR Text Anonymization System  
**Iteration**: 2 of 5  
**Date**: 2025-10-03  
**Status**: READY FOR IMPLEMENTATION  
**Previous**: [Iteration 1 Complete](Iteration%201%20Implementation%20-%20Complete%20✅.md)

---

## 1. Overview

### 1.1 Purpose

Add a verification layer (Agent 2) that independently scans anonymized documents to detect any remaining direct identifiers missed by Agent 1, ensuring higher anonymization quality.

### 1.2 Business Value

- **Quality Assurance**: Catch Agent 1's mistakes before documents are released
- **Risk Reduction**: Prevent GDPR violations from missed identifiers
- **Trust Building**: Dual-verification increases stakeholder confidence
- **Measurable Quality**: Quantifiable accuracy metrics (recall, precision)

### 1.3 Success Criteria

**MUST ACHIEVE:**

- Agent 2 achieves ≥90% recall on test corpus (detects 90% of remaining identifiers)
- Agent 2 achieves ≥85% precision (85% of reported issues are real)
- Independent operation (no Agent 1 context leaked)
- Structured, machine-readable results

**SHOULD ACHIEVE:**

- ≥95% recall on test corpus
- ≥90% precision
- Processing time <10 seconds for typical documents

### 1.4 Non-Goals (Explicitly OUT of Scope)

- ❌ Orchestrated retry loop (deferred to Iteration 3)
- ❌ Agent configuration system (deferred to Iteration 3)
- ❌ Risk assessment (deferred to Iteration 4)
- ❌ Multi-document processing
- ❌ Async/parallel processing
- ❌ CLI interface
- ❌ File I/O operations

### 1.5 Dependencies

**Prerequisites:**

- Iteration 1 implementation complete and tested
- LLM provider configured (Ollama, Claude, or OpenAI)
- Python 3.10+

**Integration Points:**

- Uses same LLM client from `src/anonymization/llm.py`
- Consumes output from Agent 1 (`AnonymizationResult`)
- No direct communication between Agent 1 and Agent 2

---

## 2. Functional Requirements

### 2.1 Agent 2 - Direct Identifier Verification

**Requirement ID**: REQ-I2-F-001  
**Priority**: MUST  
**Type**: Core Functionality

**Description**:  
Agent 2 independently scans anonymized text to detect remaining direct identifiers.

**Scope of Detection**:

Direct identifiers only (same 4 types as Agent 1):

- **Names**: Person names (first, last, full names)
- **Emails**: Email addresses (any format)
- **Phone Numbers**: Phone numbers (any format/region)
- **Addresses**: Physical addresses (street, city, postal codes)

**Behavioral Contract**:

```text
Function: validate_anonymization

INPUT:
  • anonymized_text: String
    - The text after Agent 1 processing
    - May contain placeholders ([NAME_1], [EMAIL_2], etc.)
    - May still contain missed identifiers

PROCESSING RULES:
  1. Scan text character-by-character for identifiers
  2. IGNORE existing placeholders (pattern: [TYPE_NUMBER])
  3. For each remaining identifier found:
     a. Classify type (NAME|EMAIL|PHONE|ADDRESS)
     b. Extract exact value
     c. Capture context (±20 characters around it)
     d. Record location hint (paragraph/line reference)
  4. Compute overall confidence score
  5. Generate human-readable reasoning

OUTPUT: ValidationResult
  • passed: Boolean
    - true: No remaining identifiers found
    - false: One or more identifiers remain
  • issues: List[Issue]
    - Empty list if passed=true
    - One Issue per remaining identifier if passed=false
  • agent_reasoning: String
    - Explanation of findings
    - Must be non-empty
  • confidence: Float (0.0-1.0)
    - Agent's confidence in its analysis
    - Lower confidence suggests ambiguous cases

INDEPENDENCE REQUIREMENT:
  - Agent 2 MUST NOT receive:
    • Original unredacted text
    • Agent 1's entity list
    • Agent 1's replacement mappings
    • Agent 1's reasoning
  - Agent 2 operates solely on anonymized output
```

**Edge Cases**:

| Case              | Input                                     | Expected Output                                                         |
| ----------------- | ----------------------------------------- | ----------------------------------------------------------------------- |
| Empty string      | `""`                                      | `passed=true, issues=[], reasoning="Empty document"`                    |
| Only placeholders | `"[NAME_1] contacted [EMAIL_1]"`          | `passed=true, issues=[], reasoning="All identifiers properly replaced"` |
| Mixed content     | `"[NAME_1] and John contacted [EMAIL_1]"` | `passed=false, issues=[Issue(type=NAME, value="John", ...)]`            |
| No identifiers    | `"The system processed 42 records."`      | `passed=true, issues=[], reasoning="No identifiers detected"`           |

**Error Handling**:

- Invalid input (None, non-string) → Raise `ValueError`
- LLM communication failure → Raise `LLMProviderError`
- Malformed LLM response → Retry once, then raise `ValidationError`

---

### 2.2 Demo Integration

**Requirement ID**: REQ-I2-F-002  
**Priority**: MUST  
**Type**: User-Facing

**Description**:  
Update `demo.py` to demonstrate dual-agent workflow.

**Demo Flow**:

```text
FOR EACH sample text:
  1. Display original text
  2. Run Agent 1 (anonymize_simple)
  3. Display Agent 1 result + mappings
  4. Run Agent 2 (validate_anonymization)
  5. Display Agent 2 result:
     IF passed=true:
       ✅ "Verification PASSED - No remaining identifiers"
     IF passed=false:
       ❌ "Verification FAILED - Found N remaining identifiers:"
       FOR EACH issue:
         • Display: type, value, context, location
  6. Visual separator between examples
```

**Output Format Requirements**:

- Clear visual distinction between Agent 1 and Agent 2 outputs
- Color coding (if terminal supports): green for passed, red for failed
- Unicode symbols: ✅ for success, ❌ for failure
- Preserve existing Agent 1 output format

---

## 3. Interface Contracts

### 3.1 Validation Function Interface

**Interface Name**: `validate_anonymization`  
**Location**: `src/anonymization/validation.py`  
**Purpose**: Public API for Agent 2 verification

```text
Function: validate_anonymization

Signature:
  validate_anonymization(anonymized_text: str) -> ValidationResult

Parameters:
  anonymized_text: str
    - The text after Agent 1 processing
    - Must be non-None (raises ValueError if None)
    - Empty string is valid input

Returns:
  ValidationResult
    - Immutable data structure
    - See section 4.1 for complete specification

Raises:
  ValueError:
    - If anonymized_text is None
    - If anonymized_text is not a string

  LLMProviderError:
    - If LLM client is not available
    - If LLM communication fails after retry

  ValidationError:
    - If LLM response cannot be parsed
    - If LLM response is malformed after retry

Side Effects:
  - Makes 1 LLM API call
  - No file I/O
  - No global state modification
  - No caching (intentionally stateless)

Performance:
  - Expected: 2-10 seconds for typical documents (200-500 words)
  - Timeout: 30 seconds per LLM call
  - No explicit timeout enforcement (rely on LLM client)

Idempotency:
  - NO (LLM may return different results)
  - Same input may produce different confidence scores
  - Same input should produce same pass/fail outcome
```

---

## 4. Data Structures

### 4.1 ValidationResult

**Structure Name**: `ValidationResult`  
**Location**: `src/anonymization/validation.py`  
**Type**: Dataclass (immutable via `frozen=True`)  
**Purpose**: Agent 2 verification outcome

```text
Data Structure: ValidationResult

Fields:
┌─────────────────┬───────────────┬──────────┬────────────────────────────┐
│ Field           │ Type          │ Required │ Description                │
├─────────────────┼───────────────┼──────────┼────────────────────────────┤
│ passed          │ bool          │ Yes      │ True if no remaining IDs   │
│ issues          │ list[Issue]   │ Yes      │ Empty if passed=True       │
│ agent_reasoning │ str           │ Yes      │ Human-readable explanation │
│ confidence      │ float         │ Yes      │ Range: 0.0-1.0 inclusive   │
└─────────────────┴───────────────┴──────────┴────────────────────────────┘

Validation Rules:
  IF passed == True:
    THEN issues MUST be empty list []

  IF passed == False:
    THEN len(issues) MUST be >= 1

  confidence MUST satisfy: 0.0 <= confidence <= 1.0

  agent_reasoning MUST be non-empty string (len > 0)

Immutability:
  - Use @dataclass(frozen=True)
  - All fields must be immutable types
  - issues field: use tuple instead of list for immutability

Example - Success:
  ValidationResult(
    passed=True,
    issues=[],
    agent_reasoning="No remaining identifiers detected. All personal data properly anonymized.",
    confidence=0.95
  )

Example - Failure:
  ValidationResult(
    passed=False,
    issues=[
      Issue(identifier_type="EMAIL", value="john@example.com", ...),
      Issue(identifier_type="PHONE", value="555-0123", ...)
    ],
    agent_reasoning="Found 2 remaining identifiers: 1 email address and 1 phone number that were not replaced by Agent 1.",
    confidence=0.88
  )
```

### 4.2 Issue

**Structure Name**: `Issue`  
**Location**: `src/anonymization/validation.py`  
**Type**: Dataclass (immutable via `frozen=True`)  
**Purpose**: Single remaining identifier found by Agent 2

```text
Data Structure: Issue

Fields:
┌─────────────────┬────────┬──────────┬─────────────────────────────┐
│ Field           │ Type   │ Required │ Description                 │
├─────────────────┼────────┼──────────┼─────────────────────────────┤
│ identifier_type │ str    │ Yes      │ "NAME" | "EMAIL" |          │
│                 │        │          │ "PHONE" | "ADDRESS"         │
│ value           │ str    │ Yes      │ The actual identifier text  │
│ context         │ str    │ Yes      │ ±20 characters around it    │
│ location_hint   │ str    │ Yes      │ Human-readable location     │
└─────────────────┴────────┴──────────┴─────────────────────────────┘

Field Specifications:

identifier_type:
  - Must be one of: "NAME", "EMAIL", "PHONE", "ADDRESS"
  - Uppercase only
  - No other values permitted

value:
  - The exact identifier text as found in document
  - Trimmed of leading/trailing whitespace
  - Preserves internal spacing
  - Maximum length: 500 characters

context:
  - Extract ±20 characters around the identifier
  - If identifier near start/end of document, show what's available
  - Include "..." prefix if truncated at start
  - Include "..." suffix if truncated at end
  - Purpose: Help human reviewer locate the issue

location_hint:
  - Human-readable description of location
  - Format examples:
    * "paragraph 3"
    * "paragraph 2, line 5"
    * "near beginning"
    * "end of document"
  - Not required to be machine-parseable
  - Purpose: Help human reviewer navigate to issue

Example:
  Issue(
    identifier_type="EMAIL",
    value="support@company.com",
    context="...please contact support@company.com for assistance...",
    location_hint="paragraph 4, line 2"
  )
```

---

## 5. Configuration

### 5.1 Configuration Changes

**Requirement ID**: REQ-I2-C-001  
**Priority**: SHOULD (Optional for Iteration 2)  
**Type**: Enhancement

**Description**:  
Configuration system is OUT of scope for Iteration 2, but document expected structure for Iteration 3.

**Future Configuration Format** (for reference only):

```yaml
# config.yaml - NOT IMPLEMENTED IN ITERATION 2

agents:
  agent2:
    name: "DIRECT-CHECK"
    enabled: true
    strictness: "normal" # strict | normal | lenient
    confidence_threshold: 0.8 # 0.0-1.0


  # Strictness behavior:
  # - strict: Flag anything that might be an identifier
  # - normal: Balanced approach (recommended)
  # - lenient: Only flag obvious identifiers
```

**Iteration 2 Approach**:

- ✅ Hardcoded "normal" strictness
- ✅ No configuration file
- ✅ No command-line arguments
- ✅ Document planned config for Iteration 3

---

## 6. Behavioral Requirements

### 6.1 Agent 2 Processing Flow

**Requirement ID**: REQ-I2-B-001  
**Priority**: MUST  
**Type**: Core Behavior

**Flow Specification**:

```text
FUNCTION: validate_anonymization(anonymized_text: str) -> ValidationResult

STEP 1: Input Validation
  IF anonymized_text is None:
    → RAISE ValueError("anonymized_text cannot be None")

  IF anonymized_text is not string:
    → RAISE ValueError("anonymized_text must be a string")

  IF anonymized_text is empty string:
    → RETURN ValidationResult(
        passed=True,
        issues=[],
        agent_reasoning="Empty document, nothing to validate",
        confidence=1.0
      )

STEP 2: LLM Client Initialization
  TRY:
    client = get_llm_client()
  EXCEPT RuntimeError as e:
    → RAISE LLMProviderError(f"No LLM provider available: {e}")

STEP 3: Construct LLM Prompt
  Build prompt with:
    • Instruction: "Scan for remaining identifiers"
    • Context: "Text has already been anonymized"
    • Task: "Find any missed identifiers"
    • Format: "Return JSON with structure {...}"
    • Examples: Show 2-3 example responses

  See section 6.2 for complete prompt specification

STEP 4: LLM Call (with retry)
  attempt = 1
  max_attempts = 2

  WHILE attempt <= max_attempts:
    TRY:
      response = client.complete(prompt)
      json_data = parse_json(response)

      IF json_data is valid:
        → GO TO STEP 5
      ELSE:
        attempt += 1
        IF attempt > max_attempts:
          → RAISE ValidationError("Invalid LLM response after retries")

    EXCEPT LLMError:
      attempt += 1
      IF attempt > max_attempts:
        → RAISE LLMProviderError("LLM call failed after retries")

STEP 5: Parse LLM Response
  Extract from json_data:
    • passed: boolean
    • issues: array
    • reasoning: string
    • confidence: float

  Validate structure:
    IF passed == true AND len(issues) > 0:
      → SET passed = false  # LLM made an error

    IF passed == false AND len(issues) == 0:
      → SET passed = true   # LLM made an error

    IF confidence not in [0.0, 1.0]:
      → CLAMP to range

STEP 6: Create Issue Objects
  issues_list = []

  FOR EACH issue in json_data['issues']:
    issue_obj = Issue(
      identifier_type=issue['type'],
      value=issue['value'],
      context=issue['context'],
      location_hint=issue['location']
    )
    issues_list.append(issue_obj)

STEP 7: Return Result
  RETURN ValidationResult(
    passed=parsed_passed,
    issues=issues_list,
    agent_reasoning=parsed_reasoning,
    confidence=parsed_confidence
  )

END FUNCTION
```

**Performance Characteristics**:

- Single LLM call per validation
- No iterative refinement
- No caching
- Stateless execution

---

### 6.2 LLM Prompt Specification

**Requirement ID**: REQ-I2-B-002  
**Priority**: MUST  
**Type**: Core Behavior

**Prompt Structure**:

```text
PROMPT TEMPLATE:

You are a GDPR compliance verification agent. Your task is to scan an ANONYMIZED document and identify any REMAINING direct identifiers that were not properly replaced.

IMPORTANT CONTEXT:
- This document has ALREADY been processed by an anonymization agent
- You will see placeholders like [NAME_1], [EMAIL_2], [PHONE_3], [ADDRESS_4]
- These placeholders are CORRECT and should be IGNORED
- Your job is to find identifiers that were MISSED

DIRECT IDENTIFIERS TO DETECT:
1. NAMES: Person names (first, last, full)
2. EMAILS: Email addresses
3. PHONES: Phone numbers (any format)
4. ADDRESSES: Physical addresses

DO NOT FLAG:
- Existing placeholders ([NAME_X], [EMAIL_X], etc.)
- Generic terms (person, customer, user)
- Company names or product names
- Job titles

DOCUMENT TO VERIFY:
---
{anonymized_text}
---

RESPOND IN JSON FORMAT:
{
  "passed": boolean,
  "issues": [
    {
      "type": "NAME|EMAIL|PHONE|ADDRESS",
      "value": "the actual identifier found",
      "context": "±20 chars around it",
      "location": "paragraph X"
    }
  ],
  "reasoning": "explanation of findings",
  "confidence": 0.0 to 1.0
}

EXAMPLES:

Example 1 - All identifiers replaced:
Document: "[NAME_1] contacted [EMAIL_1] about the issue."
Response: {
  "passed": true,
  "issues": [],
  "reasoning": "All identifiers properly anonymized.",
  "confidence": 0.95
}

Example 2 - Missed identifier:
Document: "[NAME_1] and John contacted [EMAIL_1]."
Response: {
  "passed": false,
  "issues": [
    {
      "type": "NAME",
      "value": "John",
      "context": "[NAME_1] and John contacted",
      "location": "paragraph 1"
    }
  ],
  "reasoning": "Found 1 remaining name that was not anonymized.",
  "confidence": 0.88
}

Now verify the document above.
```

**Prompt Engineering Notes**:

- Emphasize independence (no original document context)
- Clarify placeholder format to avoid false positives
- Provide clear JSON schema
- Include examples for clarity
- Use structured output format

---

## 7. Quality Criteria

### 7.1 Agent 2 Verification Recall

**Metric ID**: QM-I2-001  
**Priority**: MUST  
**Type**: Functional Quality

**Definition**:  
Proportion of actual remaining identifiers that Agent 2 successfully detects.

**Formula**:

```text
Recall = True Positives / (True Positives + False Negatives)

Where:
  True Positive (TP)  = Agent 2 correctly identifies remaining identifier
  False Negative (FN) = Agent 2 misses a remaining identifier
```

**Target Metrics**:

| Level   | Threshold | Priority     |
| ------- | --------- | ------------ |
| Minimum | 90%       | MUST         |
| Target  | 95%       | SHOULD       |
| Stretch | 98%       | NICE-TO-HAVE |

**Test Procedure**:

```text
TEST: Agent 2 Recall Measurement

SETUP:
  1. Prepare 50 test documents
  2. Each document contains 3-5 deliberately missed identifiers
  3. Total corpus: ~200 identifiers
  4. Distribution:
     • 40% Names (80 instances)
     • 30% Emails (60 instances)
     • 20% Phones (40 instances)
     • 10% Addresses (20 instances)

EXECUTION:
  FOR EACH test document:
    1. Run validate_anonymization(document)
    2. Extract Agent 2's findings (issues list)
    3. Compare against ground truth
    4. Classify each ground truth identifier:
       • TP: Agent 2 found it
       • FN: Agent 2 missed it

CALCULATION:
  Overall Recall = TP_total / (TP_total + FN_total)

  Per-Category Recall:
    Recall_NAME = TP_name / (TP_name + FN_name)
    Recall_EMAIL = TP_email / (TP_email + FN_email)
    Recall_PHONE = TP_phone / (TP_phone + FN_phone)
    Recall_ADDRESS = TP_address / (TP_address + FN_address)

ACCEPTANCE CRITERIA:
  MUST PASS:
    • Overall recall >= 90%
    • Each category recall >= 85%

  SHOULD PASS:
    • Overall recall >= 95%
    • Each category recall >= 90%

FAILURE RESPONSE:
  IF recall < 90%:
    1. Analyze false negatives by category
    2. Identify pattern in missed identifiers
    3. Refine Agent 2 prompt
    4. Re-test with same corpus
    5. IF still < 90% after 3 iterations:
       → Escalate to architect

EXAMPLE RESULT:
  Test Corpus: 200 identifiers
  Agent 2 Found: 190 identifiers
  Agent 2 Missed: 10 identifiers

  Overall Recall = 190/200 = 95% ✅ PASS

  Breakdown:
    NAME: 75/80 = 93.75% ✅
    EMAIL: 58/60 = 96.67% ✅
    PHONE: 38/40 = 95% ✅
    ADDRESS: 19/20 = 95% ✅
```

**Test Data Requirements**:

- Documents must be realistic (based on real use cases)
- Identifiers must be in natural contexts
- Include edge cases:
  - Names with prefixes (Dr., Mr.)
  - International phone formats
  - Email addresses with special characters
  - Multi-line addresses

---

### 7.2 Agent 2 Verification Precision

**Metric ID**: QM-I2-002  
**Priority**: MUST  
**Type**: Functional Quality

**Definition**:  
Proportion of Agent 2's reported issues that are real problems (not false alarms).

**Formula**:

```text
Precision = True Positives / (True Positives + False Positives)

Where:
  True Positive (TP)  = Agent 2 correctly flags remaining identifier
  False Positive (FP) = Agent 2 incorrectly flags something as identifier
```

**Target Metrics**:

| Level   | Threshold | Priority     |
| ------- | --------- | ------------ |
| Minimum | 85%       | MUST         |
| Target  | 90%       | SHOULD       |
| Stretch | 95%       | NICE-TO-HAVE |

**Test Procedure**:

```text
TEST: Agent 2 Precision Measurement

SETUP:
  1. Prepare 100 test documents:
     • 50 documents: Fully anonymized (clean)
     • 50 documents: Contains remaining identifiers
  2. Label ground truth for all documents

EXECUTION:
  FOR EACH test document:
    1. Run validate_anonymization(document)
    2. Extract Agent 2's findings
    3. Manually verify EACH reported issue:
       • TP: Real remaining identifier
       • FP: False alarm (placeholder, generic term, etc.)

CALCULATION:
  Precision = TP / (TP + FP)

ACCEPTANCE CRITERIA:
  MUST PASS:
    • Precision >= 85%

  SHOULD PASS:
    • Precision >= 90%

FAILURE RESPONSE:
  IF precision < 85%:
    1. Analyze false positives by type
    2. Common causes:
       • Flagging existing placeholders
       • Flagging generic terms
       • Flagging company/product names
    3. Refine prompt to reduce false positives
    4. Re-test
    5. IF still < 85% after 3 iterations:
       → Escalate to architect

EXAMPLE RESULT:
  Test Run: 100 documents
  Agent 2 Reported: 120 issues
  Real Issues (TP): 108
  False Alarms (FP): 12

  Precision = 108/120 = 90% ✅ PASS
```

---

### 7.3 Processing Time

**Metric ID**: QM-I2-003  
**Priority**: SHOULD  
**Type**: Performance

**Definition**:  
Total time from function call to return for `validate_anonymization`.

**Target Metrics**:

| Document Size          | Mean Time | P95 Time | Priority |
| ---------------------- | --------- | -------- | -------- |
| Small (100-200 words)  | <5s       | <10s     | SHOULD   |
| Medium (200-500 words) | <8s       | <15s     | SHOULD   |
| Large (up to 10KB)     | <15s      | <30s     | SHOULD   |

**Test Procedure**:

```text
TEST: Processing Time Measurement

SETUP:
  1. Prepare 60 documents:
     • 20 small (100-200 words)
     • 20 medium (200-500 words)
     • 20 large (up to 10KB)

EXECUTION:
  FOR EACH document:
    start_time = current_time()
    result = validate_anonymization(document)
    end_time = current_time()
    duration = end_time - start_time
    record(document_size, duration)

CALCULATION:
  FOR EACH size category:
    mean_time = average(durations)
    p95_time = 95th_percentile(durations)

ACCEPTANCE CRITERIA:
  SHOULD PASS (not blocking):
    • Small: mean <5s, p95 <10s
    • Medium: mean <8s, p95 <15s
    • Large: mean <15s, p95 <30s

NOTE: Performance optimization is NOT required for Iteration 2.
      Collect baseline metrics for future optimization.
```

---

## 8. Acceptance Criteria

### 8.1 Functional Acceptance

**Test Execution**: Manual testing with demo script

| #   | Criterion                                   | Test Method         | Priority |
| --- | ------------------------------------------- | ------------------- | -------- |
| 1   | `validate_anonymization` function exists    | Import test         | MUST     |
| 2   | Returns `ValidationResult` object           | Type check          | MUST     |
| 3   | Detects remaining names                     | Test with sample    | MUST     |
| 4   | Detects remaining emails                    | Test with sample    | MUST     |
| 5   | Detects remaining phones                    | Test with sample    | MUST     |
| 6   | Detects remaining addresses                 | Test with sample    | MUST     |
| 7   | Ignores existing placeholders               | Test with clean doc | MUST     |
| 8   | Returns `passed=True` for clean docs        | Test with clean doc | MUST     |
| 9   | Returns `passed=False` when issues found    | Test with bad doc   | MUST     |
| 10  | `issues` list empty when `passed=True`      | Verify invariant    | MUST     |
| 11  | `issues` list non-empty when `passed=False` | Verify invariant    | MUST     |
| 12  | Demo runs without errors                    | Execute `demo.py`   | MUST     |
| 13  | Demo shows both agents                      | Visual inspection   | MUST     |
| 14  | Demo clearly shows pass/fail                | Visual inspection   | MUST     |

### 8.2 Technical Acceptance

**Test Execution**: Code review + static analysis

| #   | Criterion                                 | Test Method     | Priority |
| --- | ----------------------------------------- | --------------- | -------- |
| 1   | Code in `src/anonymization/validation.py` | File exists     | MUST     |
| 2   | Dataclasses are frozen (immutable)        | Code review     | MUST     |
| 3   | Type hints on all public functions        | Static analysis | MUST     |
| 4   | Docstrings on all public functions        | Code review     | MUST     |
| 5   | Zero Pylance errors                       | Pylance check   | MUST     |
| 6   | Uses existing LLM client                  | Code review     | MUST     |
| 7   | No Agent 1 context leak                   | Code review     | MUST     |
| 8   | Proper error handling                     | Code review     | MUST     |
| 9   | Follows PEP 8                             | Linter check    | SHOULD   |
| 10  | Code <200 lines (target)                  | Line count      | SHOULD   |

### 8.3 Quality Acceptance

**Test Execution**: Evaluation on test corpus

| #   | Criterion                      | Test Method   | Priority |
| --- | ------------------------------ | ------------- | -------- |
| 1   | Recall ≥ 90% on test corpus    | Run QM-I2-001 | MUST     |
| 2   | Precision ≥ 85% on test corpus | Run QM-I2-002 | MUST     |
| 3   | Per-category recall ≥ 85%      | Run QM-I2-001 | MUST     |
| 4   | Recall ≥ 95%                   | Run QM-I2-001 | SHOULD   |
| 5   | Precision ≥ 90%                | Run QM-I2-002 | SHOULD   |
| 6   | P95 time <30s for 10KB docs    | Run QM-I2-003 | SHOULD   |

---

## 9. Definition of Done

### 9.1 Code Complete

- [ ] `src/anonymization/validation.py` created
- [ ] `ValidationResult` dataclass implemented (frozen)
- [ ] `Issue` dataclass implemented (frozen)
- [ ] `validate_anonymization()` function implemented
- [ ] LLM prompt designed and tested
- [ ] Demo script updated with dual-agent flow
- [ ] Zero Pylance errors
- [ ] All type hints in place
- [ ] All docstrings complete

### 9.2 Documentation Complete

- [ ] README updated with Agent 2 usage
- [ ] Code comments for complex logic
- [ ] Docstrings follow Google style
- [ ] Examples in docstrings

### 9.3 Testing Complete

- [ ] Manual testing with 3+ sample texts
- [ ] Recall test executed (QM-I2-001)
- [ ] Precision test executed (QM-I2-002)
- [ ] All acceptance criteria verified
- [ ] Test results documented

### 9.4 Quality Gates Passed

- [ ] Recall ≥ 90% (MUST)
- [ ] Precision ≥ 85% (MUST)
- [ ] Zero Pylance errors (MUST)
- [ ] Code review complete (MUST)

### 9.5 Handoff Ready

- [ ] All "MUST" criteria passed
- [ ] Test results documented
- [ ] Known issues documented
- [ ] Recommendations for Iteration 3 documented

---

## 10. Implementation Guidance

### 10.1 Recommended Approach

**Step 1: Create Data Structures (30 minutes)**

```text
File: src/anonymization/validation.py

1. Define Issue dataclass:
   - 4 fields: identifier_type, value, context, location_hint
   - frozen=True for immutability
   - Type hints on all fields

2. Define ValidationResult dataclass:
   - 4 fields: passed, issues, agent_reasoning, confidence
   - frozen=True for immutability
   - Type hints on all fields
   - Add __post_init__ validation if needed
```

**Step 2: Implement LLM Prompt (1 hour)**

```text
1. Create prompt template as multi-line string
2. Include clear instructions
3. Specify JSON response format
4. Add 2-3 examples
5. Test prompt manually with LLM provider
6. Refine based on initial results
```

**Step 3: Implement validate_anonymization (2 hours)**

```text
1. Input validation
2. Get LLM client (reuse from llm.py)
3. Construct prompt with template
4. Call LLM with retry logic
5. Parse JSON response
6. Handle malformed responses
7. Create Issue objects
8. Return ValidationResult
```

**Step 4: Update Demo (30 minutes)**

```text
1. Import validate_anonymization
2. Add Agent 2 section to output
3. Format pass/fail results
4. Display issues if any
5. Test with existing samples
```

**Step 5: Testing & Refinement (2-3 hours)**

```text
1. Test with clean documents
2. Test with documents containing missed identifiers
3. Measure recall and precision
4. Refine prompt if needed
5. Document results
```

---

### 10.2 Technical Decisions

**Decision 1: Dataclass vs Pydantic**

- **Choice**: Use standard library `dataclass` with `frozen=True`
- **Rationale**: No new dependencies, simple validation, matches Iteration 1 style
- **Note**: Tech lead may choose Pydantic if preferred

**Decision 2: JSON Parsing**

- **Choice**: Use `json.loads()` with try/except
- **Rationale**: Standard library, sufficient for this use case
- **Error Handling**: Retry once on malformed JSON, then raise ValidationError

**Decision 3: Prompt Format**

- **Choice**: Multi-line f-string template
- **Rationale**: Simple, readable, easy to modify
- **Future**: May move to template files in Iteration 3

**Decision 4: Independence Enforcement**

- **Choice**: Function signature only accepts anonymized text
- **Rationale**: Architectural constraint, prevents accidental context leaks
- **Verification**: Code review must confirm no global state access

---

### 10.3 Code Structure

**File Organization**:

```text
src/anonymization/
├── __init__.py          # Add ValidationResult, Issue exports
├── llm.py               # Unchanged (reuse existing)
├── simple.py            # Unchanged (Agent 1)
└── validation.py        # NEW - Agent 2 implementation

Structure of validation.py:
1. Imports
2. Dataclass definitions (Issue, ValidationResult)
3. Prompt template constant
4. validate_anonymization() function
5. Helper functions (if needed)
```

**Estimated Line Count**:

- Dataclasses: ~30 lines
- Prompt template: ~40 lines
- Main function: ~100 lines
- Total: ~170 lines

---

### 10.4 Common Pitfalls to Avoid

**Pitfall 1: Context Leakage**

```text
❌ WRONG:
def validate_anonymization(
    anonymized_text: str,
    original_text: str  # ← NO! Violates independence
) -> ValidationResult:

✅ CORRECT:
def validate_anonymization(
    anonymized_text: str  # Only anonymized text
) -> ValidationResult:
```

**Pitfall 2: Flagging Placeholders**

```text
Problem: Agent 2 incorrectly flags [NAME_1] as a name

Solution: Prompt must explicitly state:
"Ignore placeholders matching pattern [TYPE_NUMBER]"

Test: Verify with document containing only placeholders
```

**Pitfall 3: Inconsistent Validation**

```text
Problem: ValidationResult with passed=True but issues=[...]

Solution: Add validation in __post_init__ or after parsing:
if passed and len(issues) > 0:
    passed = False  # Fix LLM inconsistency
```

**Pitfall 4: Poor Error Messages**

```text
❌ WRONG:
raise ValueError("Invalid input")

✅ CORRECT:
raise ValueError(
    f"anonymized_text must be a string, got {type(anonymized_text)}"
)
```

---

### 10.5 Testing Strategy

**Unit Testing** (Out of scope for Iteration 2, but document approach):

```text
Future test cases:
1. test_empty_string_returns_passed()
2. test_clean_document_returns_passed()
3. test_document_with_name_returns_failed()
4. test_document_with_email_returns_failed()
5. test_ignores_existing_placeholders()
6. test_none_input_raises_value_error()
7. test_validation_result_immutability()
```

**Manual Testing** (Required for Iteration 2):

```text
Test Suite:
1. Clean document with only placeholders
   Expected: passed=True, issues=[]

2. Document with missed name
   Expected: passed=False, issues contains NAME

3. Document with multiple missed identifiers
   Expected: passed=False, issues contains all

4. Empty string
   Expected: passed=True, issues=[]

5. Document with complex formatting
   Expected: Reasonable detection accuracy
```

---

## 11. Integration with Iteration 1

### 11.1 Imports Required

```text
From Iteration 1:
- from anonymization import AnonymizationResult
- from anonymization.llm import get_llm_client

From Standard Library:
- from dataclasses import dataclass
- import json
- from typing import Optional
```

### 11.2 Demo Script Changes

**Current demo.py structure**:

```text
1. Display header
2. For each sample:
   a. Show original
   b. Run anonymize_simple()
   c. Show result
   d. Show mappings
3. Done
```

**New demo.py structure**:

```text
1. Display header
2. For each sample:
   a. Show original
   b. Run anonymize_simple() [Agent 1]
   c. Show Agent 1 result + mappings
   d. Run validate_anonymization() [Agent 2]  ← NEW
   e. Show Agent 2 result (pass/fail + issues)  ← NEW
   f. Separator
3. Done
```

### 11.3 Backward Compatibility

- ✅ No changes to existing `anonymize_simple()` function
- ✅ No changes to `AnonymizationResult` structure
- ✅ No changes to LLM client interface
- ✅ Iteration 1 code continues to work independently

---

## 12. Known Limitations

### 12.1 Intentional Limitations (By Design)

These are deferred to future iterations:

- **No Retry Loop**: Agent 2 runs once, no iterative improvement (Iteration 3)
- **No Configuration**: Hardcoded behavior, no config file (Iteration 3)
- **No Risk Levels**: Binary pass/fail, no risk scoring (Iteration 4)
- **No Contextual Analysis**: No indirect identifier detection (Iteration 5)
- **No Performance Optimization**: Single-threaded, synchronous (Future)
- **No Caching**: Each call is independent (Future)

### 12.2 Expected Failure Modes

**Scenario 1: LLM Hallucinations**

- **Problem**: LLM may report false positives
- **Mitigation**: Precision target is 85%, not 100%
- **Handling**: Accept some false positives in Iteration 2

**Scenario 2: Missed Identifiers**

- **Problem**: LLM may miss subtle identifiers
- **Mitigation**: Recall target is 90%, not 100%
- **Handling**: Accept some false negatives in Iteration 2

**Scenario 3: Ambiguous Cases**

- **Problem**: "John" could be a name or nickname
- **Mitigation**: Agent 2 should flag it (prefer safety)
- **Handling**: Human review in Iteration 3+

**Scenario 4: LLM Provider Unavailable**

- **Problem**: Network issues, API limits
- **Mitigation**: Proper error handling
- **Handling**: Raise LLMProviderError, let caller decide

---

## 13. Success Metrics

### 13.1 Quantitative Metrics

**MUST Achieve** (Blocking):

- Recall ≥ 90% on test corpus
- Precision ≥ 85% on test corpus
- Zero Pylance errors
- All functional acceptance criteria pass

**SHOULD Achieve** (Non-blocking):

- Recall ≥ 95%
- Precision ≥ 90%
- P95 processing time <30s
- Code <200 lines

### 13.2 Qualitative Metrics

**Code Quality**:

- Clear, self-documenting code
- Comprehensive docstrings
- Logical organization
- Minimal complexity

**Usability**:

- Simple API (one function)
- Clear error messages
- Intuitive result structure
- Good demo output

**Maintainability**:

- Easy to modify prompt
- Easy to add new identifier types
- Easy to adjust thresholds
- Well-documented decisions

---

## 14. Risks & Mitigations

### 14.1 Technical Risks

**Risk 1: Low Recall**

- **Probability**: Medium
- **Impact**: High (fails acceptance)
- **Mitigation**:
  - Budget 2-3 hours for prompt refinement
  - Test with diverse documents
  - Iterate on prompt based on results
- **Contingency**: If <90% after 3 iterations, escalate to architect

**Risk 2: High False Positive Rate**

- **Probability**: Medium
- **Impact**: Medium (annoying but not blocking)
- **Mitigation**:
  - Explicitly list what NOT to flag in prompt
  - Provide negative examples
  - Test with clean documents
- **Contingency**: Accept if precision ≥85%, note for Iteration 3

**Risk 3: LLM Response Format Changes**

- **Probability**: Low
- **Impact**: Medium
- **Mitigation**:
  - Robust JSON parsing with fallback
  - Retry logic
  - Clear error messages
- **Contingency**: Log malformed responses for analysis

### 14.2 Process Risks

**Risk 4: Scope Creep**

- **Probability**: Medium
- **Impact**: High (delays delivery)
- **Mitigation**:
  - Clear non-goals section
  - Refer to iteration package boundaries
  - Tech lead enforces scope
- **Contingency**: Document new requirements for Iteration 3

**Risk 5: Test Corpus Unavailable**

- **Probability**: Low
- **Impact**: Medium (can't measure recall/precision)
- **Mitigation**:
  - Create synthetic test corpus if needed
  - 50 documents, manually labeled
  - ~4 hours of preparation time
- **Contingency**: Use smaller corpus (20 documents minimum)

---

## 15. Iteration 3 Preview

### 15.1 What's Next

Iteration 3 will add:

- **Orchestration**: Automatic retry loop
- **Configuration**: YAML config file
- **Retry Context**: Feed Agent 2 findings back to Agent 1
- **Max Iterations**: Configurable retry limit
- **Failure Handling**: Graceful degradation

### 15.2 Prepare for Iteration 3

**Document These During Iteration 2**:

1. **Prompt Effectiveness**:

   - Which prompt variations worked best?
   - What examples helped most?
   - What instructions were ignored?

2. **Failure Patterns**:

   - What types of identifiers were consistently missed?
   - What patterns triggered false positives?
   - What document structures caused issues?

3. **Performance Baseline**:

   - Actual processing times by document size
   - LLM token usage
   - Memory consumption

4. **Configuration Needs**:
   - What parameters should be configurable?
   - What defaults work well?
   - What adjustments did you make during testing?

---

## 16. Appendices

### 16.1 Glossary

| Term                    | Definition                                                                             |
| ----------------------- | -------------------------------------------------------------------------------------- |
| **Direct Identifier**   | Personal data that directly identifies an individual (name, email, phone, address)     |
| **Indirect Identifier** | Data that may identify someone when combined (age, job title, location) - NOT in scope |
| **False Positive**      | Agent 2 flags something as identifier when it's not (e.g., flagging a placeholder)     |
| **False Negative**      | Agent 2 misses an actual remaining identifier                                          |
| **Recall**              | Proportion of real identifiers that were detected                                      |
| **Precision**           | Proportion of detected items that are real identifiers                                 |
| **Context Leakage**     | When Agent 2 receives information from Agent 1 (violates independence)                 |
| **Placeholder**         | Anonymization replacement like [NAME_1], [EMAIL_2]                                     |

### 16.2 Example Test Cases

**Test Case 1: Clean Document**

```text
Input:
"Customer [NAME_1] contacted us at [EMAIL_1] on [PHONE_1].
Their address is [ADDRESS_1]."

Expected Output:
ValidationResult(
  passed=True,
  issues=[],
  agent_reasoning="All identifiers properly anonymized with placeholders.",
  confidence=0.98
)
```

**Test Case 2: Missed Email**

```text
Input:
"Customer [NAME_1] contacted us at support@company.com on [PHONE_1]."

Expected Output:
ValidationResult(
  passed=False,
  issues=[
    Issue(
      identifier_type="EMAIL",
      value="support@company.com",
      context="...contacted us at support@company.com on...",
      location_hint="paragraph 1"
    )
  ],
  agent_reasoning="Found 1 remaining email address that was not anonymized.",
  confidence=0.92
)
```

**Test Case 3: Multiple Issues**

```text
Input:
"Customer [NAME_1] and John Smith emailed jane@example.com about the issue."

Expected Output:
ValidationResult(
  passed=False,
  issues=[
    Issue(identifier_type="NAME", value="John Smith", ...),
    Issue(identifier_type="EMAIL", value="jane@example.com", ...)
  ],
  agent_reasoning="Found 2 remaining identifiers: 1 name and 1 email address.",
  confidence=0.89
)
```

### 16.3 Reference Documents

**Related Documents**:

- [Architect Handoff Guide](Architect-Handoff-Guide.md)
- [Iteration 1 Implementation](Iteration%201%20Implementation%20-%20Complete%20✅.md)
- [Iteration 1 Requirements](requirements/iteration1.md)

**External References**:

- GDPR Definition of Personal Data: <https://gdpr-info.eu/art-4-gdpr/>
- Python Dataclasses: <https://docs.python.org/3/library/dataclasses.html>
- JSON Schema: <https://json-schema.org/>

### 16.4 Change Log

| Version | Date       | Changes                   | Author    |
| ------- | ---------- | ------------------------- | --------- |
| 1.0     | 2025-10-03 | Initial iteration package | Architect |

---

## 17. Delivery Checklist

### 17.1 Architect Validation

Before handing off to dev team, architect confirms:

- [ ] All five pillars complete:
  - [ ] Interface contracts defined
  - [ ] Data structures specified
  - [ ] Configuration documented (even if not implemented)
  - [ ] Behavioral requirements with step-by-step flows
  - [ ] Quality criteria with test procedures
- [ ] No implementation code (only specifications)
- [ ] No over-prescription (tech lead has design freedom)
- [ ] All dependencies documented
- [ ] All acceptance criteria testable
- [ ] Risks identified and mitigated
- [ ] Iteration 3 foundation prepared

### 17.2 Tech Lead Review

Tech lead reviews and confirms:

- [ ] Requirements are clear and actionable
- [ ] Sufficient detail to design implementation
- [ ] Not over-constrained (can choose implementation approach)
- [ ] Integration points with Iteration 1 clear
- [ ] Quality targets are reasonable
- [ ] Timeline is realistic (estimate: 1-2 days)

### 17.3 Handoff Complete

- [ ] Document delivered to dev team
- [ ] Kickoff meeting scheduled (optional)
- [ ] Questions channel established (Slack, email, etc.)
- [ ] Architect available for clarifications

---

**END OF ITERATION 2 REQUIREMENTS PACKAGE**

**Status**: READY FOR IMPLEMENTATION  
**Estimated Effort**: 1-2 days (8-16 hours)  
**Delivery Date**: TBD  
**Next Iteration**: Orchestration & Configuration (Iteration 3)
