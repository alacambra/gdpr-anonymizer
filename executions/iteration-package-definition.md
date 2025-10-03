## 1. What is an Iteration Package?

The iteration package should pick requirments of the requirments list and indicate which of them will be implemented. If only partial implementation exsit, inform about the scope of the requirment on the iteration.

### 1.1 Definition

An **Iteration Package** is a complete, self-contained set of deliverables that enables a development team to implement a discrete increment of functionality without requiring additional clarification from stakeholders, product management, or architecture.

**Key Characteristics:**
- ✅ **Self-Contained**: All information needed for implementation
- ✅ **Scoped**: Clear boundaries of what's IN and OUT
- ✅ **Actionable**: Dev team can start immediately
- ✅ **Testable**: Clear acceptance criteria
- ✅ **Sequenced**: Builds on previous iterations

### 1.2 Purpose

**FOR DEVELOPMENT TEAM:**
- Clear understanding of WHAT to build
- Sufficient detail to make technical decisions
- Acceptance criteria for "done"
- Context for WHY (business value)

**FOR TECH LEAD:**
- Architectural guidance without over-prescription
- Interface contracts for team coordination
- Quality targets
- Integration points with other iterations

**FOR PRODUCT MANAGER:**
- Verification that requirements are captured
- Visibility into incremental value delivery
- Basis for acceptance testing

**FOR ARCHITECT:**
- Ensure architectural vision is followed
- Document key decisions (ADRs)
- Manage technical debt consciously
- Prepare foundation for future iterations

### 1.3 What an Iteration Package is NOT

- ❌ **NOT Implementation Code**: Dev team writes the code
- ❌ **NOT Detailed Design**: Tech lead designs the implementation
- ❌ **NOT Task Breakdown**: Tech lead breaks into developer tasks
- ❌ **NOT Test Cases**: QA writes detailed test cases
- ❌ **NOT User Stories**: Product manager owns these (may reference them)

---