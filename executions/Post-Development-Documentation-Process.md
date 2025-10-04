# Post-Development Documentation Process

**Purpose**: Standardized process for creating final documentation after each iteration is complete.

**Owner of the document**: Development team or development responsible

**Receiver of the document**: Product Lead and Architect. Information should be relevant to validate implemented poitns and progress

**When**: Execute this process ONLY when the user explicitly states "iteration has been done" and has created a new tag (IT-1, IT-2, IT-3, etc.).

---

## Prerequisites

Before starting this process, ensure:

- [ ] User has explicitly stated "iteration is done"
- [ ] User has created a git tag (e.g., `IT-X` where X is the iteration number)
- [ ] Code is committed and tagged in git repository
- [ ] Demo has been tested and works successfully

---

## Process Steps

### Step 1: Verify Tag Exists

```bash
# Check that the iteration tag exists
git tag -l "IT-*"

# Show the tag details
git show IT-X --stat

# Show changes from previous iteration
git diff IT-{X-1}..IT-X --stat
```

**Expected Output**: Tag exists and shows the iteration's changes.

### Step 2: Analyze Code Changes

Gather information about what changed in this iteration:

```bash
# List all changed files
git diff IT-{X-1}..IT-X --name-only

# Count lines in new/modified files
git show IT-X:path/to/file.py | wc -l

# View file headers to understand purpose
git show IT-X:path/to/file.py | head -50
```

**Information to Collect**:
- New files created (with line counts)
- Modified files (with line counts)
- Unchanged files (document as "no breaking changes")
- Total lines of code added
- Key features implemented

### Step 3: Review Iteration Requirements

Check if requirements documentation exists for this iteration:

```bash
# Look for requirements document
ls -la executions/execution-X/
```

**Documents to Review**:
- `iteration-X.md` - Requirements package
- Any other specification documents
- Previous iteration's completion documents (as examples)

### Step 4: Create Directory Structure

Ensure proper directory exists:

```bash
# Create execution directory if needed
mkdir -p executions/execution-X
```

**Required Directory**: `executions/execution-X/`

### Step 5: Create "Implementation Complete ✅" Document

**File**: `executions/execution-X/Iteration X Implementation - Complete ✅.md`

**Template Structure**:

```markdown
# Iteration X Implementation - Complete ✅

**Date**: YYYY-MM-DD
**Status**: Ready for Testing

## Implementation Summary
[Brief summary referencing requirements doc]

## What Was Delivered

### ✅ Core Functionality
[List main features delivered]

### ✅ Code Structure
[Show file tree with line counts]

### ✅ Documentation
[List documentation created/updated]

### ✅ Dependencies
[Any new dependencies or changes]

## Files Created/Modified

### New Files
[List with descriptions]

### Modified Files
[List with what changed]

### Unchanged Files
[Document backward compatibility]

## Acceptance Criteria Status

### Functional Acceptance (X/X) ✅
[Checklist of functional requirements met]

### Technical Acceptance (X/X) ✅
[Checklist of technical requirements met]

### Integration Quality (X/X) ✅
[Checklist of integration requirements met]

## How to Test

### Prerequisites
[Setup requirements]

### Option 1: [Provider Name]
[Step-by-step testing instructions]

### Option 2: [Provider Name]
[Step-by-step testing instructions]

## Sample Output Expected
[Show expected demo output]

## Known Limitations (As Designed)
[List intentional scope limitations]

## Next Steps
[What to do next, questions for next iteration]

## Success Metrics (To Be Measured)
[Checklist of metrics to track]

## Questions for Iteration X+1
[Document questions for next iteration]

---

**Implementation Status**: ✅ COMPLETE
**Ready for Testing**: YES
**Iteration X+1**: [Preview next iteration]
```

### Step 6: Create "Implementation Final Summary" Document

**File**: `executions/execution-X/Iteration X Implementation - Final Summary.md`

**Template Structure**:

```markdown
# Iteration X Implementation - Final Summary

**Date**: YYYY-MM-DD
**Status**: ✅ **COMPLETE - READY FOR TESTING**

## Overview
[Comprehensive overview with context]

## Deliverables

### ✅ Core Implementation (X files, ~XXX lines total)

1. **[path/to/file1.py](../../path/to/file1.py)** (XXX lines) **NEW/UPDATED/ENHANCED**
   [Detailed description of file contents]
   [Key classes/functions]
   [Design decisions]

2. **[path/to/file2.py](../../path/to/file2.py)** (XXX lines) **NEW/UPDATED/ENHANCED**
   [Detailed description]

[Continue for all files...]

### ✅ Demo & Examples
[Demo changes and test cases]

### ✅ Configuration & Documentation
[Config and doc changes]

## Code Quality

### ✅ Zero Pylance Errors
[List type safety measures]

### ✅ Clean Code Standards
[List code quality measures]

### ✅ Requirements Compliance

| Requirement | Target | Actual | Status |
|-------------|--------|--------|--------|
[Table of requirements vs delivery]

### ✅ Architecture Compliance

| Principle | Implementation |
|-----------|----------------|
[Table of architecture principles]

## File Structure
[Complete directory tree with line counts]

## How to Test

### Quick Test (Recommended: [Provider])
[Step-by-step with code blocks]

### Expected Output
[Detailed sample output]

## Acceptance Criteria Status

### Functional (X/X) ✅
[Detailed checklist]

### Technical (X/X) ✅
[Detailed checklist]

### Integration Quality (X/X) ✅
[Detailed checklist]

### Code Quality (X/X) ✅
[Detailed checklist]

## Known Limitations (By Design)
[Comprehensive list of scope limitations]

## Next Steps
[Detailed next steps and planning]

## Key Technical Decisions
[List major design decisions with rationale]

## Success Metrics (Achieved/To Be Measured)
[Comprehensive metrics]

## Changes from Iteration X-1

### New Files
[List with line counts]

### Modified Files
[List with changes made]

### Unchanged Files (Zero Impact)
[List to show backward compatibility]

## Git Commit (IT-X Tag)

Tag: `IT-X`
Commit: `[commit hash]`

```bash
git tag IT-X
git commit -m "[Commit message template]"
```

## Iteration X+1 Preview

### What's Coming Next
[Detailed preview of next iteration features]

---

**Status**: ✅ **IMPLEMENTATION COMPLETE**
**Quality**: ✅ **ZERO PYLANCE ERRORS**
**Ready**: ✅ **READY FOR TESTING**
**Next**: Iteration X+1 - [Next iteration summary]
```

### Step 7: Reference Previous Iterations

**Use as Templates**:
- `executions/execution-1/Iteration 1 Implementation - Complete ✅.md`
- `executions/execution-1/Iteration 1 Implementation - Final Summary.md`
- `executions/execution-2/Iteration 2 Implementation - Complete ✅.md`
- `executions/execution-2/Iteration 2 Implementation - Final Summary.md`
- `executions/execution-3/Iteration 3 Implementation - Complete ✅.md`
- `executions/execution-3/Iteration 3 Implementation - Final Summary.md`

**Maintain Consistency**:
- Same section structure
- Same level of detail
- Same formatting style
- Same quality standards

### Step 8: Quality Checklist

Before marking complete, verify:

#### Document 1: "Implementation Complete ✅"
- [ ] Date is current
- [ ] Status is "Ready for Testing"
- [ ] All sections filled out
- [ ] Acceptance criteria counts are accurate (X/X format)
- [ ] Testing instructions are complete for all LLM providers
- [ ] Sample output matches actual demo output
- [ ] Known limitations are comprehensive
- [ ] Next steps are actionable
- [ ] Markdown formatting is correct
- [ ] Links to files work correctly

#### Document 2: "Implementation Final Summary"
- [ ] Date is current
- [ ] Status includes all three ✅ indicators
- [ ] All file line counts are accurate
- [ ] File descriptions are detailed and accurate
- [ ] Code quality section is comprehensive
- [ ] Requirements compliance table is complete
- [ ] Acceptance criteria tables are complete
- [ ] Git commit hash is correct
- [ ] Commit message template is professional
- [ ] Iteration preview is detailed
- [ ] Markdown formatting is correct
- [ ] Links to files work correctly

### Step 9: Verify Documentation

```bash
# List created files
ls -la executions/execution-X/

# Verify markdown formatting
# (Open in IDE or use markdown preview)
```

**Expected Files**:
1. `Iteration X Implementation - Complete ✅.md`
2. `Iteration X Implementation - Final Summary.md`
3. Any requirements documents (if not already present)

### Step 10: Confirm Completion

Inform the user:

```markdown
## ✅ Documents Created

1. **[executions/execution-X/Iteration X Implementation - Complete ✅.md](path)**
   - Implementation summary with acceptance criteria
   - Testing instructions
   - Sample output
   - Known limitations
   - Next steps

2. **[executions/execution-X/Iteration X Implementation - Final Summary.md](path)**
   - Comprehensive overview
   - Detailed deliverables with line counts
   - Code quality metrics
   - Complete file structure
   - Acceptance criteria status
   - Key technical decisions
   - Git commit template
   - Next iteration preview

Both documents accurately reflect the state at IT-X tag (commit [hash]).
```

---

## Key Information to Extract

For each iteration, gather and document:

### Code Metrics
- **Total lines**: Sum of all implementation files
- **New lines**: Lines added in this iteration
- **Files created**: Count and list with line counts
- **Files modified**: Count and list with line counts
- **Files unchanged**: List to show backward compatibility

### Features Delivered
- **Core functionality**: Main features implemented
- **Supporting features**: Helper functions, utilities
- **Infrastructure**: Shared code, models, clients
- **Integration points**: How components connect

### Quality Metrics
- **Pylance errors**: Should always be 0
- **Type coverage**: Should be 100% for public APIs
- **Documentation coverage**: Should be 100% for public APIs
- **Test coverage**: Note if tests exist (later iterations)

### Acceptance Criteria
- **Functional**: Feature completeness
- **Technical**: Code quality and standards
- **Integration**: Backward compatibility
- **Code Quality**: Type safety, documentation

---

## Examples by Iteration

### Iteration 1 Focus
- Single-agent anonymization (Agent 1)
- LLM integration
- Basic entity types (NAME, EMAIL, PHONE, ADDRESS)
- Minimal viable implementation

### Iteration 2 Focus
- Dual-agent workflow (Agent 1 + Agent 2)
- Validation layer
- Pydantic models
- OTHER entity type
- Auth token support

### Iteration 3 Focus
- Complete 3-agent workflow (Agent 1 + Agent 2 + Agent 3)
- Risk assessment stub
- Conditional execution
- Final GDPR compliance recommendation
- Zero breaking changes

### Future Iterations
- Follow same pattern
- Always reference previous iterations
- Maintain consistency
- Document evolution

---

## Important Notes

1. **Wait for User Signal**: ONLY start this process when user explicitly says iteration is done
2. **Tag Must Exist**: Verify git tag exists before proceeding
3. **Use Templates**: Reference previous iterations for consistency
4. **Accuracy**: All line counts and metrics must be verified
5. **Completeness**: Both documents must be comprehensive
6. **Quality**: Zero Pylance errors, professional formatting
7. **Links**: All file references should be clickable markdown links
8. **Preview**: Always include preview of next iteration

---

## Tools and Commands

### Useful Git Commands
```bash
# List all tags
git tag -l "IT-*"

# Show tag details
git show IT-X --stat

# Compare iterations
git diff IT-{X-1}..IT-X --stat
git diff IT-{X-1}..IT-X --name-only

# Count lines in a file at specific tag
git show IT-X:path/to/file.py | wc -l

# View file content at specific tag
git show IT-X:path/to/file.py

# Get commit hash for tag
git rev-parse IT-X
```

### Useful File Commands
```bash
# Count lines in current file
wc -l path/to/file.py

# List directory contents
ls -la executions/execution-X/

# Create directory
mkdir -p executions/execution-X/
```

---

## Success Criteria

Documentation is complete when:
- [ ] Both documents created in correct directory
- [ ] All sections filled with accurate information
- [ ] All line counts verified
- [ ] All links working
- [ ] Markdown formatting correct
- [ ] Consistent with previous iterations
- [ ] User has confirmed completion
- [ ] Documents provide clear testing instructions
- [ ] Documents include next iteration preview

---

**Version**: 1.0
**Last Updated**: 2025-10-04
**Applies To**: All iterations (IT-1, IT-2, IT-3, and beyond)
