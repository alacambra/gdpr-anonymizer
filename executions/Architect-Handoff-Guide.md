# Architect Handoff Guide - Iteration Package Specification

## Document Information

**Purpose**: Define what architects must deliver to development teams for each iteration  
**Audience**: Architects preparing iteration packages  
**Project Type**: Modular monolith with dedicated dev team and tech lead  
**Version**: 1.0  

---

## 1. Overview

### 1.1 The Handoff Chain

```
Stakeholder → Product Manager → Architect → Dev Team (with Tech Lead)
```

**Architect's Role:**
- Translate business requirements into technical specifications
- Define system structure without prescribing implementation
- Provide sufficient detail for tech lead to design solutions
- Establish quality gates and acceptance criteria

**What This Is:**
- ✅ Technical requirements and constraints
- ✅ Interface contracts and data structures
- ✅ Behavioral specifications
- ✅ Quality criteria and acceptance tests

**What This Is NOT:**
- ❌ Implementation code or pseudocode
- ❌ Detailed design (tech lead's responsibility)
- ❌ Technology selection (unless architecturally mandated)
- ❌ Step-by-step coding instructions

---

## 2. The Five Pillars of Specification

### 2.1 Interface Contracts

**Detail Level**: ⭐⭐⭐ HIGH - Language agnostic but specific

**What to Provide:**

```
Interface Name: IAgent1
Location: domain/ports/
Purpose: Contract for anonymization execution agent

Methods:
────────────────────────────────────────────────────
Method: execute

Inputs:
  • document: Document
    The document to anonymize
  • retry_context: Optional[RetryContext]
    Context from previous attempt (null on first call)

Returns:
  • AnonymizationResult
    Contains anonymized text, mappings, and metadata

Exceptions:
  • InvalidDocumentError: If document is empty or malformed
  • LLMProviderError: If LLM communication fails

Behavior Contract:
  - Pre-conditions: document must be valid (non-empty)
  - Post-conditions: All direct identifiers replaced
  - Idempotency: NO (LLM may vary)
  - Timeout: 60 seconds for documents up to 10KB
────────────────────────────────────────────────────
```

**Alternative Format - Table:**

| Method | Inputs | Returns | Exceptions | Contract |
|--------|--------|---------|------------|----------|
| execute | document: Document<br>retry_context: RetryContext? | AnonymizationResult | InvalidDocumentError<br>LLMProviderError | All identifiers replaced |

**Don't Include:**
- ❌ Python Protocol syntax
- ❌ Implementation details
- ❌ Private methods

---

### 2.2 Data Structures

**Detail Level**: ⭐⭐⭐ HIGH - Schema specification

**What to Provide:**

```
Data Structure: ValidationResult
Location: domain/models/
Purpose: Outcome of Agent 2 verification
Immutability: Immutable

Fields:
┌─────────────────┬───────────────┬──────────┬────────────────────────┐
│ Field           │ Type          │ Required │ Description            │
├─────────────────┼───────────────┼──────────┼────────────────────────┤
│ passed          │ Boolean       │ Yes      │ True if no issues      │
│ issues          │ List[Issue]   │ Yes      │ Empty if passed        │
│ agent_reasoning │ String        │ Yes      │ Explanation            │
│ confidence      │ Float (0-1)   │ Yes      │ Confidence score       │
└─────────────────┴───────────────┴──────────┴────────────────────────┘

Validation Rules:
  • If passed=true, then issues must be empty
  • If passed=false, then issues must have ≥1 item
  • confidence must be 0.0-1.0

Nested Type: Issue
┌─────────────────┬────────┬──────────┬─────────────────────────┐
│ Field           │ Type   │ Required │ Description             │
├─────────────────┼────────┼──────────┼─────────────────────────┤
│ identifier_type │ Enum   │ Yes      │ NAME|EMAIL|PHONE|ADDRESS│
│ value           │ String │ Yes      │ The identifier found    │
│ context         │ String │ Yes      │ ±20 chars around it     │
│ location_hint   │ String │ Yes      │ "paragraph 3"           │
└─────────────────┴────────┴──────────┴─────────────────────────┘
```

**Don't Include:**
- ❌ Implementation choice (dataclass vs Pydantic)
- ❌ Private fields
- ❌ Method implementations

---

### 2.3 Configuration Formats

**Detail Level**: ⭐⭐⭐⭐ VERY HIGH - Exact format with examples

**What to Provide:**

```yaml
# config.yaml - Complete structure

llm:
  provider: "claude"              # Options: ollama | claude | openai
  model: "claude-sonnet-4.5"      # Provider-specific model
  temperature: 0.1                # Range: 0.0-2.0
  max_tokens: 4096                # Positive integer
  
  ollama:
    base_url: "http://localhost:11434"
    default_model: "llama2"
  
  claude:
    api_key_env: "ANTHROPIC_API_KEY"    # Env var name
    default_model: "claude-sonnet-4.5"
  
  openai:
    api_key_env: "OPENAI_API_KEY"
    organization_env: "OPENAI_ORG"      # Optional
    default_model: "gpt-4"

agents:
  agent1:
    name: "ANON-EXEC"
    enabled: true
  
  agent2:
    name: "DIRECT-CHECK"
    enabled: true
    strictness: "normal"          # Options: strict | normal | lenient
    confidence_threshold: 0.8     # Range: 0.0-1.0

orchestration:
  max_iterations: 3               # Range: 1-10
  fail_on_validation_failure: false

output:
  include_metadata: true
  include_iteration_history: true
```

**Validation Rules:**
- llm.provider must be: ollama | claude | openai
- llm.temperature must be: 0.0-2.0
- If provider=claude: ANTHROPIC_API_KEY must be set
- If provider=openai: OPENAI_API_KEY must be set
- orchestration.max_iterations must be: 1-10

**Environment Variables:**
```bash
# Required based on provider
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Optional overrides (pattern: ANON_<SECTION>_<FIELD>)
ANON_LLM_PROVIDER=openai
ANON_ORCHESTRATION_MAX_ITERATIONS=5
```

**Security:**
- ❌ NEVER commit API keys to config.yaml
- ✅ API keys ONLY in environment variables
- ✅ Provide config.yaml.example with placeholders

---

### 2.4 Behavioral Requirements

**Detail Level**: ⭐⭐⭐⭐ VERY HIGH - Precise step-by-step behavior

**What to Provide:**

```
REQ-I2-F-005: Orchestrated Agent Loop

Trigger: User requests document anonymization

Workflow:
────────────────────────────────────────────────────
STEP 1: Initialize
  - Set iteration_counter = 1
  - Prepare original document

STEP 2: Execute Agent 1
  - Input: Original document + optional RetryContext
  - Output: AnonymizationResult
  - Record in attempt_history

STEP 3: Execute Agent 2
  - Input: Anonymized document ONLY
  - Output: ValidationResult
  - Record in attempt_history

DECISION POINT:
  IF ValidationResult.passed = true:
    → Go to STEP 5 (Success)
  
  IF ValidationResult.passed = false AND iteration_counter < max_iterations:
    → Go to STEP 4 (Retry)
  
  IF ValidationResult.passed = false AND iteration_counter >= max_iterations:
    → Go to STEP 6 (Failure)

STEP 4: Prepare Retry
  - Increment iteration_counter
  - Create RetryContext with:
    * Original document
    * Previous anonymization
    * Issues from Agent 2
  → Go back to STEP 2

STEP 5: Success Path
  - Return OrchestrationResult:
    * status: SUCCESS
    * final_result: AnonymizationResult
    * all_attempts: History
    * iteration_count: Total iterations
  → END

STEP 6: Failure Path
  - Return OrchestrationResult:
    * status: FAILED
    * final_result: Best attempt
    * all_attempts: History
    * persistent_issues: Aggregated issues
    * recommendation: "Manual review required"
  → END
────────────────────────────────────────────────────

Configuration:
  • max_iterations: Default 3, range 1-10

Error Handling:
  • Agent 1 exception → Propagate to caller
  • Agent 2 exception → Propagate to caller
  • Max iterations reached → Return FAILED status (not exception)

Performance:
  • Expected: 5-60 seconds for typical documents
  • Timeout: 300 seconds total
```

**Don't Include:**
- ❌ Implementation (for loops, try/catch)
- ❌ Code structure
- ❌ Which classes/methods to use

---

### 2.5 Quality Criteria

**Detail Level**: ⭐⭐⭐⭐ VERY HIGH - Measurable with test procedures

**What to Provide:**

```
Quality Metric: Agent 2 Verification Recall

Definition:
  Proportion of actual remaining identifiers that Agent 2 detects

Formula:
  Recall = True Positives / (True Positives + False Negatives)

Target:
  • Minimum: 90%
  • Target: 95%
  • Stretch: 98%

Test Method:
  1. Prepare 50 documents with known remaining identifiers
  2. Each document contains 3-5 missed identifiers
  3. Pass each to Agent 2
  4. Compare Agent 2 findings vs ground truth
  5. Calculate: TP / (TP + FN)

Test Data:
  • 50 documents
  • ~200 total identifiers
  • Mix: 40% names, 30% emails, 20% phones, 10% addresses

Acceptance:
  MUST: Overall recall ≥ 90%
  MUST: Per-category recall ≥ 85%
  SHOULD: Overall recall ≥ 95%

Failure Response:
  IF < 90%:
    1. Analyze false negatives
    2. Refine Agent 2 prompt
    3. Re-test
    4. If still failing after 3 attempts → Escalate to architect

Example:
  Test: 200 identifiers in corpus
  Agent 2 found: 190
  Missed: 10
  Recall = 190/200 = 95% ✓ PASS

────────────────────────────────────────────────────

Quality Metric: Agent 2 Verification Precision

Definition:
  Proportion of Agent 2's reported issues that are real problems

Formula:
  Precision = True Positives / (True Positives + False Positives)

Target:
  • Minimum: 85%
  • Target: 90%
  • Stretch: 95%

Test Method:
  1. Prepare 100 documents (50 clean, 50 with issues)
  2. Pass each to Agent 2
  3. Manually verify each reported issue
  4. Classify: True Positive or False Positive
  5. Calculate: TP / (TP + FP)

Acceptance:
  MUST: Precision ≥ 85%
  SHOULD: Precision ≥ 90%

────────────────────────────────────────────────────

Quality Metric: Orchestration Processing Time

Definition:
  Total time from start to OrchestrationResult

Target:
  • Typical documents (200-500 words): < 30 seconds
  • Large documents (up to 10KB): < 60 seconds

Test Method:
  1. Prepare 20 documents of varying sizes
  2. Time full orchestration (all iterations)
  3. Calculate mean and p95

Acceptance:
  MUST: P95 < 60 seconds for documents up to 10KB
  SHOULD: Mean < 30 seconds for typical documents
```

---

## 3. Iteration Package Checklist

### 3.1 Required Deliverables

**Primary Document:**
- [ ] Iteration Requirements Document with all five pillars:
  - [ ] Interface contracts defined
  - [ ] Data structures specified
  - [ ] Configuration format complete with examples
  - [ ] Behavioral requirements with step-by-step flows
  - [ ] Quality criteria with test procedures

**Supporting Documents:**
- [ ] Architecture Decision Records (ADRs) - if architectural choices made
- [ ] Dependency documentation - prerequisites and constraints
- [ ] Migration guide - if updating existing code

### 3.2 Validation Checklist

Before handoff, verify:

**Completeness:**
- [ ] All interfaces have complete contracts
- [ ] All data structures have field specifications
- [ ] Configuration has validation rules
- [ ] All behaviors have decision points specified
- [ ] All quality metrics have test procedures

**Clarity:**
- [ ] No ambiguous terms (defined in glossary if needed)
- [ ] Examples provided for complex concepts
- [ ] Decision points clearly marked
- [ ] Edge cases documented

**Appropriate Detail:**
- [ ] Enough detail for tech lead to design
- [ ] Not so detailed that it prescribes implementation
- [ ] No code syntax (except configuration examples)
- [ ] No technology choices (unless mandatory)

**Testability:**
- [ ] All quality criteria are measurable
- [ ] Test procedures are concrete
- [ ] Acceptance thresholds defined
- [ ] Failure escalation paths clear

---

## 4. Common Mistakes to Avoid

### 4.1 Too Much Detail (Over-specification)

**❌ Wrong:**
```python
class Agent1:
    def execute(self, doc):
        for entity in self._scan(doc):
            if entity.type == "NAME":
                placeholder = f"[NAME_{self.counter}]"
```
This is implementation code.

**✅ Right:**
```
Agent 1 must scan document, identify entities, and replace 
with placeholders using format [TYPE_NUMBER].
```

### 4.2 Too Little Detail (Under-specification)

**❌ Wrong:**
```
Agent 2 should verify the anonymization.
```
This is too vague.

**✅ Right:**
```
Agent 2 must:
  1. Scan anonymized document for remaining identifiers
  2. Return ValidationResult with passed=true/false
  3. If failed, list specific issues with locations
  4. Independent scan (no Agent 1 context)
```

### 4.3 Technology Prescription

**❌ Wrong:**
```
Use Pydantic BaseModel for ValidationResult.
Use async/await for all methods.
```
Let tech lead decide unless architecturally mandated.

**✅ Right:**
```
ValidationResult must be immutable after creation.
All agent methods must be non-blocking for future scalability.
```

### 4.4 Mixing Requirements with Implementation

**❌ Wrong:**
```
Orchestrator should use a for loop to retry up to max_iterations,
with a try/except block to catch Agent 2 failures.
```

**✅ Right:**
```
Orchestrator must retry up to max_iterations when Agent 2 
returns failed validation, then return FAILED status if 
limit reached.
```

---

## 5. Summary: Detail Level Matrix

| Pillar | Detail Level | Format | Why |
|--------|--------------|--------|-----|
| **Interface Contracts** | ⭐⭐⭐ High | Tables or structured text | Tech lead needs exact contracts |
| **Data Structures** | ⭐⭐⭐ High | Tables with validation | Prevents confusion |
| **Configuration** | ⭐⭐⭐⭐ Very High | Complete YAML examples | User-facing format |
| **Behavioral Requirements** | ⭐⭐⭐⭐ Very High | Step-by-step flows | Zero ambiguity |
| **Quality Criteria** | ⭐⭐⭐⭐ Very High | Measurable metrics | Clear acceptance |

---

## 6. Template Structure

Use this structure for iteration requirements documents:

```
# Iteration N Requirements

## 1. Overview
  - Purpose
  - Success Criteria
  - Non-Goals

## 2. Functional Requirements
  - Feature specifications
  - Behavioral requirements with workflows

## 3. Interface Contracts
  - All interfaces with complete contracts

## 4. Data Structures
  - All domain models with field specs

## 5. Configuration
  - Complete config format
  - Validation rules
  - Environment variables

## 6. Quality Criteria
  - All metrics with test procedures
  - Acceptance thresholds

## 7. Acceptance Criteria
  - Functional checklist
  - Technical checklist
  - Quality gates

## 8. Definition of Done
  - Code complete
  - Documentation complete
  - Testing complete
```

---

**End of Guide**

This guide ensures architects provide sufficient detail for dev teams to implement 
successfully without over-constraining technical decisions.