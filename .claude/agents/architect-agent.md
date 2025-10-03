# Architect Handoff Guide - Iteration Package Specification

## Document Information

**Purpose**: Define what architects must deliver to development teams for each iteration  
**Audience**: Architects, Product Managers, Tech Leads  
**Scope**: Modular monolith projects with dedicated dev teams  
**Version**: 1.0  
**Last Updated**: 2025-10-03

---

## 1. Overview

### 1.1 The Handoff Process

```
Stakeholder → Product Manager → Architect → Dev Team (with Tech Lead)
                                    ↓
                          Iteration Package
```

**The Architect's Role:**
- Translate business requirements into technical specifications
- Define system structure without prescribing implementation
- Provide sufficient detail for tech lead to design solutions
- Establish quality gates and acceptance criteria
- Bridge the gap between "what" (product) and "how" (development)

**What This Is NOT:**
- ❌ Detailed design documents (tech lead's responsibility)
- ❌ Implementation code or pseudocode
- ❌ Technology selection (unless architecturally significant)
- ❌ Step-by-step coding instructions

**What This IS:**
- ✅ Technical requirements and constraints
- ✅ Interface contracts and data structures
- ✅ Behavioral specifications
- ✅ Quality criteria and acceptance tests
- ✅ Architectural boundaries and principles

### 1.2 Iteration Package Components

Each iteration package must contain:

1. **Iteration Requirements Document** (Primary deliverable)
2. **Architecture Decision Records** (ADRs) - if architectural choices made
3. **Dependency Documentation** - prerequisites and constraints
4. **Handoff Checklist** - validation that package is complete

---

## 2. The Five Pillars of Technical Specification

### 2.1 Interface Contracts (Method Signatures)

**Purpose**: Define the contracts between system components without dictating implementation.

#### Detail Level: ⭐⭐⭐ HIGH DETAIL - Language Agnostic

**What to Provide:**

For each interface/port in the system:

```
Interface Name: [Name]
Location: [Layer/Package]
Purpose: [Why this interface exists]
Implements/Extends: [Parent interfaces, if any]

Methods:
──────────────────────────────────────────────────────────────
Method: [method_name]

Inputs:
  • parameter_name: Type (constraints/format)
    Description: What this parameter represents
  • [repeat for each parameter]

Returns:
  • Type (constraints/format)
    Description: What is returned

Exceptions:
  • ExceptionType: When thrown
  • [repeat for each exception]

Behavior Contract:
  - Pre-conditions: What must be true before calling
  - Post-conditions: What will be true after calling
  - Side effects: Any state changes or external effects
  - Idempotency: Can it be called multiple times safely?

Performance Contract:
  - Expected time complexity: O(n), O(1), etc.
  - Expected space complexity
  - Timeout: Maximum execution time

──────────────────────────────────────────────────────────────
[Repeat for each method]
```

**Example:**

```
Interface Name: IAgent1
Location: domain/ports/agents.py
Purpose: Contract for anonymization execution agent

Methods:
──────────────────────────────────────────────────────────────
Method: execute

Inputs:
  • document: Document
    The document to anonymize (domain model)
  • retry_context: Optional[RetryContext] (nullable)
    Context from previous failed attempt, if this is a retry

Returns:
  • AnonymizationResult
    Contains anonymized document, mappings, and metadata

Exceptions:
  • InvalidDocumentError: If document is empty or malformed
  • LLMProviderError: If LLM communication fails (propagated from infrastructure)

Behavior Contract:
  - Pre-conditions:
    * document must be valid (non-empty, readable text)
    * If retry_context provided, must contain valid previous attempt
  - Post-conditions:
    * All direct identifiers in document are replaced with placeholders
    * Mapping registry created with all replacements
    * Same identifier always maps to same placeholder
  - Side effects:
    * Calls external LLM provider (logged)
    * No state persistence within agent
  - Idempotency: NO - may produce different results due to LLM non-determinism

Performance Contract:
  - Expected time: O(n) where n = document length
  - Expected space: O(m) where m = number of entities
  - Timeout: 60 seconds for documents up to 10KB
──────────────────────────────────────────────────────────────
```

**Alternative Format - Decision Table:**

| Method | Inputs | Outputs | Exceptions | Pre-conditions | Post-conditions |
|--------|--------|---------|------------|----------------|-----------------|
| execute | document: Document<br>retry_context: RetryContext? | AnonymizationResult | InvalidDocumentError<br>LLMProviderError | document is valid | All identifiers replaced |

**What NOT to Include:**
- ❌ Python Protocol syntax or class definitions
- ❌ Implementation details (how to replace text)
- ❌ Private/helper method signatures
- ❌ Technology-specific details (async/sync, decorators)

---

### 2.2 Data Structure Specifications

**Purpose**: Define the shape of data that flows through the system.

#### Detail Level: ⭐⭐⭐ HIGH DETAIL - Schema Specification

**What to Provide:**

For each domain model/data structure:

```
Data Structure: [Name]
Location: [Layer/Package]
Type: [Domain Model | DTO | Value Object | Entity]
Purpose: [What this represents in the business domain]
Immutability: [Immutable | Mutable] (with justification)

Fields:
┌─────────────────┬──────────────┬──────────┬─────────────┬────────────────────┐
│ Field Name      │ Type         │ Required │ Default     │ Description        │
├─────────────────┼──────────────┼──────────┼─────────────┼────────────────────┤
│ [name]          │ [type]       │ Yes/No   │ [value|N/A] │ [description]      │
└─────────────────┴──────────────┴──────────┴─────────────┴────────────────────┘

Type Definitions:
  • [Type]: [Constraints, format, examples]
    Example: "Email: String in format user@domain.com, max 254 chars"

Validation Rules:
  • [Rule description]
  • [Invariants that must be maintained]
  • [Cross-field validations]

Relationships:
  • [Related entity/model] - [Nature of relationship]

Serialization:
  • Format: [JSON | YAML | Binary | N/A]
  • Schema: [If JSON/YAML, provide schema]
  • Versioning: [How breaking changes handled]

Lifecycle:
  • Creation: [When/how instances created]
  • Mutation: [What can change after creation]
  • Destruction: [When/how instances disposed]
```

**Example:**

```
Data Structure: ValidationResult
Location: domain/models/validation.py
Type: Domain Model (Value Object)
Purpose: Represents the outcome of Agent 2's verification of anonymized document
Immutability: Immutable (instances never change after creation)

Fields:
┌─────────────────┬───────────────┬──────────┬─────────────┬──────────────────────────────┐
│ Field Name      │ Type          │ Required │ Default     │ Description                  │
├─────────────────┼───────────────┼──────────┼─────────────┼──────────────────────────────┤
│ passed          │ Boolean       │ Yes      │ N/A         │ True if no issues found      │
│ issues          │ List[Issue]   │ Yes      │ Empty list  │ Problems found (if any)      │
│ agent_reasoning │ String        │ Yes      │ N/A         │ Agent's explanation          │
│ confidence      │ Float         │ Yes      │ N/A         │ Confidence score (0.0-1.0)   │
│ timestamp       │ DateTime      │ Yes      │ Now (UTC)   │ When validation performed    │
└─────────────────┴───────────────┴──────────┴─────────────┴──────────────────────────────┘

Type Definitions:
  • Boolean: true | false
  • List[Issue]: Ordered list of Issue objects (see nested structure below)
  • String: UTF-8 text, max 5000 characters
  • Float: Decimal number, precision to 2 decimal places, range 0.0-1.0
  • DateTime: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ), UTC timezone

Validation Rules:
  • If passed = true, then issues must be empty list (length = 0)
  • If passed = false, then issues must contain at least 1 Issue
  • confidence must be between 0.0 and 1.0 (inclusive)
  • agent_reasoning must not be empty string
  • timestamp must not be in the future

Relationships:
  • Contains: List[Issue] (composition - Issues don't exist outside ValidationResult)

Serialization:
  • Format: JSON
  • Schema:
    {
      "passed": boolean,
      "issues": [Issue],
      "agent_reasoning": string,
      "confidence": number,
      "timestamp": string (ISO 8601)
    }
  • Versioning: Add new optional fields only; never remove or rename

Lifecycle:
  • Creation: Instantiated by Agent 2 after verification complete
  • Mutation: Never (immutable value object)
  • Destruction: Garbage collected when no longer referenced

──────────────────────────────────────────────────────────────

Nested Structure: Issue
Purpose: Represents a single validation problem found
Immutability: Immutable

Fields:
┌─────────────────┬────────┬──────────┬─────────┬──────────────────────────────┐
│ Field Name      │ Type   │ Required │ Default │ Description                  │
├─────────────────┼────────┼──────────┼─────────┼──────────────────────────────┤
│ identifier_type │ Enum   │ Yes      │ N/A     │ Type: NAME|EMAIL|PHONE|ADDRESS│
│ value           │ String │ Yes      │ N/A     │ The identifier found         │
│ context         │ String │ Yes      │ N/A     │ ±20 chars surrounding text   │
│ location_hint   │ String │ Yes      │ N/A     │ Location description         │
└─────────────────┴────────┴──────────┴─────────┴──────────────────────────────┘

Validation Rules:
  • identifier_type must be one of: NAME, EMAIL, PHONE, ADDRESS
  • value must not be empty string
  • context must not be empty string, max 100 characters
  • location_hint format: "paragraph N" or "line N" or "near '[text]'"
```

**What NOT to Include:**
- ❌ Implementation choice (dataclass vs Pydantic vs plain class)
- ❌ Private/internal fields
- ❌ Method implementations
- ❌ Getters/setters (unless they have business logic meaning)

---

### 2.3 Configuration Formats

**Purpose**: Define all user-configurable options and their structure.

#### Detail Level: ⭐⭐⭐⭐ VERY HIGH DETAIL - Exact Format

**What to Provide:**

```
Configuration File: [filename]
Format: [YAML | JSON | TOML | INI]
Location: [Where file should be placed]
Loading Priority: [Order of precedence]

Complete Structure:
[Full example configuration with all options]

Field Specifications:
──────────────────────────────────────────────────────────────
Section: [section.subsection]
Field: [field_name]

Type: [Type]
Required: [Yes | No]
Default: [Default value if not provided]
Valid Values: [Constraints, enum values, ranges]
Example: [Example value]
Description: [What this controls]
Impact: [What changes when this is modified]

──────────────────────────────────────────────────────────────
[Repeat for each field]

Validation Rules:
  • [Cross-field validation]
  • [Required combinations]
  • [Mutually exclusive options]

Environment Variable Overrides:
  • Pattern: [PREFIX_SECTION_FIELD]
  • Example: [ANON_LLM_PROVIDER=openai]

Required Environment Variables:
  • [VAR_NAME]: [When required] - [Description]

Security Considerations:
  • [Which fields contain sensitive data]
  • [How secrets should be handled]
  • [What should never be committed to version control]

Migration Guide (if updating existing config):
  • From version: [X] to [Y]
  • Breaking changes: [List]
  • Migration steps: [How to update]
```

**Example:**

```
Configuration File: config.yaml
Format: YAML
Location: Project root directory or ~/.anonymization/config.yaml
Loading Priority: 1. CLI args → 2. Environment vars → 3. config.yaml → 4. Defaults

Complete Structure:
──────────────────────────────────────────────────────────────
llm:
  provider: "claude"              # "ollama" | "claude" | "openai"
  model: "claude-sonnet-4.5"      # Provider-specific model identifier
  temperature: 0.1                # 0.0-2.0, controls randomness
  max_tokens: 4096                # Maximum response length
  
  ollama:
    base_url: "http://localhost:11434"
    default_model: "llama2"
  
  claude:
    api_key_env: "ANTHROPIC_API_KEY"
    default_model: "claude-sonnet-4.5"
  
  openai:
    api_key_env: "OPENAI_API_KEY"
    organization_env: "OPENAI_ORG"
    default_model: "gpt-4"

agents:
  agent1:
    name: "ANON-EXEC"
    enabled: true
  
  agent2:
    name: "DIRECT-CHECK"
    enabled: true
    strictness: "normal"          # "strict" | "normal" | "lenient"
    confidence_threshold: 0.8     # 0.0-1.0

orchestration:
  max_iterations: 3               # 1-10
  fail_on_validation_failure: false

output:
  include_metadata: true
  include_iteration_history: true
──────────────────────────────────────────────────────────────

Field Specifications:
──────────────────────────────────────────────────────────────
Section: llm
Field: provider

Type: String (Enumeration)
Required: Yes
Default: "claude"
Valid Values: "ollama" | "claude" | "openai"
Example: "openai"
Description: Which LLM provider to use for anonymization
Impact: Determines which API is called and which credentials are needed

──────────────────────────────────────────────────────────────
Section: llm
Field: temperature

Type: Float
Required: No
Default: 0.1
Valid Values: 0.0 to 2.0 (inclusive)
Example: 0.5
Description: Controls randomness in LLM responses. Lower = more deterministic.
Impact: Lower values give more consistent results; higher allows more creativity

──────────────────────────────────────────────────────────────
Section: agents.agent2
Field: confidence_threshold

Type: Float
Required: No
Default: 0.8
Valid Values: 0.0 to 1.0 (inclusive)
Example: 0.9
Description: Minimum confidence for Agent 2 to report PASS
Impact: Higher threshold = more cautious validation (more likely to fail)

──────────────────────────────────────────────────────────────
[Continue for all fields...]

Validation Rules:
  • If llm.provider = "claude", then environment variable ANTHROPIC_API_KEY must be set
  • If llm.provider = "openai", then environment variable OPENAI_API_KEY must be set
  • If llm.provider = "ollama", then llm.ollama.base_url must be accessible
  • agents.agent2.enabled = true requires agents.agent1.enabled = true
  • orchestration.max_iterations must be >= 1
  • If agents.agent2.strictness = "strict", recommend confidence_threshold >= 0.9

Environment Variable Overrides:
  • Pattern: ANON_<SECTION>_<FIELD>
  • Example: ANON_LLM_PROVIDER=openai
  • Example: ANON_ORCHESTRATION_MAX_ITERATIONS=5
  • Nested fields use underscore: ANON_AGENTS_AGENT2_STRICTNESS=strict

Required Environment Variables:
  • ANTHROPIC_API_KEY: When llm.provider="claude" - Anthropic API key from console
  • OPENAI_API_KEY: When llm.provider="openai" - OpenAI API key
  • OPENAI_ORG: When llm.provider="openai" AND using organization - OpenAI org ID (optional)

Security Considerations:
  • NEVER commit API keys to config.yaml
  • NEVER commit config.yaml with real API keys to version control
  • API keys must ONLY be in environment variables
  • Add config.yaml with real keys to .gitignore
  • Provide config.yaml.example with placeholder values
  • Use .env file for development (not committed)

Migration Guide:
  • From version: None (first iteration with config)
  • Future iterations: Will document breaking changes here
```

**What NOT to Include:**
- ❌ How configuration is loaded (implementation detail)
- ❌ Which library to use for parsing
- ❌ Internal configuration objects structure

---

### 2.4 Behavioral Requirements

**Purpose**: Specify what the system does in response to inputs and conditions.

#### Detail Level: ⭐⭐⭐⭐ VERY HIGH DETAIL - Precise Behavior

**What to Provide:**

For each significant behavior or workflow:

```
Requirement ID: [REQ-XX-X-NNN]
Requirement Name: [Short descriptive name]
Source: [Business requirement reference]
Priority: [Must Have | Should Have | Nice to Have]

Behavior Description:
[1-2 sentence summary of what this requirement specifies]

Trigger Conditions:
WHEN: [What causes this behavior to execute]
  • [Specific condition 1]
  • [Specific condition 2]

Input State:
  • [What must exist before behavior starts]
  • [Pre-conditions that must be true]

Workflow Steps:
──────────────────────────────────────────────────────────────
STEP 1: [Step name]
  Action: [What happens]
  Actor: [Which component performs this]
  Input: [What data is used]
  Output: [What is produced]
  Duration: [Expected time]

STEP 2: [Step name]
  [Same structure]

DECISION POINT: [Decision name]
  Condition: [What is evaluated]
  
  IF [condition A]:
    → [consequence A]
    → Go to STEP X
  
  ELSE IF [condition B]:
    → [consequence B]
    → Go to STEP Y
  
  ELSE:
    → [default consequence]
    → Go to STEP Z

[Continue for all steps]
──────────────────────────────────────────────────────────────

Output State:
  • [What exists after behavior completes]
  • [Post-conditions that are guaranteed]

Success Criteria:
  • [What defines successful completion]

Failure Scenarios:
  Scenario: [Failure type]
    Condition: [When this failure occurs]
    Handling: [What should happen]
    Recovery: [Can it be retried? How?]
    User Impact: [What user sees]

Edge Cases:
  Case: [Edge case description]
    Behavior: [What should happen]
    Rationale: [Why this behavior chosen]

Performance Requirements:
  • Time complexity: [Big O notation]
  • Expected duration: [Concrete time estimate]
  • Timeout: [Maximum allowed time]
  • Resource usage: [Memory, connections, etc.]

Concurrency:
  • Can multiple instances run simultaneously? [Yes | No]
  • Is this behavior thread-safe? [Yes | No | N/A]
  • Synchronization requirements: [If any]

Observability:
  • What should be logged: [Key events to log]
  • What metrics to collect: [Counters, timers, etc.]

Configuration:
  • [Config values that affect this behavior]
  • [Defaults and ranges]

Dependencies:
  • Requires: [Other behaviors/components this depends on]
  • Conflicts with: [Incompatible behaviors]
```

**Example:**

```
Requirement ID: REQ-I2-F-005
Requirement Name: Orchestrated Agent Loop with Iterative Refinement
Source: REQ-F-021 (Multi-agent workflow orchestration)
Priority: Must Have

Behavior Description:
System must coordinate Agent 1 and Agent 2 in an iterative loop, retrying anonymization up to configured maximum if validation fails, until either validation passes or maximum iterations reached.

Trigger Conditions:
WHEN: User requests document anonymization via CLI or API
  • User has provided valid input document
  • Configuration has been loaded successfully
  • LLM provider is accessible

Input State:
  • Original document (Document domain model) exists
  • Configuration specifies max_iterations (default: 3)
  • Both Agent 1 and Agent 2 are enabled in configuration
  • LLM provider is initialized and ready

Workflow Steps:
──────────────────────────────────────────────────────────────
STEP 1: Initialize
  Action: Prepare orchestration context
  Actor: AnonymizationOrchestrator
  Input: Original document, configuration
  Output: Orchestration context (iteration_counter = 1, attempt_history = [])
  Duration: < 1ms

STEP 2: Execute Agent 1 (Anonymization)
  Action: Invoke Agent 1 to anonymize document
  Actor: Agent 1 (ANON-EXEC)
  Input: 
    - Original document
    - RetryContext (null on first attempt, populated on retries)
  Output: AnonymizationResult (anonymized text, mappings, metadata)
  Duration: 2-30 seconds (depends on document size and LLM)
  
  Record: Add AnonymizationResult to attempt_history

STEP 3: Execute Agent 2 (Verification)
  Action: Invoke Agent 2 to verify anonymization quality
  Actor: Agent 2 (DIRECT-CHECK)
  Input: Anonymized document ONLY (no context from Agent 1)
  Output: ValidationResult (passed flag, issues list, reasoning)
  Duration: 2-15 seconds
  
  Record: Add ValidationResult to attempt_history

DECISION POINT: Evaluate Validation Result
  Condition: Check ValidationResult.passed and iteration_counter
  
  IF ValidationResult.passed = true:
    → Anonymization successful
    → Go to STEP 5 (Success Path)
  
  ELSE IF ValidationResult.passed = false AND iteration_counter < max_iterations:
    → Validation failed but retries remain
    → Go to STEP 4 (Retry Path)
  
  ELSE IF ValidationResult.passed = false AND iteration_counter >= max_iterations:
    → Validation failed and no retries remain
    → Go to STEP 6 (Failure Path)

STEP 4: Prepare Retry (only if validation failed and retries remain)
  Action: Prepare context for Agent 1 retry
  Actor: AnonymizationOrchestrator
  Input: Previous AnonymizationResult, ValidationResult with issues
  Output: RetryContext containing:
    - Original document (unchanged)
    - Previous anonymization attempt
    - List of specific issues from ValidationResult
    - iteration_counter value
  Duration: < 1ms
  
  Increment: iteration_counter += 1
  
  → Go back to STEP 2 (with RetryContext populated)

STEP 5: Success Path
  Action: Package successful result
  Actor: AnonymizationOrchestrator
  Input: Final AnonymizationResult, all attempt_history
  Output: OrchestrationResult with:
    - status: SUCCESS
    - final_result: Last AnonymizationResult
    - all_attempts: List of all anonymization attempts
    - all_validations: List of all validation results
    - iteration_count: Total iterations executed
    - processing_time: Total time elapsed
  Duration: < 1ms
  
  → END (return OrchestrationResult to caller)

STEP 6: Failure Path
  Action: Package failure result with diagnostics
  Actor: AnonymizationOrchestrator
  Input: All attempt_history, final ValidationResult
  Output: OrchestrationResult with:
    - status: FAILED
    - final_result: Best attempt (last AnonymizationResult)
    - all_attempts: List of all anonymization attempts
    - all_validations: List of all validation results
    - iteration_count: max_iterations (exhausted)
    - persistent_issues: Aggregated list of issues found across all attempts
    - recommendation: "Manual review required"
    - processing_time: Total time elapsed
  Duration: < 1ms
  
  → END (return OrchestrationResult to caller)
──────────────────────────────────────────────────────────────

Output State:
  • OrchestrationResult exists with complete history
  • Original document unchanged (preserved)
  • All attempts and validations recorded for auditing
  • Clear success or failure status
  • If failed: Diagnostic information available

Success Criteria:
  • ValidationResult.passed = true within max_iterations
  • All identifiers successfully anonymized
  • OrchestrationResult.status = SUCCESS

Failure Scenarios:
  Scenario: Agent 1 throws exception
    Condition: LLM provider error, invalid document, etc.
    Handling: Exception propagates to caller immediately
    Recovery: No automatic retry - caller decides
    User Impact: Error message with details, no output files created
  
  Scenario: Agent 2 throws exception
    Condition: LLM provider error during verification
    Handling: Exception propagates to caller immediately
    Recovery: No automatic retry - caller decides
    User Impact: Error message, may have anonymized output but unverified
  
  Scenario: Max iterations reached without success
    Condition: iteration_counter >= max_iterations AND ValidationResult.passed = false
    Handling: Return OrchestrationResult with FAILED status
    Recovery: User can manually review or adjust configuration and retry
    User Impact: Warning message, output marked as unverified

Edge Cases:
  Case: max_iterations = 1 (no retries allowed)
    Behavior: Single attempt only; if Agent 2 fails, immediately go to failure path
    Rationale: Configuration allows disabling retry for speed

  Case: Agent 2 passes on first attempt
    Behavior: Skip retry logic entirely, go directly to success path
    Rationale: Most common case - should be fastest path
  
  Case: Agent 1 produces identical output on retry
    Behavior: Continues to Agent 2 verification anyway
    Rationale: Agent 2 might evaluate differently, or issue was intermittent
  
  Case: Document has no identifiers
    Behavior: Agent 1 returns empty mappings, Agent 2 should pass
    Rationale: Valid scenario - document already clean

Performance Requirements:
  • Time complexity: O(n × m) where n = document size, m = iterations
  • Expected duration: 5-60 seconds for typical documents (200-500 words)
  • Timeout: 300 seconds (5 minutes) total
  • Resource usage: One LLM API connection at a time (sequential)

Concurrency:
  • Can multiple instances run simultaneously? Yes (stateless orchestration)
  • Is this behavior thread-safe? Yes (no shared mutable state)
  • Synchronization requirements: None (each document processed independently)

Observability:
  • What should be logged:
    - Orchestration started (document ID, timestamp)
    - Agent 1 iteration N started/completed
    - Agent 2 iteration N started/completed (result: PASS/FAIL)
    - Retry initiated (iteration number, issues count)
    - Orchestration completed (status, total iterations, duration)
  
  • What metrics to collect:
    - Counter: total_anonymizations_attempted
    - Counter: total_anonymizations_succeeded
    - Counter: total_anonymizations_failed
    - Histogram: anonymization_duration_seconds
    - Histogram: iterations_per_document
    - Counter: total_retries_triggered

Configuration:
  • orchestration.max_iterations: Controls retry limit
    - Default: 3
    - Valid range: 1-10
    - Impact: Higher = more attempts but longer processing time
  
  • orchestration.fail_on_validation_failure: Error vs warning on failure
    - Default: false (returns result with warnings)
    - If true: Raises ValidationFailedError instead
    - Impact: Changes error handling behavior

Dependencies:
  • Requires: Agent 1 and Agent 2 implementations available
  • Requires: LLM provider accessible
  • Requires: Configuration loaded
  • Conflicts with: None
```

**What NOT to Include:**
- ❌ Implementation algorithms (for loops, if statements)
- ❌ Code structure (which classes, which methods)
- ❌ Technology choices (sync vs async)
- ❌ Optimization strategies

---

### 2.5 Quality Criteria

**Purpose**: Define measurable success criteria for testing and acceptance.

#### Detail Level: ⭐⭐⭐⭐ VERY HIGH DETAIL - Measurable Metrics

**What to Provide:**

For each quality dimension:

```
Quality Dimension: [Name]
Category: [Performance | Accuracy | Reliability | Usability | Security]
Priority: [Critical | High | Medium | Low]
Applies To: [Which component/feature]

Metric Definition:
Name: [Metric name]
Definition: [What is being measured]
Formula: [Mathematical formula if applicable]
Unit: [Percentage, seconds, count, etc.]

Target Value:
  • Minimum acceptable: [Threshold for pass/fail]
  • Target: [Desired value]
  • Stretch goal: [Exceptional performance]

Measurement Method:
Test Approach: [How to measure this]
Test Data: [What data to use]
Test Procedure:
  1. [Step 1]
  2. [Step 2]
  [...]
  
Sample Size: [How many tests needed for statistical significance]
Test Environment: [Conditions for testing]

Acceptance Criteria:
MUST: [Conditions that must be met for release]
SHOULD: [Conditions that should be met but not blocking]
NICE TO HAVE: [Aspirational goals]

Failure Handling:
IF target not met:
  1. [First remediation step]
  2. [Second remediation step]
  3. [Escalation path if still failing]

Context and Examples:
Why This Matters: [Business justification]
Example Calculation: [Walk through an example]
Historical Data: [If available from previous iterations]

Reporting:
Format: [How results should be reported]
Frequency: [When to measure]
Owner: [Who is responsible for measurement]
```

**Example:**

```
Quality Dimension: Agent 2 Verification Accuracy
Category: Accuracy
Priority: Critical
Applies To: Agent 2 (DIRECT-CHECK) verification functionality

──────────────────────────────────────────────────────────────
Metric 1: Recall (Sensitivity)
──────────────────────────────────────────────────────────────

Metric Definition:
Name: Verification Recall
Definition: Proportion of actual remaining identifiers that Agent 2 successfully detects
Formula: Recall = True Positives / (True Positives + False Negatives)
  Where:
    - True Positive = Agent 2 correctly identifies a remaining identifier
    - False Negative = Agent 2 misses a remaining identifier
Unit: Percentage (0-100%)

Target Value:
  • Minimum acceptable: 90%
  • Target: 95%
  • Stretch goal: 98%

Measurement Method:
Test Approach: Controlled test with known ground truth

Test Data:
  • Corpus: 50 documents intentionally containing missed identifiers
  • Each document contains 3-5 deliberately missed identifiers
  • Identifier types distributed: 40% names, 30% emails, 20% phones, 10% addresses
  • Total identifiers in test set: ~200 remaining identifiers
  • Documents sourced from: Real anonymization failures from Iteration 1 testing

Test Procedure:
  1. Prepare 50 test documents with known remaining identifiers (ground truth)
  2. For each document:
     a. Pass anonymized document to Agent 2
     b. Collect ValidationResult with issues list
     c. Compare Agent 2's findings against ground truth
     d. Record: True Positives, False Negatives
  3. Calculate: Recall = TP / (TP + FN)
  4. Calculate per-category recall (names, emails, phones, addresses)
  5. Calculate confidence intervals (95%)

Sample Size: 50 documents minimum, 200+ total identifiers
Test Environment: Same LLM provider and model as production configuration

Acceptance Criteria:
MUST: Overall recall ≥ 90%
MUST: Per-category recall ≥ 85% for each identifier type
SHOULD: Overall recall ≥ 95%
SHOULD: Confidence interval width < 5%
NICE TO HAVE: Recall ≥ 98%

Failure Handling:
IF overall recall < 90%:
  1. Analyze false negatives by category
  2. Refine Agent 2 prompt to emphasize missed patterns
  3. Re-test with same corpus
  4. If still < 90% after 3 prompt iterations: Escalate to architect
  5. Architect decision: Adjust target OR delay iteration OR change approach

Context and Examples:
Why This Matters: 
  Low recall means Agent 2 misses remaining identifiers, leading to 
  privacy breaches. This is the most critical metric for GDPR compliance.

Example Calculation:
  Test Set: 50 documents, 200 total remaining identifiers
  Agent 2 Results:
    - Correctly identified (TP): 190 identifiers
    - Missed (FN): 10 identifiers
  
  Recall = 190 / (190 + 10) = 190 / 200 = 0.95 = 95% ✓ PASS

Historical Data: 
  Iteration 1 manual testing: Estimated 85-90% recall (informal)
  Iteration 2 target: 95% (formal measurement)

Reporting:
Format: Test report with:
  - Overall recall percentage
  - Per-category breakdown
  - List of all false negatives with analysis
  - Prompt versions tested
  - Recommendations
Frequency: Once per iteration, before acceptance
Owner: QA Lead with support from Tech Lead

──────────────────────────────────────────────────────────────
Metric 2: Precision (Positive Predictive Value)
──────────────────────────────────────────────────────────────

Metric Definition:
Name: Verification Precision
Definition: Proportion of Agent 2's reported issues that are actual problems
Formula: Precision = True Positives / (True Positives + False Positives)
  Where:
    - True Positive = Agent 2 correctly identifies a remaining identifier
    - False Positive = Agent 2 flags something that isn't actually an identifier
Unit: Percentage (0-100%)

Target Value:
  • Minimum acceptable: 85%
  • Target: 90%
  • Stretch goal: 95%

Measurement Method:
Test Approach: Controlled test with mixed documents (some clean, some with issues)

Test Data:
  • Corpus: 100 documents total
    - 50 documents: Correctly anonymized (should produce zero issues)
    - 50 documents: Contain missed identifiers (should produce issues)
  • Documents varied in:
    - Length: 100-1000 words
    - Domain: Business emails, meeting notes, medical records, legal documents
    - Complexity: Simple to complex sentence structures

Test Procedure:
  1. Prepare 100 test documents (50 clean, 50 with issues)
  2. For each document:
     a. Pass to Agent 2
     b. Collect all reported issues
     c. Manually verify each reported issue
     d. Classify as True Positive or False Positive
  3. Calculate: Precision = TP / (TP + FP)
  4. Analyze false positive patterns
  5. Calculate confidence intervals

Sample Size: 100 documents minimum
Test Environment: Production-equivalent configuration

Acceptance Criteria:
MUST: Overall precision ≥ 85%
SHOULD: Precision ≥ 90%
SHOULD: False positive rate < 15%
NICE TO HAVE: Precision ≥ 95%

Failure Handling:
IF precision < 85%:
  1. Analyze false positive patterns (what is misclassified)
  2. Refine Agent 2 prompt to reduce over-flagging
  3. Balance