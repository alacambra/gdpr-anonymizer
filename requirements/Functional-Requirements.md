# Functional Requirements - GDPR Text Anonymization System

## 1. Overview

This document outlines the functional requirements for a GDPR-compliant text anonymization system that processes documents through a multi-agent workflow to ensure personal data is properly anonymized.

## 2. Core Anonymization Capabilities

### 2.1 Direct Identifier Processing

**REQ-F-001**: The system SHALL identify and replace all direct personal identifiers including:

- Full names (first name, last name, middle names)
- Email addresses
- Phone numbers (all international formats)
- Physical addresses (street, city, postal code)
- National identification numbers (DNI, passport, SSN, etc.)
- IP addresses
- Device identifiers
- Account numbers
- License plate numbers

**REQ-F-002**: The system SHALL use standardized placeholder format: `[TYPE_NUMBER]`

- Examples: `[NAME_1]`, `[EMAIL_1]`, `[PHONE_1]`
- Sequential numbering per type: `[NAME_1]`, `[NAME_2]`, etc.

**REQ-F-003**: The system SHALL maintain consistency across the document

- Same entity receives same placeholder throughout
- All variations of an entity are mapped to single placeholder
- Example: "John Smith", "John", "Mr. Smith" → all become `[NAME_1]`

### 2.2 Indirect Identifier Processing

**REQ-F-004**: The system SHALL identify and process indirect identifiers (quasi-identifiers):

- Dates (birth dates, employment dates, event dates)
- Job titles and roles
- Geographic locations (neighborhoods, small towns)
- Educational institutions
- Employer names
- Unique combinations of attributes

**REQ-F-005**: The system SHALL apply appropriate anonymization techniques for indirect identifiers:

- **Generalization**: "Born January 15, 1985" → "Born in the 1980s"
- **Suppression**: Remove highly specific temporal sequences
- **Aggregation**: "Worked at 4 different companies" instead of listing each
- **Perturbation**: Add noise to numerical data where appropriate

### 2.3 Document Structure Preservation

**REQ-F-006**: The system SHALL maintain document readability after anonymization

- Preserve paragraph structure
- Maintain sentence flow
- Keep formatting (bold, italic, lists) where possible
- Ensure grammatical correctness after replacement

**REQ-F-007**: The system SHALL preserve relationship integrity between entities

- If "John" is `[NAME_1]`, then "John's colleague Sarah" should maintain relationship context
- Maintain pronoun consistency (he/she/they references)

### 2.4 Context-Aware Processing

**REQ-F-008**: The system SHALL handle contextual data appropriately

- Recognize when individual data points form identifying patterns
- Assess full document context for re-identification risk
- Not rely solely on chunked processing for risk assessment

**REQ-F-009**: The system SHALL distinguish between:

- **Direct identifiers**: Process via chunking (if needed)
- **Contextual patterns**: Analyze with full document context

## 3. Multi-Agent Workflow

### 3.1 Agent 1: ANON-EXEC (Anonymization Executor)

**REQ-F-010**: Agent 1 SHALL perform systematic document scanning

- Identify all personal data requiring anonymization
- Create entity registry mapping original → placeholder
- Execute replacements consistently

**REQ-F-011**: Agent 1 SHALL support both full-document and chunked processing

- Use full document scan for entity registry creation
- Apply chunked replacement for large documents (>150 lines)
- Use configurable chunk size and overlap parameters

**REQ-F-012**: Agent 1 SHALL generate structured outputs:

- Anonymized document text
- Entity registry (all identified entities)
- Anonymization mapping log (transformation record)
- Processing statistics (entity counts by type)

**REQ-F-013**: Agent 1 SHALL support multiple consecutive LLM calls within single session:

- Call 1: Identify entities (full document)
- Call 2: Build entity registry
- Call 3: Apply replacements (chunked or full)
- Call 4: Self-verification

### 3.2 Agent 2: DIRECT-CHECK (Direct Identifier Verification)

**REQ-F-014**: Agent 2 SHALL verify complete removal of direct identifiers

- Perform binary check: PASS or FAIL
- Scan for any remaining personal identifiers
- Check for common anonymization errors (partial replacements, missed variations)

**REQ-F-015**: Agent 2 SHALL produce validation report containing:

- Overall result: PASS or FAIL
- List of any identified issues (if FAIL)
- Specific locations of remaining identifiers
- Recommendations for remediation

**REQ-F-016**: Agent 2 SHALL trigger iterative refinement

- If validation FAILS, return control to Agent 1
- Provide specific issues to Agent 1 for correction
- Support up to 3 refinement iterations

### 3.3 Agent 3: RISK-ASSESS (Risk Assessment)

**REQ-F-017**: Agent 3 SHALL evaluate re-identification risk using 5 dimensions:

1. **Uniqueness of Data Combinations** (1-5 scale)
   - Assess how unique the combination of remaining attributes is
   - Consider demographic rarity

2. **Population Size** (1-5 scale)
   - Evaluate size of potential matching population
   - Consider geographic and temporal scope

3. **External Correlation Potential** (1-5 scale)
   - Assess likelihood of matching with public records
   - Consider LinkedIn, social media, news articles
   - Evaluate corporate databases, academic publications

4. **Temporal Patterns** (1-5 scale)
   - Analyze date sequences and timelines
   - Assess career progression patterns
   - Evaluate event chronologies

5. **Context Richness** (1-5 scale)
   - Evaluate narrative detail level
   - Assess industry-specific terminology
   - Consider project descriptions, achievements

**REQ-F-018**: Agent 3 SHALL calculate overall risk score:

- Sum of 5 dimensions: 1-25 total
- Map to risk levels:
  - **CRITICAL**: 21-25 (Not GDPR compliant)
  - **HIGH**: 16-20 (Not GDPR compliant)
  - **MEDIUM**: 11-15 (Marginally compliant)
  - **LOW**: 6-10 (Compliant)
  - **NEGLIGIBLE**: 1-5 (Fully compliant)

**REQ-F-019**: Agent 3 SHALL provide detailed risk assessment report:

- Score for each dimension with justification
- Overall risk level and GDPR compliance determination
- Specific concerns and remaining vulnerabilities
- Recommendations for additional anonymization (if needed)

**REQ-F-020**: Agent 3 SHALL require full document context

- Must analyze complete document, not chunks
- Must see all temporal sequences together
- Must evaluate full demographic profile

## 4. Workflow Orchestration

### 4.1 Sequential Processing

**REQ-F-021**: The system SHALL execute agents in deterministic sequence:

1. Agent 1: Execute anonymization
2. Agent 2: Verify direct identifiers removed
3. If Agent 2 FAILS: Return to Agent 1 with issues
4. Agent 3: Assess re-identification risk
5. Return complete results

**REQ-F-022**: The system SHALL support parallel execution where appropriate:

- Agent 2 and Agent 3 MAY run in parallel if both use final output
- Chunked replacements within Agent 1 MAY run in parallel

### 4.2 Error Handling and Recovery

**REQ-F-023**: The system SHALL handle agent failures gracefully:

- Log errors with full context
- Provide clear error messages to user
- Support retry mechanism for transient failures
- Maintain partial results for debugging

**REQ-F-024**: The system SHALL enforce maximum iteration limits:

- Maximum 3 refinement loops (Agent 1 ↔ Agent 2)
- Clear failure message if limit exceeded
- Preserve all intermediate results for analysis

## 5. Output and Reporting

### 5.1 Anonymized Document

**REQ-F-025**: The system SHALL generate anonymized document with:

- All placeholders properly applied
- Original structure preserved
- Readable and grammatically correct text
- Metadata (processing timestamp, configuration used)

### 5.2 Anonymization Mapping Log

**REQ-F-026**: The system SHALL produce detailed mapping log:

- Each original value → placeholder mapping
- Entity type classification
- Location information (line numbers)
- Anonymization technique applied (for indirect identifiers)

**REQ-F-027**: The mapping log SHALL be stored securely:

- Separate from anonymized document
- Access controlled (only authorized users)
- Retention policy configurable

### 5.3 Processing Summary

**REQ-F-028**: The system SHALL generate processing summary with:

- Total entities identified by type
- Number of replacements made
- Document size before/after
- Processing time for each agent
- Number of refinement iterations

### 5.4 Agent Reports

**REQ-F-029**: The system SHALL provide individual reports from each agent:

**Agent 1 Report:**

- Entities identified (count by type)
- Placeholder assignments
- Chunking strategy used (if applicable)
- Self-verification results

**Agent 2 Report:**

- Validation result (PASS/FAIL)
- Issues found (if any)
- Verification methodology
- Confidence level

**Agent 3 Report:**

- Dimension scores (1-5 each)
- Overall risk score (1-25)
- Risk level classification
- GDPR compliance determination
- Detailed justification for each score
- Recommendations

### 5.5 Final Assessment

**REQ-F-030**: The system SHALL deliver final GDPR compliance determination:

- **COMPLIANT**: Document safe to publish (LOW or NEGLIGIBLE risk)
- **MARGINAL**: Proceed with caution (MEDIUM risk)
- **NON-COMPLIANT**: Do not publish (HIGH or CRITICAL risk)

**REQ-F-031**: The system SHALL provide actionable recommendations:

- If non-compliant: Specific steps to achieve compliance
- Alternative anonymization approaches
- Data suppression suggestions

## 6. Command-Line Interface

### 6.1 Basic Operations

**REQ-F-032**: The system SHALL support CLI command for anonymization:

```bash
anonymize <input-file> [options]
```

**REQ-F-033**: The system SHALL support options:

- `--config <file>`: Use custom configuration
- `--output <file>`: Specify output location
- `--provider <ollama|claude|openai>`: Select LLM provider
- `--model <model-name>`: Specify model
- `--report-format <json|markdown|pdf>`: Report format
- `--verbose`: Detailed logging
- `--dry-run`: Analysis without anonymization

### 6.2 Configuration Management

**REQ-F-034**: The system SHALL support configuration initialization:

```bash
anonymize init [--template <basic|advanced>]
```

- Generate default config.yaml
- Include comments explaining each option

**REQ-F-035**: The system SHALL support configuration validation:

```bash
anonymize validate-config <config-file>
```

### 6.3 System Information

**REQ-F-036**: The system SHALL provide version and system info:
```bash
anonymize --version
anonymize --info
```

## 7. Configuration

### 7.1 LLM Provider Configuration

**REQ-F-037**: The system SHALL support configuration for each LLM provider:

**Ollama:**

- Base URL (default: http://localhost:11434)
- Model name
- Temperature, top_p, max_tokens

**Claude (Anthropic):**

- API key (from environment variable)
- Model name (claude-sonnet-4.5, etc.)
- Temperature, max_tokens

**OpenAI:**

- API key (from environment variable)
- Model name (gpt-4, etc.)
- Organization (optional)
- Temperature, max_tokens

### 7.2 Agent Configuration

**REQ-F-038**: The system SHALL support per-agent configuration:

**Agent 1:**

- Chunk size (default: 30 lines)
- Overlap (default: 5 lines)
- Max full document size (default: 150 lines)
- Self-verification enabled (default: true)

**Agent 2:**

- Verification strictness (strict, normal, lenient)
- Max iterations (default: 3)

**Agent 3:**

- Risk dimension weights (if custom scoring needed)
- Compliance thresholds
- External data sources to consider

### 7.3 GDPR Configuration

**REQ-F-039**: The system SHALL support GDPR compliance configuration:

- Risk level thresholds (customizable)
- Data retention policies
- Audit logging requirements
- Approved anonymization techniques

## 8. Data Handling

### 8.1 Input Requirements

**REQ-F-040**: The system SHALL accept input formats:

- Plain text (.txt)
- Markdown (.md)
- PDF (.pdf) - extract text
- Word documents (.docx) - extract text
- HTML (.html) - extract text

**REQ-F-041**: The system SHALL validate input:

- File exists and is readable
- File size within limits (configurable max size)
- Supported format
- Valid character encoding (UTF-8)

### 8.2 Output Requirements

**REQ-F-042**: The system SHALL generate output files:

- Anonymized document (same format as input, or plain text)
- Mapping log (JSON format)
- Processing summary (JSON or Markdown)
- Agent reports (JSON or Markdown)
- Final assessment (JSON or Markdown)

### 8.3 Security Requirements

**REQ-F-043**: The system SHALL handle sensitive data securely:

- Original documents never sent to external services unprocessed
- Mapping logs encrypted at rest (optional, configurable)
- API keys stored in environment variables only
- Secure deletion of temporary files

**REQ-F-044**: The system SHALL maintain audit trail:

- Log all anonymization operations
- Record user, timestamp, configuration used
- Store logs securely with retention policy
- Support log export for compliance audits

## 9. Performance Requirements

**REQ-F-045**: The system SHALL process documents efficiently:

- Small documents (<50 lines): <30 seconds
- Medium documents (50-200 lines): <2 minutes
- Large documents (200-500 lines): <5 minutes
- Very large documents (>500 lines): Provide progress indication

**REQ-F-046**: The system SHALL support batch processing:

- Process multiple documents sequentially or in parallel
- Aggregate reporting across batch
- Resume capability for interrupted batches

## 10. Extensibility Requirements

**REQ-F-047**: The system SHALL support adding new LLM providers:

- Plugin architecture for providers
- Minimal code changes to add provider
- Configuration-driven provider selection

**REQ-F-048**: The system SHALL support custom anonymization rules:

- User-defined entity types
- Custom placeholder formats
- Domain-specific anonymization logic

**REQ-F-049**: The system SHALL support additional agents:

- Agent 4, 5, etc. can be added to workflow
- Configurable agent sequence
- Agent-specific configuration sections

## 11. Quality Attributes

### 11.1 Accuracy

**REQ-F-050**: The system SHALL achieve high accuracy in:

- Direct identifier detection: >98%
- Placeholder consistency: 100%
- False positive rate: <5%

### 11.2 Completeness

**REQ-F-051**: The system SHALL ensure completeness:

- All direct identifiers removed (verified by Agent 2)
- All contextual patterns assessed (by Agent 3)
- No data loss (structure preserved)

### 11.3 Repeatability

**REQ-F-052**: The system SHALL produce repeatable results:

- Same input + configuration = same output
- Deterministic placeholder assignment
- Consistent risk scoring methodology

## 12. Documentation Requirements

**REQ-F-053**: The system SHALL provide comprehensive documentation:

- User guide for CLI usage
- Configuration reference
- GDPR compliance guide
- API documentation (if applicable)
- Troubleshooting guide

**REQ-F-054**: The system SHALL include examples:

- Sample documents (before/after)
- Configuration templates
- Common use cases
- Best practices for GDPR compliance

## 13. Future Enhancements (Optional)

**REQ-F-055**: The system MAY support in future versions:

- Web-based interface
- REST API for integration
- Real-time anonymization
- Multi-language support
- Image redaction (for scanned documents)
- Database anonymization
- Anonymization of structured data (JSON, CSV)

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-03  
**Status**: Draft for Implementation