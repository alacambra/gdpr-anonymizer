# Requirement Naming Convention Standard

## Document Control

**Version**: 1.0  
**Date**: 2025-10-06  
**Status**: Active  
**Applies To**: All requirement documents in GDPR Text Anonymization System project

---

## 1. Purpose

This document defines the formal naming convention for all requirements in the project to ensure:
- Unique identification of each requirement
- Clear categorization by type
- Stable traceability across document versions
- Consistent structure across all requirement documents

---

## 2. Requirement Identifier Structure

### 2.1 Standard Format

```
REQ-[TYPE]-[NUMBER][SUFFIX]
```

**Components**:
- `REQ`: Fixed prefix (all requirements)
- `TYPE`: Requirement type code (1-3 letters)
- `NUMBER`: Sequential integer (001, 002, 003, etc.)
- `SUFFIX`: Optional letter or decimal for insertions/sub-requirements

**Examples**:
- `REQ-F-001` - Functional requirement #1
- `REQ-A-023` - Architectural requirement #23
- `REQ-A-023A` - Inserted after REQ-A-023
- `REQ-F-015.1` - Sub-requirement of REQ-F-015

### 2.2 Type Codes

| Code | Type | Purpose | Document Location |
|------|------|---------|-------------------|
| **F** | Functional | What the system does (features, behaviors, capabilities) | Functional-Requirements.md |
| **A** | Architectural | How the system is structured (design, patterns, layers) | Architectural-Requirements.md |
| **NF** | Non-Functional | Quality attributes (performance, security, usability) | Non-Functional-Requirements.md |
| **I** | Interface | API contracts, endpoints, protocols | Interface-Requirements.md |
| **D** | Data | Data models, schemas, storage | Data-Requirements.md |

**Extensible**: New type codes can be added as needed (e.g., REQ-T for testing requirements).

### 2.3 Number Assignment

**Sequential within type**:
- Start at 001 for each requirement type
- Increment by 1 for each new requirement
- No gaps (don't skip numbers)
- Three-digit format with leading zeros: 001, 002, ..., 099, 100

**Example sequence**:
```
REQ-F-001
REQ-F-002
REQ-F-003
...
REQ-F-099
REQ-F-100
```

---

## 3. Suffixes for Insertions and Sub-Requirements

### 3.1 Alphabetic Suffixes (Insertions)

**Purpose**: Insert new requirements between existing ones without renumbering

**Format**: Single uppercase letter (A, B, C, ...)

**Usage**:
```
Existing:
REQ-A-077
REQ-A-078

Need to insert between:
REQ-A-077
REQ-A-077A    ← New requirement inserted
REQ-A-077B    ← Another insertion
REQ-A-078

Further insertion:
REQ-A-077
REQ-A-077A
REQ-A-077AA   ← Insert between A and B (use double letter)
REQ-A-077B
REQ-A-078
```

**When to use**:
- Adding related requirements in same topic area
- Splitting an existing requirement into multiple parts
- Need to maintain logical grouping without renumbering

### 3.2 Decimal Suffixes (Sub-Requirements)

**Purpose**: Create hierarchical relationships

**Format**: Period followed by integer (.1, .2, .3, ...)

**Usage**:
```
REQ-F-015       Parent requirement
REQ-F-015.1     Child requirement
REQ-F-015.2     Child requirement
REQ-F-015.2.1   Grandchild requirement
```

**When to use**:
- Requirement has multiple detailed components
- Breaking down complex requirement into parts
- Need to show parent-child relationship

**Rule**: Sub-requirements inherit the scope of their parent. If REQ-F-015 is removed, all .1, .2, etc. are also removed.

### 3.3 Suffix Combinations

**Allowed**:
- `REQ-A-023A.1` - Sub-requirement of inserted requirement
- `REQ-F-100B.2` - Valid hierarchical structure

**Avoid**:
- `REQ-A-023.1A` - Confusing (use REQ-A-023.1.1 or REQ-A-023A)
- `REQ-A-023-1` - Hyphens reserved for type separator only

---

## 4. Requirement Versioning

### 4.1 Document Versioning vs Requirement Versioning

**Important**: Individual requirements are **NOT versioned**. The requirement ID remains stable.

**Version tracking happens at document level**:
```markdown
## Document Version History

**Version 2.0** (2025-10-06)
- REQ-A-001: Added (new modular monolith requirement)
- REQ-A-023: Modified (changed from agent impl to orchestration)
- REQ-F-055: Deprecated (superseded by REQ-F-055A)
```

### 4.2 Modification Tracking

**When requirement content changes**:
1. Keep the same requirement ID
2. Update the text in place
3. Add version annotation in document history
4. Optionally mark in requirement: `*[v2.0]*`

**Example**:
```markdown
**REQ-A-002**: *[v2.0]* The system SHALL enforce strict dependency direction...

[Previous version said "The system SHALL separate concerns" - updated in v2.0]
```

### 4.3 Deprecation Process

**When requirement is no longer valid**:

1. Mark as deprecated in document
2. Add deprecation notice
3. Reference replacement requirement
4. Keep in document (do not delete)

**Format**:
```markdown
**REQ-A-023** (original version): *[Deprecated v2.0]*
- **Original text**: "Agent implementations SHALL reside in infrastructure layer"
- **Reason**: Oversimplified. Split into REQ-A-023A and REQ-A-023B
- **Migration**: See REQ-A-023A, REQ-A-023B for current requirements
- **Deprecated date**: 2025-10-06
```

---

## 5. Cross-References Between Requirements

### 5.1 Referencing Format

**Within same document**:
```markdown
As specified in REQ-A-015, the system SHALL...
This extends REQ-F-023 by adding...
See also: REQ-A-010, REQ-A-011A
```

**Cross-document references**:
```markdown
To support REQ-F-001 (Functional Requirements), the architecture...
This architectural requirement implements functional requirement REQ-F-023.
```

### 5.2 Dependency Tracking

**Optional but recommended** - create traceability matrix:

| Requirement | Depends On | Implemented By |
|-------------|------------|----------------|
| REQ-F-001 | - | REQ-A-023A, REQ-A-033A |
| REQ-A-023A | REQ-A-011A, REQ-A-011B | - |

---

## 6. Naming Rules Summary

### 6.1 DO

✓ Use consistent format: `REQ-[TYPE]-[NUMBER][SUFFIX]`  
✓ Start numbering at 001 for each type  
✓ Use alphabetic suffixes for insertions (A, B, C)  
✓ Use decimal suffixes for sub-requirements (.1, .2, .3)  
✓ Keep requirement IDs stable (don't renumber)  
✓ Track changes in document version history  
✓ Mark deprecated requirements clearly  

### 6.2 DON'T

✗ Don't use hyphens in suffixes (REQ-A-023-1)  
✗ Don't version individual requirements (REQ-A-023v2)  
✗ Don't reuse deleted requirement IDs  
✗ Don't skip numbers in sequence  
✗ Don't delete deprecated requirements (mark as deprecated)  
✗ Don't mix suffix types illogically (REQ-A-023.1A)  

---

## 7. Examples by Scenario

### 7.1 Initial Requirement Creation

```markdown
**REQ-F-001**: The system SHALL identify personal data
**REQ-F-002**: The system SHALL anonymize identified data
**REQ-F-003**: The system SHALL verify anonymization completeness
```

### 7.2 Inserting Related Requirements

```markdown
Existing:
**REQ-A-050**: The system SHALL use async I/O
**REQ-A-051**: The system SHALL support parallel processing

Need to add between:
**REQ-A-050**: The system SHALL use async I/O
**REQ-A-050A**: The system SHALL use asyncio for concurrency  ← NEW
**REQ-A-050B**: The system SHALL provide sync wrappers        ← NEW
**REQ-A-051**: The system SHALL support parallel processing
```

### 7.3 Breaking Down Complex Requirement

```markdown
**REQ-A-064**: The system SHALL follow modular monolith structure

Becomes:
**REQ-A-064**: The system SHALL follow modular monolith structure
**REQ-A-064.1**: Domain layer SHALL have zero external dependencies
**REQ-A-064.2**: Application layer SHALL depend only on domain
**REQ-A-064.3**: Infrastructure layer SHALL implement domain ports
```

### 7.4 Modifying Existing Requirement

```markdown
Version 1.0:
**REQ-A-004**: The system SHALL separate concerns into 3 layers

Version 2.0 (modified):
**REQ-A-004**: *[v2.0]* The system SHALL separate concerns into 4 layers

Document History:
- v2.0 (2025-10-06): REQ-A-004 modified - changed from 3 to 4 layers
```

### 7.5 Deprecating and Replacing

```markdown
**REQ-A-023**: *[Deprecated v2.0]* Agent implementations SHALL reside in infrastructure
- Replaced by: REQ-A-023A (orchestration strategies) and REQ-A-033A (agent responsibilities)

**REQ-A-023A**: *[New v2.0]* The system SHALL support multiple orchestration strategies
**REQ-A-033A**: *[New v2.0]* Agent implementations SHALL separate domain and infrastructure concerns
```

---

## 8. Governance

### 8.1 Requirement ID Assignment Authority

**Architects** assign:
- REQ-A (Architectural)
- REQ-NF (Non-Functional - architectural aspects)

**Product Managers** assign:
- REQ-F (Functional)
- REQ-NF (Non-Functional - user-facing aspects)

**Technical Leads** assign:
- REQ-I (Interface)
- REQ-D (Data)

### 8.2 Change Control

**Minor changes** (clarification, typos):
- Update in place
- Note in commit message
- No version history entry needed

**Major changes** (scope, behavior):
- Update requirement text
- Document in version history
- Mark with version annotation
- Notify affected stakeholders

**Deprecation**:
- Requires architect approval
- Must provide migration path
- Document reason clearly

---

## 9. Tooling and Automation

### 9.1 Validation Rules

Automated checks should verify:
- Format compliance: `^REQ-[A-Z]{1,3}-\d{3}[A-Z]*(\.\d+)*$`
- No duplicate IDs within a document
- All cross-references point to existing requirements
- Deprecated requirements have migration notes

### 9.2 Traceability Tools

**Recommended** (but not required for this project):
- Requirements management database
- Automated cross-reference checking
- Impact analysis tools
- Test-to-requirement traceability

---

## 10. Document Metadata

### 10.1 Required Sections in Requirement Documents

Each requirements document SHALL include:

**Header**:
```markdown
# [Document Title]

## Document Control
**Version**: X.Y
**Date**: YYYY-MM-DD
**Status**: Draft | Active | Deprecated
**Related Documents**: [list]
```

**Version History**:
```markdown
## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | 2025-10-06 | Added modular monolith requirements | Architect |
| 1.0 | 2025-10-03 | Initial version | Team |
```

**Change Summary** (for major versions):
```markdown
## Version X.Y Change Summary

### New Requirements
- REQ-X-###: Description

### Modified Requirements
- REQ-X-###: Change description

### Deprecated Requirements
- REQ-X-###: Deprecation reason
```

---

## Appendix A: Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  REQUIREMENT NAMING QUICK REFERENCE                     │
├─────────────────────────────────────────────────────────┤
│  Format:    REQ-[TYPE]-[NUMBER][SUFFIX]                 │
│                                                           │
│  Types:     F=Functional, A=Architectural, NF=NonFunc   │
│             I=Interface, D=Data                          │
│                                                           │
│  Number:    001, 002, 003, ... (3 digits)               │
│                                                           │
│  Suffixes:  A, B, C    (insertions)                     │
│             .1, .2, .3  (sub-requirements)               │
│                                                           │
│  Examples:  REQ-F-001   (functional #1)                 │
│             REQ-A-023A  (inserted after A-023)          │
│             REQ-F-050.1 (sub-req of F-050)              │
│                                                           │
│  Changes:   Document version, not requirement version   │
│  Deprecated: Mark, don't delete                         │
│  References: REQ-X-### format                           │
└─────────────────────────────────────────────────────────┘
```

---

**END OF STANDARD**