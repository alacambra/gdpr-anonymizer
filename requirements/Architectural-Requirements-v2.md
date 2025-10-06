# Architectural Requirements - GDPR Text Anonymization System

## Document Control

**Version**: 2.0
**Date**: 2025-10-06
**Status**: Active
**Related Documents**: Functional Requirements v1.0, Requirement Numbering System v1.0

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | 2025-10-06 | Added modular monolith, agentic architecture, agent prompts in domain, orchestration strategies | Architecture Team |
| 1.0 | 2025-10-03 | Initial version | Architecture Team |

---

## Version 2.0 Change Summary

### New Requirements Added

- **REQ-A-001A**: Modular monolith principles
- **REQ-A-011**: Agent definitions in domain layer
- **REQ-A-011A**: Agent prompts in domain layer
- **REQ-A-023A**: Multiple orchestration strategies
- **REQ-A-023B**: AutoGen integration requirements
- **REQ-A-033A**: Agent implementation responsibilities clarification
- **REQ-A-064A**: Updated directory structure with agent prompts and orchestration
- **REQ-A-073A-078B**: Complete agentic architecture section (7 new requirements)
- **REQ-A-079A-084B**: Complete modular monolith section (6 new requirements)

### Modified Requirements

- **REQ-A-002**: Added explicit forbidden dependencies diagram
- **REQ-A-004**: Changed from 3 layers to 4 layers (added Interface layer)
- **REQ-A-005**: Added agent definitions and prompts to domain layer contents
- **REQ-A-064**: Modified directory structure
- **REQ-A-093**: Added FastAPI and optional AutoGen to technology stack

### Deprecated Requirements

- **REQ-A-023** (original): *[Deprecated v2.0]* "Agent implementations SHALL reside in infrastructure layer"
  - **Reason**: Oversimplified. Content replaced by REQ-A-023A (orchestration strategies) and REQ-A-033A (agent responsibilities)
  - **Migration**: See REQ-A-023A, REQ-A-023B, REQ-A-033A
  - **Deprecated date**: 2025-10-06

---

## 1. Overview

This document defines the architectural requirements for building a maintainable, extensible, and GDPR-compliant text anonymization system based on hexagonal architecture and modular monolith principles.

---

## 2. Architectural Style

### 2.1 Hexagonal Architecture (Ports & Adapters)

**REQ-A-001**: The system SHALL follow hexagonal architecture principles:

- Business logic isolated in domain core
- External dependencies accessed through ports (interfaces)
- Adapters implement ports for specific technologies
- Dependencies point inward (infrastructure → application → domain)

**REQ-A-001A**: *[New v2.0]* The system SHALL be a **modular monolith**:

- Single deployable unit
- Clear module boundaries via hexagonal layers
- Low coupling between modules
- High cohesion within modules
- Ability to extract to microservices if needed (not required initially)

**Rationale**: Following Marta Fernández García's approach, prompts encode the agent's "cognitive model" - the business logic of what the agent should do. This is domain knowledge, not infrastructure machinery.

### 19.2 Agent Interaction Patterns

**REQ-A-075A**: *[New v2.0]* Agent interaction SHALL support:

**Current State** (Sequential):

- Agent 1 → produces output
- Agent 2 → verifies output
- Agent 3 → assesses risk
- Orchestrator manages sequence

**Future State** (Conversational - Optional):

- Agents communicate via messages
- Shared conversation context
- Dynamic agent selection
- Managed by AutoGen or similar

**REQ-A-076A**: *[New v2.0]* Agent outputs SHALL be:

- Structured (domain models, not strings)
- Validated on creation
- Immutable once created
- Traceable to source agent

### 19.3 Orchestration Patterns

**REQ-A-077A**: *[New v2.0]* The system SHALL support multiple orchestration patterns:

**Pattern 1: Sequential** (Current)

- Linear execution flow
- Manual error handling
- Direct control over agent sequence
- Simple to understand and debug

**Pattern 2: AutoGen GroupChat** (Future)

- Agent-to-agent communication
- Dynamic agent selection
- Conversation-based workflow
- Complex interaction patterns

**Pattern 3: Parallel Execution** (Future)

- Independent agent execution
- Result aggregation
- Performance optimization
- Requires careful coordination

**REQ-A-078A**: *[New v2.0]* Orchestration selection SHALL be:

- Configuration-driven
- Swappable without domain changes
- Transparent to interface layer
- Documented with trade-offs

**REQ-A-078B**: *[New v2.0]* Agent state management SHALL:

- Maintain conversation context when needed
- Support stateless operation as default
- Clear session lifecycle
- No global mutable state

---

## 20. Modular Monolith Principles

### 20.1 Module Definition

**REQ-A-079A**: *[New v2.0]* Modules SHALL be defined by hexagonal layers:

- Each layer is a module
- Clear interfaces between layers
- No circular dependencies between layers
- Modules communicate via ports only

**REQ-A-080A**: *[New v2.0]* Module independence SHALL be enforced:

- Domain module imports: NONE (except stdlib)
- Application module imports: domain only
- Infrastructure module imports: domain, application (via ports)
- Interface module imports: all layers (for DI)

### 20.2 Deployment Model

**REQ-A-081A**: *[New v2.0]* Modular monolith deployment SHALL be:

- Single Python package
- Single process (with async concurrency)
- Single database connection pool (if database added)
- Single configuration file
- Deployed as one unit

**Benefits**:

- Simple deployment
- No distributed system complexity
- Easier debugging
- Lower latency
- Transactional consistency

### 20.3 Future Microservices Extraction

**REQ-A-082A**: *[New v2.0]* Future microservices extraction SHALL be possible:

- Each layer can become a service if needed
- Ports become API boundaries
- Domain models become shared contracts
- But premature extraction is avoided

### 20.4 Module Boundaries

**REQ-A-083A**: *[New v2.0]* Module boundaries SHALL use explicit contracts:

- Python Protocols for interfaces
- Pydantic models for data contracts
- Comprehensive type hints
- Contract tests at module boundaries

**REQ-A-084A**: *[New v2.0]* Breaking changes SHALL be managed:

- Deprecation warnings before removal
- Version compatibility layers
- Migration guides
- Backward compatibility where feasible

**REQ-A-084B**: *[New v2.0]* Module cohesion SHALL be maximized:

- Related functionality grouped together
- Single responsibility per module
- Minimal cross-module dependencies
- High internal coupling, low external coupling

---

## 21. Concurrency Architecture

### 21.1 Concurrency Model

**REQ-A-077**: The system SHALL use single-threaded async model:

- One event loop per process
- Async/await for concurrency
- No threading or multiprocessing (initially)
- asyncio.gather for parallel operations

**REQ-A-078**: The system SHALL support safe parallelization:

- Parallel chunk processing (Agent 1)
- Parallel agent execution (Agent 2 & 3)
- Batch document processing
- No shared mutable state

### 21.2 Synchronization

**REQ-A-079**: The system SHALL manage synchronization:

- Locks only where necessary (minimize)
- Atomic operations for shared resources
- Clear ownership of mutable state
- Immutable domain models preferred

---

## 22. Versioning and Compatibility

### 22.1 Semantic Versioning

**REQ-A-080**: The system SHALL use semantic versioning:

- MAJOR.MINOR.PATCH format
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### 22.2 API Stability

**REQ-A-081**: The system SHALL maintain API stability:

- Domain interfaces are stable (avoid breaking changes)
- Deprecation warnings before removal
- Migration guides for breaking changes
- Backward compatibility for configuration (where possible)

### 22.3 LLM Provider Compatibility

**REQ-A-082**: The system SHALL handle provider changes:

- Version pinning for provider libraries
- Adapter layer isolates provider API changes
- Graceful degradation if provider unavailable
- Clear error messages for incompatible versions

---

## 23. Code Quality Architecture

### 23.1 Code Style

**REQ-A-083**: The system SHALL enforce code style:

- PEP 8 compliance
- Type hints for all public interfaces
- Maximum line length: 100 characters
- Automated formatting (Black or Ruff)

**REQ-A-084**: The system SHALL use static analysis:

- mypy for type checking (strict mode)
- ruff for linting
- Pre-commit hooks for automation
- CI/CD integration for enforcement

### 23.2 Code Organization

**REQ-A-085**: Code organization SHALL follow:

- One class per file (for large classes)
- Modules organized by layer
- Clear separation of concerns
- Minimal circular dependencies

**REQ-A-086**: Import organization SHALL follow:

- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetical within groups

---

## 24. Build and CI/CD Architecture

### 24.1 Build System

**REQ-A-087**: The system SHALL use modern Python tooling:

- Poetry for dependency management
- pyproject.toml for configuration
- Automated version bumping
- Lock file for reproducible builds

### 24.2 CI/CD Pipeline

**REQ-A-088**: The system SHALL implement CI/CD pipeline:

- Automated testing on commit
- Code quality checks
- Coverage reporting
- Automated deployment (future)

### 24.3 Release Process

**REQ-A-089**: The system SHALL follow release process:

- Changelog maintenance
- Version tagging
- Release notes generation
- Documentation updates

---

## 25. Migration and Evolution

### 25.1 Future Extensions

**REQ-A-090**: The architecture SHALL support future additions:

- Web API (REST or GraphQL)
- Web UI (React/Vue frontend)
- Database storage (for audit logs)
- Real-time processing (WebSocket streaming)
- Multi-tenancy support

### 25.2 Migration Strategy

**REQ-A-091**: The system SHALL support migrations:

- Configuration file migrations
- Data format migrations
- Backward compatibility layers
- Migration documentation

---

## 26. Directory Structure

**REQ-A-092**: The system SHALL follow this structure:

```text
anonymization-system/
├── pyproject.toml              # Project configuration
├── README.md                   # Project overview
├── LICENSE                     # License file
├── .env.example                # Example environment variables
│
├── src/
│   └── anonymization/
│       ├── __init__.py
│       │
│       ├── domain/             # Domain Layer (pure business logic)
│       │   ├── __init__.py
│       │   ├── models/         # Domain models
│       │   │   ├── __init__.py
│       │   │   ├── document.py
│       │   │   ├── entity_registry.py
│       │   │   ├── anonymization_mapping.py
│       │   │   ├── risk_assessment.py
│       │   │   └── validation_result.py
│       │   ├── services/       # Domain services
│       │   │   ├── __init__.py
│       │   │   ├── gdpr_compliance.py
│       │   │   └── risk_calculator.py
│       │   ├── ports/          # Interfaces (ports)
│       │   │   ├── __init__.py
│       │   │   ├── agent_interfaces.py
│       │   │   ├── llm_provider_interface.py
│       │   │   └── storage_interface.py
│       │   ├── agents/         # Agent definitions (NEW v2.0)
│       │   │   ├── __init__.py
│       │   │   ├── agent_definitions.py
│       │   │   └── prompts/
│       │   │       ├── __init__.py
│       │   │       ├── agent1_prompts.py
│       │   │       ├── agent2_prompts.py
│       │   │       └── agent3_prompts.py
│       │   └── exceptions.py   # Domain exceptions
│       │
│       ├── application/        # Application Layer (use cases)
│       │   ├── __init__.py
│       │   ├── orchestration/  # Orchestration strategies (NEW v2.0)
│       │   │   ├── __init__.py
│       │   │   ├── base_orchestrator.py
│       │   │   ├── sequential_orchestrator.py
│       │   │   └── autogen_orchestrator.py  # Optional
│       │   ├── use_cases/
│       │   │   ├── __init__.py
│       │   │   ├── anonymize_document.py
│       │   │   └── assess_risk.py
│       │   └── config.py       # Configuration models
│       │
│       ├── infrastructure/     # Infrastructure Layer (adapters)
│       │   ├── __init__.py
│       │   ├── adapters/
│       │   │   ├── __init__.py
│       │   │   ├── llm/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── base.py
│       │   │   │   ├── ollama_adapter.py
│       │   │   │   ├── claude_adapter.py
│       │   │   │   ├── openai_adapter.py
│       │   │   │   └── factory.py
│       │   │   ├── storage/
│       │   │   │   ├── __init__.py
│       │   │   │   └── file_system.py
│       │   │   └── reporting/
│       │   │       ├── __init__.py
│       │   │       ├── json_reporter.py
│       │   │       └── markdown_reporter.py
│       │   ├── agents/         # Agent implementations
│       │   │   ├── __init__.py
│       │   │   ├── agent1_anon_exec.py
│       │   │   ├── agent2_direct_check.py
│       │   │   └── agent3_risk_assess.py
│       │   └── config_loader.py
│       │
│       └── interfaces/         # User Interfaces
│           ├── __init__.py
│           └── cli/
│               ├── __init__.py
│               ├── main.py
│               └── commands.py
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── fixtures/              # Test fixtures
│   │   ├── __init__.py
│   │   ├── sample_documents.py
│   │   └── mock_responses.py
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/
│   └── e2e/
│
├── docs/                       # Documentation
│   ├── index.md
│   ├── architecture/
│   │   ├── overview.md
│   │   └── decisions/         # ADRs
│   ├── user-guide/
│   └── api/
│
├── config/                     # Configuration templates
│   ├── config.yaml.example
│   └── config.yaml
│
└── logs/                       # Log directory (gitignored)
```

**REQ-A-064A**: *[New v2.0]* Directory structure changes from v1.0:

- Added `domain/agents/` for agent definitions
- Added `domain/agents/prompts/` for agent prompt templates
- Added `application/orchestration/` for orchestration strategies
- Separated interface layer from infrastructure

---

## 27. Technology Stack Summary

**REQ-A-093**: *[v2.0]* The system SHALL use these core technologies:

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Language | Python | ≥3.10 | Core language |
| Dependency Mgmt | Poetry | Latest | Package management |
| Validation | Pydantic | ≥2.0 | Data validation |
| CLI | Click | ≥8.0 | Command-line interface |
| CLI UI | Rich | ≥13.0 | Terminal formatting |
| Logging | Loguru | ≥0.7 | Structured logging |
| Config | PyYAML | ≥6.0 | YAML parsing |
| Env Vars | python-dotenv | ≥1.0 | Environment config |
| HTTP Client | httpx | ≥0.27 | Async HTTP |
| Testing | pytest | ≥8.0 | Test framework |
| Async Testing | pytest-asyncio | ≥0.23 | Async test support |
| Coverage | pytest-cov | ≥4.1 | Code coverage |
| Type Checking | mypy | ≥1.8 | Static type analysis |
| Linting | Ruff | ≥0.1 | Fast linter |
| Web API (future) | FastAPI | ≥0.104 | REST API framework |

**Optional LLM Provider Libraries**:

- openai ≥1.0 (for OpenAI)
- anthropic ≥0.18 (for Claude)
- ollama ≥0.1 (for Ollama, or use httpx directly)

**Optional Orchestration Libraries**:

- pyautogen ≥0.2 (for AutoGen orchestration - if selected)

---

## 28. Design Patterns

**REQ-A-094**: The system SHALL apply these design patterns:

- **Hexagonal Architecture**: Overall structure
- **Modular Monolith**: Deployment model
- **Dependency Injection**: All dependencies
- **Factory Pattern**: LLM provider creation
- **Strategy Pattern**: Different anonymization techniques, orchestration strategies
- **Template Method**: Agent execution workflow
- **Repository Pattern**: Storage abstraction (if needed)
- **Builder Pattern**: Complex configuration assembly
- **Observer Pattern**: Logging and monitoring (implicit)
- **Adapter Pattern**: LLM provider adapters

---

## 29. Non-Functional Requirements

### 29.1 Maintainability

**REQ-A-095**: The system SHALL be maintainable:

- Clear separation of concerns
- Comprehensive documentation
- Consistent code style
- High test coverage
- Minimal technical debt

### 29.2 Scalability

**REQ-A-096**: The system SHALL scale:

- Horizontal: Process multiple documents in parallel
- Vertical: Handle larger documents efficiently
- Resource-efficient (memory, CPU)

### 29.3 Reliability

**REQ-A-097**: The system SHALL be reliable:

- Graceful error handling
- Retry mechanisms for transient failures
- Data integrity guarantees
- Audit trail for compliance

### 29.4 Usability

**REQ-A-098**: The system SHALL be usable:

- Clear CLI interface
- Helpful error messages
- Good defaults
- Comprehensive examples

---

## Appendix A: Requirement Traceability Matrix

| Requirement | Related Functional Requirements | Implementation Location |
|-------------|--------------------------------|------------------------|
| REQ-A-001 | REQ-F-001, REQ-F-002 | Overall architecture |
| REQ-A-011A | REQ-F-001, REQ-F-002, REQ-F-003 | domain/agents/ |
| REQ-A-011B | REQ-F-001, REQ-F-002, REQ-F-003 | domain/agents/prompts/ |
| REQ-A-023A | REQ-F-001 through REQ-F-005 | application/orchestration/ |
| REQ-A-033A | REQ-F-001, REQ-F-002 | infrastructure/agents/ |

---

## Appendix B: Architecture Decision Records (ADRs)

### ADR-001: Use Hexagonal Architecture

**Status**: Accepted
**Date**: 2025-10-03
**Context**: Need maintainable, testable architecture
**Decision**: Adopt hexagonal architecture
**Consequences**: Clear separation of concerns, easier testing, potential complexity

### ADR-002: Agent Prompts in Domain Layer

**Status**: Accepted
**Date**: 2025-10-06
**Context**: Prompts encode business logic about GDPR compliance
**Decision**: Move agent prompts to domain layer
**Consequences**: Prompts version-controlled with business logic, clearer ownership
**References**: Marta Fernández García's hexagonal architecture for AI agents

### ADR-003: Modular Monolith Deployment

**Status**: Accepted
**Date**: 2025-10-06
**Context**: Balance simplicity with architectural rigor
**Decision**: Deploy as modular monolith, not microservices
**Consequences**: Simpler deployment, easier debugging, possible future extraction

### ADR-004: Multiple Orchestration Strategies

**Status**: Accepted
**Date**: 2025-10-06
**Context**: Need flexibility for future complex agent interactions
**Decision**: Support pluggable orchestration strategies
**Consequences**: More initial complexity, future flexibility, configuration-driven

---

## Appendix C: Glossary

**Agent**: An autonomous component that performs a specific task using LLM capabilities

**Adapter**: Implementation of a port that connects to external systems

**Domain**: The business logic layer, independent of technical infrastructure

**Hexagonal Architecture**: Architectural pattern isolating business logic from external dependencies

**Modular Monolith**: Single deployable unit with clear internal module boundaries

**Orchestrator**: Component coordinating execution of multiple agents

**Port**: Interface defining contract between domain and infrastructure

**Prompt**: Text instruction to LLM defining expected behavior (domain asset)

---

**Document Version**: 2.0
**Last Updated**: 2025-10-06
**Status**: Active
**Related Documents**: Functional Requirements v1.0, Requirement Numbering System v1.0

**END OF ARCHITECTURAL REQUIREMENTS**ionale**: Modular monolith provides simplicity of deployment with architectural rigor, avoiding premature distribution while maintaining clean boundaries.

**REQ-A-002**: *[v2.0]* The system SHALL separate concerns into distinct layers:

- **Domain Layer**: Business logic, entities, domain services, agent definitions, agent prompts
- **Application Layer**: Use cases, orchestration, workflow
- **Infrastructure Layer**: External integrations, I/O, frameworks, agent implementations
- **Interface Layer**: User interfaces (CLI, API - future)

**REQ-A-002A**: *[New v2.0]* The system SHALL enforce strict dependency direction:

```text
Allowed:
  Interface    →  Application  →  Domain
      ↓              ↓
  Infrastructure  ←┘

Forbidden:
  Domain  →  Application  ✗
  Domain  →  Infrastructure  ✗
  Domain  →  Interface  ✗
  Application  →  Infrastructure  ✗ (except via ports)
```

**REQ-A-003**: The system SHALL ensure domain independence:

- Domain layer has ZERO dependencies on external libraries
- Domain layer does not know about LLM providers, file systems, or CLI
- Domain models are pure Python data structures

---

## 3. Layer Responsibilities

### 3.1 Domain Layer

**REQ-A-004**: *[v2.0]* The domain layer SHALL contain:

- **Domain Models**: Document, EntityRegistry, AnonymizationMapping, RiskAssessment, ValidationResult
- **Domain Services**: GDPRComplianceChecker, RiskCalculator
- **Domain Interfaces (Ports)**: IAgent1, IAgent2, IAgent3, ILLMProvider, ILLMSession
- **Business Rules**: Anonymization policies, risk scoring logic, GDPR compliance rules
- **Agent Definitions**: Agent roles, responsibilities, behavioral contracts
- **Agent Prompts**: Prompt templates encoding business rules

**REQ-A-005**: Domain models SHALL be:

- Immutable where possible (using dataclasses with frozen=True or Pydantic)
- Self-validating (enforce invariants)
- Rich in behavior (not anemic)
- Free of infrastructure concerns

**REQ-A-006**: Domain services SHALL:

- Encapsulate complex business logic
- Operate on domain models only
- Be stateless
- Have no side effects on external systems

### 3.2 Application Layer

**REQ-A-007**: The application layer SHALL contain:

- **Use Cases**: AnonymizeDocument, ValidateAnonymization, AssessRisk
- **Orchestrators**: AnonymizationOrchestrator (coordinates agents)
- **Application Services**: Workflow management, transaction boundaries
- **DTOs**: Data transfer objects for cross-layer communication (if needed)

**REQ-A-008**: The application layer SHALL:

- Orchestrate domain objects to fulfill use cases
- Manage transaction boundaries
- Handle application-level errors
- Coordinate infrastructure adapters

**REQ-A-009**: Orchestration SHALL support:

- Sequential agent execution (Agent 1 → 2 → 3)
- Conditional branching (retry loops)
- Parallel execution where safe (Agent 2 and 3)
- Error recovery and rollback

### 3.3 Infrastructure Layer

**REQ-A-010**: The infrastructure layer SHALL contain:

- **LLM Adapters**: OllamaAdapter, ClaudeAdapter, OpenAIAdapter
- **Storage Adapters**: FileSystemStorage, ConfigLoader
- **Reporting Adapters**: JSONReporter, MarkdownReporter
- **Agent Implementations**: Agent1_ANON_EXEC, Agent2_DIRECT_CHECK, Agent3_RISK_ASSESS
- **CLI Adapter**: Command-line interface implementation

**REQ-A-011**: Infrastructure adapters SHALL:

- Implement domain ports (interfaces)
- Handle external communication
- Translate between external formats and domain models
- Manage connections and resources

### 3.4 Agent Definitions and Prompts

**REQ-A-011A**: *[New v2.0]* Agent **definitions** SHALL reside in domain layer:

**Location**: `domain/agents/`

**Content**:

- Agent roles and responsibilities
- Agent behavioral contracts
- Agent cognitive models (what they do, not how)
- Success criteria for each agent

**REQ-A-011B**: *[New v2.0]* Agent **prompts** SHALL reside in domain layer:

**Location**: `domain/agents/prompts/`

**Content**:

- Prompt templates for each agent
- System prompts encoding business rules
- Example prompts demonstrating desired behavior
- Prompt validation rules

**Rationale**: Prompts encode domain expertise (GDPR rules, anonymization techniques, risk assessment criteria). They define what agents should do, which is domain logic, not infrastructure machinery.

---

## 4. Dependency Management

### 4.1 Dependency Inversion

**REQ-A-012**: The system SHALL apply dependency inversion principle:

- High-level modules (domain) do not depend on low-level modules (infrastructure)
- Both depend on abstractions (interfaces/ports)
- Infrastructure implements domain-defined interfaces

**REQ-A-013**: Dependencies SHALL flow inward:

```text
CLI → Application → Domain
     ↓           ↓
Infrastructure ←┘
```

### 4.2 Dependency Injection

**REQ-A-014**: The system SHALL use dependency injection:

- Constructor injection for all dependencies
- No service locator pattern
- Composition root in main.py
- Configuration-driven assembly

**REQ-A-015**: The system SHALL support multiple DI approaches:

- Manual composition (for simplicity)
- DI container (if complexity grows)
- Factory pattern for complex object creation

### 4.3 Module Independence

**REQ-A-015A**: *[New v2.0]* Module imports SHALL be restricted:

- Domain module imports: NONE (except Python stdlib)
- Application module imports: domain only
- Infrastructure module imports: domain, application (via ports)
- Interface module imports: all layers (for DI composition)

### 4.4 Orchestration Framework Consideration

**REQ-A-023A**: *[New v2.0]* The system SHALL support **multiple orchestration strategies**:

```text
application/orchestration/
├── base_orchestrator.py        # Abstract interface
├── sequential_orchestrator.py  # Current manual approach
└── autogen_orchestrator.py     # Future AutoGen approach (optional)
```

**REQ-A-023B**: *[New v2.0]* AutoGen integration (if selected) SHALL:

- Be implemented as an orchestration adapter in application layer
- Implement the same orchestrator interface
- Use domain-defined agent ports
- Not leak into domain layer
- Be swappable with other orchestration strategies

**Decision Criteria for AutoGen**:

- Use if workflow complexity exceeds 3 agents
- Use if dynamic agent selection needed
- Use if complex conversation flows required
- Otherwise, use sequential orchestrator

---

## 5. Interface Design (Ports)

### 5.1 Agent Interfaces

**REQ-A-016**: Agent interfaces SHALL be defined in domain layer:

```python
# domain/ports/agent_interfaces.py

class IAgent1_ANON_EXEC(Protocol):
    """Port for anonymization execution agent"""
    async def execute(
        self, 
        document: Document
    ) -> tuple[Document, EntityRegistry, AnonymizationMapping]:
        ...

class IAgent2_DIRECT_CHECK(Protocol):
    """Port for direct identifier verification agent"""
    async def verify(
        self, 
        document: Document
    ) -> ValidationResult:
        ...

class IAgent3_RISK_ASSESS(Protocol):
    """Port for risk assessment agent"""
    async def assess(
        self, 
        document: Document, 
        mapping: AnonymizationMapping
    ) -> RiskAssessment:
        ...
```

**REQ-A-017**: Interfaces SHALL use Python Protocols (PEP 544):

- Structural typing for flexibility
- No inheritance required
- Clear contracts

### 5.2 LLM Provider Interface

**REQ-A-018**: LLM provider interface SHALL abstract LLM communication:

```python
# domain/ports/llm_provider_interface.py

class ILLMProvider(Protocol):
    """Port for LLM provider abstraction"""
    
    async def invoke(
        self,
        system_prompt: str,
        user_message: str,
        config: LLMConfig
    ) -> str:
        """Single stateless call to LLM"""
        ...
    
    async def create_session(self) -> ILLMSession:
        """Create stateful conversation session"""
        ...

class ILLMSession(Protocol):
    """Port for stateful LLM conversation"""
    
    async def send(self, message: str) -> str:
        """Send message in session context"""
        ...
    
    def get_history(self) -> list[Message]:
        """Retrieve conversation history"""
        ...
    
    async def close(self):
        """Clean up session resources"""
        ...
```

### 5.3 Storage Interface

**REQ-A-019**: Storage interface SHALL abstract file operations:

```python
# domain/ports/storage_interface.py

class IDocumentStorage(Protocol):
    """Port for document storage operations"""
    
    async def read(self, path: str) -> Document:
        ...
    
    async def write(self, document: Document, path: str) -> None:
        ...
    
    async def exists(self, path: str) -> bool:
        ...
```

---

## 6. Adapter Implementation

### 6.1 LLM Adapters

**REQ-A-020**: Each LLM adapter SHALL implement ILLMProvider:

- Handle provider-specific authentication
- Translate generic config to provider format
- Manage rate limiting and retries
- Handle provider-specific errors

**REQ-A-021**: LLM adapters SHALL be interchangeable:

- Same interface for all providers
- Configuration-driven selection
- No business logic in adapters

**REQ-A-022**: LLM adapters SHALL support both usage patterns:

- Stateless invocation (single calls)
- Stateful sessions (conversation history)

### 6.2 Agent Implementations

**REQ-A-023** (original version): *[Deprecated v2.0]*

- **Original text**: "Agent implementations SHALL reside in infrastructure layer"
- **Reason**: Oversimplified. Split into REQ-A-023A (orchestration) and REQ-A-033A (agent responsibilities)
- **Migration**: See REQ-A-023A, REQ-A-023B, REQ-A-033A for current requirements
- **Deprecated date**: 2025-10-06

**REQ-A-024**: Agent internal architecture SHALL support:

- Multiple LLM calls within single session
- Chunking strategies (for Agent 1)
- Self-verification mechanisms
- Structured output parsing

### 6.3 Agent Implementation Responsibilities

**REQ-A-033A**: *[New v2.0]* Agent implementation responsibilities:

**What agents do** (infrastructure concerns):

- Execute LLM API calls via ILLMProvider
- Parse JSON responses from LLM
- Handle malformed responses
- Retry transient failures
- Manage session state (if needed)

**What agents don't do** (domain concerns - handled by prompts/definitions):

- Define what to ask LLM (prompts are in domain)
- Define business rules (in domain services)
- Define validation criteria (in domain models)

---

## 7. Asynchronous Architecture

### 7.1 Async/Await Pattern

**REQ-A-025**: The system SHALL use async/await for I/O operations:

- All LLM calls are async
- All file operations are async
- All agent methods are async
- Application orchestration is async

**REQ-A-026**: The system SHALL use asyncio for concurrency:

- Parallel LLM calls where appropriate (chunked processing)
- Concurrent agent execution (Agent 2 & 3)
- Efficient resource utilization

**REQ-A-027**: The system SHALL provide sync wrappers where needed:

- CLI entry point can be sync (using asyncio.run)
- Synchronous convenience methods for simple use cases

### 7.2 HTTP Client Requirements

**REQ-A-028**: The system SHALL use async HTTP client:

- httpx for async HTTP requests
- Connection pooling for efficiency
- Timeout configuration
- Retry mechanisms

---

## 8. Configuration Architecture

### 8.1 Configuration Management

**REQ-A-029**: The system SHALL support hierarchical configuration:

- Default configuration embedded in code
- User configuration file (config.yaml)
- Environment variables (for secrets)
- Command-line arguments (highest priority)

**REQ-A-030**: Configuration SHALL be type-safe:

- Use Pydantic models for configuration
- Validation on load
- Clear error messages for invalid config

**REQ-A-031**: Configuration structure SHALL include:

```yaml
llm:
  provider: "claude"  # ollama | claude | openai
  model: "claude-sonnet-4.5"
  temperature: 0.1
  max_tokens: 4096
  
  ollama:
    base_url: "http://localhost:11434"
  
  claude:
    api_key_env: "ANTHROPIC_API_KEY"
  
  openai:
    api_key_env: "OPENAI_API_KEY"
    organization: null

agents:
  agent1:
    chunk_size: 30
    overlap: 5
    max_full_document_lines: 150
    session_strategy: "single"  # single | multi
  
  agent2:
    strictness: "normal"  # strict | normal | lenient
    max_iterations: 3
  
  agent3:
    require_full_document: true
    dimension_weights:
      uniqueness: 1.0
      population_size: 1.0
      external_correlation: 1.0
      temporal_patterns: 1.0
      context_richness: 1.0

orchestration:
  strategy: "sequential"  # sequential | autogen | parallel

gdpr:
  risk_thresholds:
    critical: [21, 25]
    high: [16, 20]
    medium: [11, 15]
    low: [6, 10]
    negligible: [1, 5]
  
  compliance_level: "strict"  # strict | moderate | lenient

output:
  report_format: "markdown"  # json | markdown | both
  include_mapping_log: true
  audit_logging: true

performance:
  enable_parallel_processing: true
  max_concurrent_chunks: 5
  timeout_seconds: 300
```

### 8.2 Secrets Management

**REQ-A-032**: The system SHALL handle secrets securely:

- API keys NEVER in configuration files
- API keys from environment variables only
- Support for .env files (via python-dotenv)
- Clear error messages when API keys missing

---

## 9. Error Handling Architecture

### 9.1 Error Hierarchy

**REQ-A-033**: The system SHALL define custom exception hierarchy:

```python
# domain/exceptions.py

class AnonymizationError(Exception):
    """Base exception for anonymization system"""
    pass

class DocumentError(AnonymizationError):
    """Document processing errors"""
    pass

class ValidationError(AnonymizationError):
    """Validation failures"""
    pass

class RiskAssessmentError(AnonymizationError):
    """Risk assessment failures"""
    pass

class LLMProviderError(AnonymizationError):
    """LLM provider communication errors"""
    pass

class ConfigurationError(AnonymizationError):
    """Configuration errors"""
    pass
```

**REQ-A-034**: Error handling SHALL follow layers:

- Domain layer: Raises domain exceptions
- Application layer: Catches and translates exceptions
- Infrastructure layer: Catches external exceptions, wraps in domain exceptions
- CLI layer: Catches all exceptions, provides user-friendly messages

### 9.2 Error Recovery

**REQ-A-035**: The system SHALL implement retry mechanisms:

- Exponential backoff for transient failures
- Configurable retry limits
- Specific retry logic for rate limiting
- Preserve partial results on failure

**REQ-A-036**: The system SHALL provide error context:

- Stack traces in debug mode
- User-friendly messages in production
- Suggestions for remediation
- Log correlation IDs for troubleshooting

---

## 10. Logging Architecture

### 10.1 Logging Strategy

**REQ-A-037**: The system SHALL use structured logging:

- Loguru for logging framework
- JSON format for machine-readable logs
- Human-readable format for console
- Contextual information in all log entries

**REQ-A-038**: Logging levels SHALL be applied consistently:

- **DEBUG**: Internal state, detailed execution flow
- **INFO**: High-level operations (document processed, agent completed)
- **WARNING**: Recoverable issues (retry attempts, validation warnings)
- **ERROR**: Failures requiring attention
- **CRITICAL**: System-level failures

**REQ-A-039**: The system SHALL support multiple log outputs:

- Console (stderr) for interactive use
- File rotation for persistent logs
- JSON logs for audit trail (GDPR requirement)

### 10.2 GDPR Audit Logging

**REQ-A-040**: The system SHALL maintain GDPR-compliant audit trail:

- Log all anonymization operations
- Include: timestamp, user (if applicable), document ID, configuration
- Record: entities identified, anonymization techniques applied, risk scores
- Store audit logs separately with retention policy
- Support export for compliance audits

**REQ-A-041**: Audit logs SHALL be immutable:

- Append-only log files
- Integrity verification (checksums)
- No modification or deletion (within retention period)

---

## 11. Testing Architecture

### 11.1 Test Strategy

**REQ-A-042**: The system SHALL support multiple test levels:

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test adapter integration with external systems
- **End-to-end tests**: Test complete workflows
- **Contract tests**: Verify interface contracts

**REQ-A-043**: Test structure SHALL mirror source structure:

```text
tests/
├── unit/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── integration/
├── e2e/
└── fixtures/
```

### 11.2 Test Isolation

**REQ-A-044**: Tests SHALL be isolated:

- No dependencies on external services (use mocks)
- No file system dependencies (use in-memory or temp)
- No network calls (mock HTTP)
- Deterministic and repeatable

**REQ-A-045**: The system SHALL provide test fixtures:

- Mock LLM provider with predefined responses
- Sample documents (various sizes and complexities)
- Expected outputs for validation
- Configuration fixtures

### 11.3 Mock Architecture

**REQ-A-046**: The system SHALL provide comprehensive mocks:

```python
# tests/mocks/mock_llm_provider.py

class MockLLMProvider(ILLMProvider):
    """Mock LLM provider for testing without API calls"""
    
    def __init__(self, responses: dict[str, str]):
        self.responses = responses
        self.call_history: list[dict] = []
    
    async def invoke(
        self, 
        system_prompt: str, 
        user_message: str, 
        config: LLMConfig
    ) -> str:
        self.call_history.append({
            "system_prompt": system_prompt,
            "user_message": user_message,
            "config": config
        })
        
        # Return predefined response based on keywords
        for keyword, response in self.responses.items():
            if keyword in user_message:
                return response
        
        return "Mock default response"
    
    async def create_session(self) -> ILLMSession:
        return MockLLMSession(self.responses)
```

**REQ-A-047**: Mock implementations SHALL:

- Track all invocations for verification
- Support predefined response sequences
- Simulate errors when needed
- Provide assertion helpers

### 11.4 Test Coverage Requirements

**REQ-A-048**: The system SHALL maintain test coverage:

- Minimum 80% code coverage overall
- 90% coverage for domain layer
- 70% coverage for infrastructure layer
- Coverage reports generated automatically

**REQ-A-049**: Critical paths SHALL have 100% coverage:

- All agent execution paths
- GDPR compliance logic
- Risk calculation algorithms
- Anonymization mapping logic

---

## 12. Performance Architecture

### 12.1 Performance Requirements

**REQ-A-050**: The system SHALL be designed for performance:

- Async I/O for all external calls
- Parallel processing where safe
- Efficient memory usage (streaming for large documents)
- Connection pooling for HTTP clients

**REQ-A-051**: The system SHALL support performance tuning:

- Configurable timeouts
- Adjustable parallelism levels
- Batch size configuration
- Cache strategies (if applicable)

### 12.2 Resource Management

**REQ-A-052**: The system SHALL manage resources efficiently:

- Context managers for file handles
- Proper cleanup of HTTP connections
- LLM session lifecycle management
- Memory cleanup after processing

**REQ-A-053**: The system SHALL handle large documents:

- Streaming parsing where possible
- Chunked processing with memory limits
- Progress reporting for long operations
- Graceful degradation for very large inputs

---

## 13. Extensibility Architecture

### 13.1 Plugin Architecture

**REQ-A-054**: The system SHALL support extensibility through:

- Interface-based plugin system
- Dynamic provider loading (for LLM providers)
- Custom agent implementation support
- Custom anonymization rule plugins

**REQ-A-055**: New LLM providers SHALL be addable via:

1. Implement ILLMProvider interface
2. Register in provider factory
3. Add configuration section
4. No changes to domain or application layers

**REQ-A-056**: New agents SHALL be addable via:

1. Define agent interface (IAgent4, etc.)
2. Implement agent in infrastructure layer
3. Update orchestrator configuration
4. Add agent-specific configuration

### 13.2 Configuration-Driven Behavior

**REQ-A-057**: The system SHALL support configuration-driven features:

- Enable/disable agents via configuration
- Customize workflow sequence
- Select anonymization techniques
- Configure risk scoring weights

---

## 14. Security Architecture

### 14.1 Data Security

**REQ-A-058**: The system SHALL protect sensitive data:

- Original documents never logged
- Personal data masked in logs
- Mapping logs encrypted at rest (optional)
- Secure temporary file handling

**REQ-A-059**: The system SHALL sanitize outputs:

- No API keys in error messages
- No internal paths in user-facing output
- No sensitive data in logs
- Stack traces only in debug mode

### 14.2 API Security

**REQ-A-060**: The system SHALL secure API communication:

- HTTPS only for all external calls
- API key rotation support
- Timeout enforcement
- Certificate verification

### 14.3 Access Control

**REQ-A-061**: The system SHALL support access control (future):

- User authentication (if API developed)
- Role-based access to mapping logs
- Audit trail for all access
- Separation of duties

---

## 15. Deployment Architecture

### 15.1 Packaging

**REQ-A-062**: The system SHALL be packaged as:

- Python package installable via pip
- Self-contained with all dependencies
- Entry point for CLI command
- Versioned releases

**REQ-A-063**: The system SHALL support multiple deployment modes:

- Local installation (pip install)
- Docker container (future)
- Cloud deployment (future)
- Standalone executable (future)

### 15.2 Environment Requirements

**REQ-A-064**: The system SHALL specify environment requirements:

- Python 3.10+ required
- Operating system compatibility (Linux, macOS, Windows)
- Memory requirements (minimum 2GB recommended)
- Disk space for logs and temporary files

### 15.3 Configuration Management

**REQ-A-065**: The system SHALL support deployment configuration:

- Environment-specific config files
- Environment variable overrides
- Configuration validation on startup
- Clear error messages for misconfiguration

---

## 16. Monitoring and Observability

### 16.1 Metrics Collection

**REQ-A-066**: The system SHALL collect operational metrics:

- Processing time per document
- Agent execution times
- LLM call latency and token usage
- Error rates by type
- Success/failure rates

**REQ-A-067**: Metrics SHALL be exposed via:

- Log files (structured format)
- Metrics export (Prometheus format - future)
- Health check endpoint (if API mode)

### 16.2 Tracing

**REQ-A-068**: The system SHALL support distributed tracing:

- Correlation IDs for all operations
- Parent-child relationship tracking (agent calls)
- End-to-end request tracing
- Performance bottleneck identification

### 16.3 Health Checks

**REQ-A-069**: The system SHALL provide health checks:

- LLM provider connectivity
- Configuration validity
- File system access
- Memory availability

---

## 17. Documentation Architecture

### 17.1 Code Documentation

**REQ-A-070**: The system SHALL maintain code documentation:

- Docstrings for all public interfaces
- Type hints for all functions
- Inline comments for complex logic
- Architecture decision records (ADRs)

**REQ-A-071**: Documentation style SHALL follow:

- Google-style docstrings
- PEP 257 conventions
- Sphinx-compatible format

### 17.2 API Documentation

**REQ-A-072**: The system SHALL provide API documentation:

- Interface contracts documented
- Usage examples for each interface
- Integration guides for each LLM provider
- Agent implementation guide

### 17.3 User Documentation

**REQ-A-073**: The system SHALL include user documentation:

- Installation guide
- Quick start guide
- Configuration reference
- CLI command reference
- Troubleshooting guide
- GDPR compliance guide

---

## 18. Data Flow Architecture

### 18.1 Request Flow

**REQ-A-074**: The system SHALL follow this data flow:

```text
User Input (CLI)
    ↓
CLI Adapter (parse arguments, load config)
    ↓
Application Orchestrator
    ↓
┌─────────────────────────────────────┐
│ Agent 1 (ANON-EXEC)                 │
│   ↓                                 │
│ LLM Provider → Multiple calls       │
│   ↓                                 │
│ Return: Anonymized Doc + Mapping    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Agent 2 (DIRECT-CHECK)              │
│   ↓                                 │
│ LLM Provider → Verification         │
│   ↓                                 │
│ Return: ValidationResult            │
└─────────────────────────────────────┘
    ↓
  [If FAIL: Loop back to Agent 1]
    ↓
  [If PASS: Continue]
    ↓
┌─────────────────────────────────────┐
│ Agent 3 (RISK-ASSESS)               │
│   ↓                                 │
│ LLM Provider → Risk analysis        │
│   ↓                                 │
│ Return: RiskAssessment              │
└─────────────────────────────────────┘
    ↓
Application Orchestrator (aggregate results)
    ↓
Output Adapters (write files, generate reports)
    ↓
User Output (files + console summary)
```

### 18.2 Data Transformation

**REQ-A-075**: Data transformations SHALL be explicit:

- Input parsing: CLI args → Configuration + Document
- Domain translation: Document → LLM prompts
- Result parsing: LLM responses → Domain models
- Output formatting: Domain models → Reports

**REQ-A-076**: The system SHALL validate data at boundaries:

- Input validation at CLI layer
- Domain model validation on construction
- Output validation before writing

---

## 19. Agentic Architecture Principles

### 19.1 Agent Cognitive Architecture

**REQ-A-073A**: *[New v2.0]* Agent cognitive architecture SHALL separate:

**Domain Concerns** (what agents do):

- Agent roles and responsibilities
- Behavioral contracts
- Decision-making criteria
- Business rules encoded in prompts
- Success/failure criteria

**Infrastructure Concerns** (how agents execute):

- LLM API interaction
- Response parsing
- Retry logic
- Session management
- Error handling

**REQ-A-074A**: *[New v2.0]* Agent prompts SHALL be treated as domain assets:

- Version controlled alongside domain code
- Testable independently
- Documented with examples
- Contain business expertise
- Define expected agent behavior

**Rationale**: Following Marta Fernández García's approach, prompts encode the agent's "cognitive model" - the business logic of what the agent should do. This is domain knowledge, not infrastructure machinery.

### 19.2 Agent Interaction Patterns

**REQ-A-075A**: *[New v2.0]* Agent interaction SHALL support:

**Current State** (Sequential):

- Agent 1 → produces output
- Agent 2 → verifies output
- Agent 3 → assesses risk
- Orchestrator manages sequence

**Future State** (Conversational - Optional):

- Agents communicate via messages
- Shared conversation context
- Dynamic agent selection
- Managed by AutoGen or similar

**REQ-A-076A**: *[New v2.0]* Agent outputs SHALL be:

- Structured (domain models, not strings)
- Validated on creation
- Immutable once created
- Traceable to source agent

### 19.3 Orchestration Patterns

**REQ-A-077A**: *[New v2.0]* The system SHALL support multiple orchestration patterns:

**Pattern 1: Sequential** (Current)

- Linear execution flow
- Manual error handling
- Direct control over agent sequence
- Simple to understand and debug

**Pattern 2: AutoGen GroupChat** (Future)

- Agent-to-agent communication
- Dynamic agent selection
- Conversation-based workflow
- Complex interaction patterns

**Pattern 3: Parallel Execution** (Future)

- Independent agent execution
- Result aggregation
- Performance optimization
- Requires careful coordination

**REQ-A-078A**: *[New v2.0]* Orchestration selection SHALL be:

- Configuration-driven
- Swappable without domain changes
- Transparent to interface layer
- Documented with trade-offs

**REQ-A-078B**: *[New v2.0]* Agent state management SHALL:

- Maintain conversation context when needed
- Support stateless operation as default
- Clear session lifecycle
- No global mutable state

---

## 20. Modular Monolith Principles

### 20.1 Module Definition

**REQ-A-079A**: *[New v2.0]* Modules SHALL be defined by hexagonal layers:

- Each layer is a module
- Clear interfaces between layers
- No circular dependencies between layers
- Modules communicate via ports only

**REQ-A-080A**: *[New v2.0]* Module independence SHALL be enforced:

- Domain module imports: NONE (except stdlib)
- Application module imports: domain only
- Infrastructure module imports: domain, application (via ports)
- Interface module imports: all layers (for DI)

### 20.2 Deployment Model

**REQ-A-081A**: *[New v2.0]* Modular monolith deployment SHALL be:

- Single Python package
- Single process (with async concurrency)
- Single database connection pool (if database added)
- Single configuration file
- Deployed as one unit

**Benefits**:

- Simple deployment
- No distributed system complexity
- Easier debugging
- Lower latency
- Transactional consistency

### 20.3 Future Microservices Extraction

**REQ-A-082A**: *[New v2.0]* Future microservices extraction SHALL be possible:

- Each layer can become a service if needed
- Ports become API boundaries
- Domain models become shared contracts
- But premature extraction is avoided

### 20.4 Module Boundaries

**REQ-A-083A**: *[New v2.0]* Module boundaries SHALL use explicit contracts:

- Python Protocols for interfaces
- Pydantic models for data contracts
- Comprehensive type hints
- Contract tests at module boundaries

**REQ-A-084A**: *[New v2.0]* Breaking changes SHALL be managed:

- Deprecation warnings before removal
- Version compatibility layers
- Migration guides
- Backward compatibility where feasible

**REQ-A-084B**: *[New v2.0]* Module cohesion SHALL be maximized:

- Related functionality grouped together
- Single responsibility per module
- Minimal cross-module dependencies
- High internal coupling, low external coupling

---

## 21. Concurrency Architecture

### 21.1 Concurrency Model

**REQ-A-077**: The system SHALL use single-threaded async model:

- One event loop per process
- Async/await for concurrency
- No threading or multiprocessing (initially)
- asyncio.gather for parallel operations

**REQ-A-078**: The system SHALL support safe parallelization:

- Parallel chunk processing (Agent 1)
- Parallel agent execution (Agent 2 & 3)
- Batch document processing
- No shared mutable state

### 21.2 Synchronization

**REQ-A-079**: The system SHALL manage synchronization:

- Locks only where necessary (minimize)
- Atomic operations for shared resources
- Clear ownership of mutable state
- Immutable domain models preferred

---

## 22. Versioning and Compatibility

### 22.1 Semantic Versioning

**REQ-A-080**: The system SHALL use semantic versioning:

- MAJOR.MINOR.PATCH format
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### 22.2 API Stability

**REQ-A-081**: The system SHALL maintain API stability:

- Domain interfaces are stable (avoid breaking changes)
- Deprecation warnings before removal
- Migration guides for breaking changes
- Backward compatibility for configuration (where possible)

### 22.3 LLM Provider Compatibility

**REQ-A-082**: The system SHALL handle provider changes:

- Version pinning for provider libraries
- Adapter layer isolates provider API changes
- Graceful degradation if provider unavailable
- Clear error messages for incompatible versions

---

## 23. Code Quality Architecture

### 23.1 Code Style

**REQ-A-083**: The system SHALL enforce code style:

- PEP 8 compliance
- Type hints for all public interfaces
- Maximum line length: 100 characters
- Automated formatting (Black or Ruff)

**REQ-A-084**: The system SHALL use static analysis:

- mypy for type checking (strict mode)
- ruff for linting
- Pre-commit hooks for automation
- CI/CD integration for enforcement

### 23.2 Code Organization

**REQ-A-085**: Code organization SHALL follow:

- One class per file (for large classes)
- Modules organized by layer
- Clear separation of concerns
- Minimal circular dependencies

**REQ-A-086**: Import organization SHALL follow:

- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetical within groups

---

## 24. Build and CI/CD Architecture

### 24.1 Build System

**REQ-A-087**: The system SHALL use modern Python tooling:

- Poetry for dependency management
- pyproject.toml for configuration
- Automated version bumping
- Lock file for reproducible builds

### 24.2 CI/CD Pipeline

**REQ-A-088**: The system SHALL implement CI/CD pipeline:

- Automated testing on commit
- Code quality checks
- Coverage reporting
- Automated deployment (future)

### 24.3 Release Process

**REQ-A-089**: The system SHALL follow release process:

- Changelog maintenance
- Version tagging
- Release notes generation
- Documentation updates

---

## 25. Migration and Evolution

### 25.1 Future Extensions

**REQ-A-090**: The architecture SHALL support future additions:

- Web API (REST or GraphQL)
- Web UI (React/Vue frontend)
- Database storage (for audit logs)
- Real-time processing (WebSocket streaming)
- Multi-tenancy support

### 25.2 Migration Strategy

**REQ-A-091**: The system SHALL support migrations:

- Configuration file migrations
- Data format migrations
- Backward compatibility layers
- Migration documentation

---

## 26. Directory Structure

**REQ-A-092**: The system SHALL follow this structure:

```text
anonymization-system/
├── pyproject.toml              # Project configuration
├── README.md                   # Project overview
├── LICENSE                     # License file
├── .env.example                # Example environment variables
│
├── src/
│   └── anonymization/
│       ├── __init__.py
│       │
│       ├── domain/             # Domain Layer (pure business logic)
│       │   ├── __init__.py
│       │   ├── models/         # Domain models
│       │   │   ├── __init__.py
│       │   │   ├── document.py
│       │   │   ├── entity_registry.py
│       │   │   ├── anonymization_mapping.py
│       │   │   ├── risk_assessment.py
│       │   │   └── validation_result.py
│       │   ├── services/       # Domain services
│       │   │   ├── __init__.py
│       │   │   ├── gdpr_compliance.py
│       │   │   └── risk_calculator.py
│       │   ├── ports/          # Interfaces (ports)
│       │   │   ├── __init__.py
│       │   │   ├── agent_interfaces.py
│       │   │   ├── llm_provider_interface.py
│       │   │   └── storage_interface.py
│       │   ├── agents/         # Agent definitions (NEW v2.0)
│       │   │   ├── __init__.py
│       │   │   ├── agent_definitions.py
│       │   │   └── prompts/
│       │   │       ├── __init__.py
│       │   │       ├── agent1_prompts.py
│       │   │       ├── agent2_prompts.py
│       │   │       └── agent3_prompts.py
│       │   └── exceptions.py   # Domain exceptions
│       │
│       ├── application/        # Application Layer (use cases)
│       │   ├── __init__.py
│       │   ├── orchestration/  # Orchestration strategies (NEW v2.0)
│       │   │   ├── __init__.py
│       │   │   ├── base_orchestrator.py
│       │   │   ├── sequential_orchestrator.py
│       │   │   └── autogen_orchestrator.py  # Optional
│       │   ├── use_cases/
│       │   │   ├── __init__.py
│       │   │   ├── anonymize_document.py
│       │   │   └── assess_risk.py
│       │   └── config.py       # Configuration models
│       │
│       ├── infrastructure/     # Infrastructure Layer (adapters)
│       │   ├── __init__.py
│       │   ├── adapters/
│       │   │   ├── __init__.py
│       │   │   ├── llm/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── base.py
│       │   │   │   ├── ollama_adapter.py
│       │   │   │   ├── claude_adapter.py
│       │   │   │   ├── openai_adapter.py
│       │   │   │   └── factory.py
│       │   │   ├── storage/
│       │   │   │   ├── __init__.py
│       │   │   │   └── file_system.py
│       │   │   └── reporting/
│       │   │       ├── __init__.py
│       │   │       ├── json_reporter.py
│       │   │       └── markdown_reporter.py
│       │   ├── agents/         # Agent implementations
│       │   │   ├── __init__.py
│       │   │   ├── agent1_anon_exec.py
│       │   │   ├── agent2_direct_check.py
│       │   │   └── agent3_risk_assess.py
│       │   └── config_loader.py
│       │
│       └── interfaces/         # User Interfaces
│           ├── __init__.py
│           └── cli/
│               ├── __init__.py
│               ├── main.py
│               └── commands.py
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── fixtures/              # Test fixtures
│   │   ├── __init__.py
│   │   ├── sample_documents.py
│   │   └── mock_responses.py
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/
│   └── e2e/
│
├── docs/                       # Documentation
│   ├── index.md
│   ├── architecture/
│   │   ├── overview.md
│   │   └── decisions/         # ADRs
│   ├── user-guide/
│   └── api/
│
├── config/                     # Configuration templates
│   ├── config.yaml.example
│   └── config.yaml
│
└── logs/                       # Log directory (gitignored)
```

**REQ-A-064A**: *[New v2.0]* Directory structure changes from v1.0:

- Added `domain/agents/` for agent definitions
- Added `domain/agents/prompts/` for agent prompt templates
- Added `application/orchestration/` for orchestration strategies
- Separated interface layer from infrastructure

---

## 27. Technology Stack Summary

**REQ-A-093**: *[v2.0]* The system SHALL use these core technologies:

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Language | Python | ≥3.10 | Core language |
| Dependency Mgmt | Poetry | Latest | Package management |
| Validation | Pydantic | ≥2.0 | Data validation |
| CLI | Click | ≥8.0 | Command-line interface |
| CLI UI | Rich | ≥13.0 | Terminal formatting |
| Logging | Loguru | ≥0.7 | Structured logging |
| Config | PyYAML | ≥6.0 | YAML parsing |
| Env Vars | python-dotenv | ≥1.0 | Environment config |
| HTTP Client | httpx | ≥0.27 | Async HTTP |
| Testing | pytest | ≥8.0 | Test framework |
| Async Testing | pytest-asyncio | ≥0.23 | Async test support |
| Coverage | pytest-cov | ≥4.1 | Code coverage |
| Type Checking | mypy | ≥1.8 | Static type analysis |
| Linting | Ruff | ≥0.1 | Fast linter |
| Web API (future) | FastAPI | ≥0.104 | REST API framework |

**Optional LLM Provider Libraries**:

- openai ≥1.0 (for OpenAI)
- anthropic ≥0.18 (for Claude)
- ollama ≥0.1 (for Ollama, or use httpx directly)

**Optional Orchestration Libraries**:

- pyautogen ≥0.2 (for AutoGen orchestration - if selected)

---

## 28. Design Patterns

**REQ-A-094**: The system SHALL apply these design patterns:

- **Hexagonal Architecture**: Overall structure
- **Modular Monolith**: Deployment model
- **Dependency Injection**: All dependencies
- **Factory Pattern**: LLM provider creation
- **Strategy Pattern**: Different anonymization techniques, orchestration strategies
- **Template Method**: Agent execution workflow
- **Repository Pattern**: Storage abstraction (if needed)
- **Builder Pattern**: Complex configuration assembly
- **Observer Pattern**: Logging and monitoring (implicit)
- **Adapter Pattern**: LLM provider adapters

---

## 29. Non-Functional Requirements

### 29.1 Maintainability

**REQ-A-095**: The system SHALL be maintainable:

- Clear separation of concerns
- Comprehensive documentation
- Consistent code style
- High test coverage
- Minimal technical debt

### 29.2 Scalability

**REQ-A-096**: The system SHALL scale:

- Horizontal: Process multiple documents in parallel
- Vertical: Handle larger documents efficiently
- Resource-efficient (memory, CPU)

### 29.3 Reliability

**REQ-A-097**: The system SHALL be reliable:

- Graceful error handling
- Retry mechanisms for transient failures
- Data integrity guarantees
- Audit trail for compliance

### 29.4 Usability

**REQ-A-098**: The system SHALL be usable:

- Clear CLI interface
- Helpful error messages
- Good defaults
- Comprehensive examples

---

## Appendix A: Requirement Traceability Matrix

| Requirement | Related Functional Requirements | Implementation Location |
|-------------|--------------------------------|------------------------|
| REQ-A-001 | REQ-F-001, REQ-F-002 | Overall architecture |
| REQ-A-001A | REQ-F-001 through REQ-F-005 | Overall architecture |
| REQ-A-011A | REQ-F-001, REQ-F-002, REQ-F-003 | domain/agents/ |
| REQ-A-011B | REQ-F-001, REQ-F-002, REQ-F-003 | domain/agents/prompts/ |
| REQ-A-023A | REQ-F-001 through REQ-F-005 | application/orchestration/ |
| REQ-A-033A | REQ-F-001, REQ-F-002 | infrastructure/agents/ |

---

## Appendix B: Architecture Decision Records (ADRs)

### ADR-001: Use Hexagonal Architecture

**Status**: Accepted
**Date**: 2025-10-03
**Context**: Need maintainable, testable architecture
**Decision**: Adopt hexagonal architecture
**Consequences**: Clear separation of concerns, easier testing, potential complexity

### ADR-002: Agent Prompts in Domain Layer

**Status**: Accepted
**Date**: 2025-10-06
**Context**: Prompts encode business logic about GDPR compliance
**Decision**: Move agent prompts to domain layer
**Consequences**: Prompts version-controlled with business logic, clearer ownership
**References**: Marta Fernández García's hexagonal architecture for AI agents

### ADR-003: Modular Monolith Deployment

**Status**: Accepted
**Date**: 2025-10-06
**Context**: Balance simplicity with architectural rigor
**Decision**: Deploy as modular monolith, not microservices
**Consequences**: Simpler deployment, easier debugging, possible future extraction

### ADR-004: Multiple Orchestration Strategies

**Status**: Accepted
**Date**: 2025-10-06
**Context**: Need flexibility for future complex agent interactions
**Decision**: Support pluggable orchestration strategies
**Consequences**: More initial complexity, future flexibility, configuration-driven

---

## Appendix C: Glossary

**Agent**: An autonomous component that performs a specific task using LLM capabilities

**Adapter**: Implementation of a port that connects to external systems

**Domain**: The business logic layer, independent of technical infrastructure

**Hexagonal Architecture**: Architectural pattern isolating business logic from external dependencies

**Modular Monolith**: Single deployable unit with clear internal module boundaries

**Orchestrator**: Component coordinating execution of multiple agents

**Port**: Interface defining contract between domain and infrastructure

**Prompt**: Text instruction to LLM defining expected behavior (domain asset)

---

**Document Version**: 2.0
**Last Updated**: 2025-10-06
**Status**: Active
**Related Documents**: Functional Requirements v1.0, Requirement Numbering System v1.0

---

**END OF ARCHITECTURAL REQUIREMENTS**