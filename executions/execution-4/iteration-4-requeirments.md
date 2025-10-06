# Iteration 3 Requirements - Hexagonal Architecture Migration

## Document Control

**Version**: 1.1
**Date**: 2025-10-06
**Status**: Ready for Planning
**Iteration Goal**: Migrate from POC to production-ready hexagonal architecture with modular monolith structure (STRUCTURE ONLY - maintain existing functionality)
**Estimated Effort**: 2-3 weeks
**Related Documents**:
- Functional Requirements v2.0
- Architectural Requirements v2.0
- Iteration 1 Implementation (Complete)
- Iteration 2 Implementation (Complete)

---

## 🔑 KEY PRINCIPLE: STRUCTURE ONLY, NO FUNCTIONALITY CHANGES

**This iteration is EXCLUSIVELY about architectural migration. Zero functional changes to agents.**

| Component | Current (Iteration 2) | Target (Iteration 3) | Changes |
|-----------|----------------------|---------------------|---------|
| Agent 1 | `simple.py` - entity identification | `infrastructure/agents/agent1_anon_exec.py` | **Structure only** - same logic |
| Agent 2 | `validation.py` - validation | `infrastructure/agents/agent2_direct_check.py` | **Structure only** - same logic |
| Agent 3 | `risk.py` - stub (returns NEGLIGIBLE) | `infrastructure/agents/agent3_risk_assess.py` | **Structure only** - KEEP STUB |
| LLM | `llm.py` - direct LLM calls | `infrastructure/adapters/llm/*_adapter.py` | **Structure only** - same providers |

**What changes**: Directory structure, layer separation, dependency injection, FastAPI interface
**What doesn't change**: Agent behavior, prompts, LLM responses, output quality

---

## 1. Iteration Overview

### 1.1 Purpose

Transform the Iteration 1-2 implementation into a production-ready modular monolith with:
- Hexagonal architecture (Domain, Application, Infrastructure, Interface layers)
- **MAINTAIN EXACT CURRENT FUNCTIONALITY** - Agent 1, Agent 2, Agent 3 (stub)
- FastAPI REST interface
- Async/await throughout
- Comprehensive configuration system
- Production-grade error handling and logging

**CRITICAL**: This is a **STRUCTURE-ONLY migration**. Agent functionality remains unchanged:

- Agent 1: Entity identification and replacement (as-is from simple.py)
- Agent 2: Validation of anonymization (as-is from validation.py)
- Agent 3: Risk assessment STUB (as-is from risk.py - returns NEGLIGIBLE)

### 1.2 Success Criteria

**ARCHITECT PERSPECTIVE:**
- ✅ Hexagonal architecture fully implemented
- ✅ Clear separation of concerns across 4 layers
- ✅ Domain layer has zero external dependencies
- ✅ All agents working in coordinated workflow
- ✅ FastAPI endpoints operational
- ✅ Agent prompts in domain layer
- ✅ Infrastructure adapters swappable

**USER PERSPECTIVE:**
- ✅ Can call REST API to anonymize documents
- ✅ Receives validation results from Agent 2
- ✅ Sees GDPR compliance risk assessment from Agent 3
- ✅ Configuration via YAML file
- ✅ Clear error messages and logging

**DEVELOPER PERSPECTIVE:**
- ✅ Can add new LLM providers easily
- ✅ Can test layers independently
- ✅ Clear module boundaries
- ✅ Type hints and documentation complete

### 1.3 Explicit Non-Goals

This iteration deliberately EXCLUDES:

- ❌ **ANY new agent functionality** - Agents 1, 2, 3 work exactly as current implementation
- ❌ Agent 3 real risk assessment (keep stub that returns NEGLIGIBLE)
- ❌ Advanced chunking strategies
- ❌ Indirect identifier processing
- ❌ Web UI (API only)
- ❌ Database persistence
- ❌ Authentication/authorization
- ❌ Rate limiting
- ❌ Comprehensive testing (basic tests only)

### 1.4 Migration Strategy

**Strangler Fig Pattern:**
1. Create new hexagonal structure alongside POC
2. Migrate POC code into appropriate layers
3. Keep POC functional until migration complete
4. Deprecate POC in final step

---

## 2. Functional Requirements - iteration 4

### 2.1 Multi-Agent Workflow

**REQ-I3-F-001**: Complete Agent 1 (ANON-EXEC)  
**Source**: REQ-F-010, REQ-F-012  
**Status**: EXTENSION OF ITERATION 1

**Requirements:**
- Extend Iteration 1 implementation to support full Agent 1 specification
- Add entity registry with metadata
- Add processing statistics
- Maintain backward compatibility with Iteration 1 output format

**Success Criteria:**
- All 4 entity types detected (NAME, EMAIL, PHONE, ADDRESS)
- Entity registry includes confidence scores
- Processing stats available

**REQ-I3-F-002**: Implement Agent 2 (DIRECT-CHECK)  
**Source**: REQ-F-014, REQ-F-015, REQ-F-016  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- Verify complete removal of direct identifiers
- Binary result: PASS or FAIL
- List specific remaining identifiers if FAIL
- Support up to 3 retry iterations with Agent 1

**Success Criteria:**
- >90% recall on test corpus
- >85% precision on test corpus
- Clear issue reporting with locations

**REQ-I3-F-003**: Migrate Agent 3 (RISK-ASSESS) - STUB ONLY
**Source**: risk.py (existing stub implementation)
**Status**: MIGRATION ONLY - NO NEW FUNCTIONALITY

**Requirements:**

- Migrate existing stub from risk.py to hexagonal architecture
- Continue returning hardcoded NEGLIGIBLE risk assessment
- Maintain same RiskAssessment dataclass structure
- Keep stub reasoning message
- No LLM calls required (stub implementation)

**Success Criteria:**

- Agent 3 returns same stub results as current implementation
- Fits into hexagonal architecture properly
- Can be enhanced in future iterations without architectural changes

**REQ-I3-F-004**: Orchestration Workflow  
**Source**: REQ-F-021, REQ-F-024  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- Sequential execution: Agent 1 → Agent 2 → Agent 3
- Retry loop: If Agent 2 fails, return to Agent 1 (max 3 iterations)
- Aggregate results from all agents
- Return comprehensive AnonymizationResult

**Success Criteria:**
- Workflow completes successfully for valid inputs
- Retry logic functions correctly
- Failure after max iterations returns clear error

### 2.2 REST API Interface

**REQ-I3-F-005**: FastAPI Application  
**Source**: REQ-A-040, REQ-A-041  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- POST /api/v1/anonymize - single document
- POST /api/v1/anonymize/batch - multiple documents  
- GET /api/v1/config - current configuration
- GET /health - health check
- OpenAPI documentation auto-generated

**Success Criteria:**
- All endpoints functional
- Request/response validation via Pydantic
- OpenAPI spec accessible at /docs

**REQ-I3-F-006**: API Error Handling  
**Source**: REQ-F-023  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- HTTP status codes: 200 (success), 400 (invalid), 500 (error)
- Structured error responses with detail messages
- Request ID for traceability
- Validation errors with field-level detail

**Success Criteria:**
- Clear error messages for all failure scenarios
- No stack traces exposed in production mode

### 2.3 Configuration System

**REQ-I3-F-007**: YAML Configuration  
**Source**: REQ-F-037, REQ-F-038  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- config.yaml with sections: llm, agents, orchestration, logging
- Environment variable substitution (${ANTHROPIC_API_KEY})
- Schema validation via Pydantic
- Config file validation command

**Success Criteria:**
- All configuration options documented
- Invalid config rejected with clear errors
- Environment variables properly substituted

---

## 3. Architectural Requirements - iteration 4

### 3.1 Domain Layer

**REQ-I3-A-001**: Domain Models  
**Source**: REQ-A-007, REQ-A-008  
**Status**: NEW IMPLEMENTATION

**Required Models:**
```
domain/models/
├── document.py          # Document entity
├── entity.py            # Entity value object
├── anonymization_mapping.py
├── validation_result.py # Agent 2 output
└── risk_assessment.py   # Agent 3 output
```

**Requirements:**
- All models immutable (frozen dataclass or Pydantic)
- Self-validating (enforce invariants)
- Rich behavior (not anemic)
- Zero external dependencies

**Success Criteria:**
- Models can be instantiated independently
- Validation rules enforce business rules
- No imports from infrastructure/application

**REQ-I3-A-002**: Domain Ports  
**Source**: REQ-A-009, REQ-A-010  
**Status**: NEW IMPLEMENTATION

**Required Interfaces:**
```
domain/ports/
├── agent_interfaces.py     # IAgent1, IAgent2, IAgent3
├── llm_provider_interface.py  # ILLMProvider, ILLMSession
└── storage_interface.py    # IDocumentStorage (future)
```

**Requirements:**
- Use Python Protocols (PEP 544)
- Fully typed method signatures
- Comprehensive docstrings

**Success Criteria:**
- Infrastructure can implement without importing domain internals
- Type checking passes (mypy strict mode)

**REQ-I3-A-003**: Agent Prompts in Domain  
**Source**: REQ-A-011B, REQ-A-074  
**Status**: NEW IMPLEMENTATION

**Required Structure:**
```
domain/agents/
├── agent_definitions.py    # Agent roles and contracts
└── prompts/
    ├── agent1_prompts.py   # Anonymization prompts
    ├── agent2_prompts.py   # Verification prompts
    └── agent3_prompts.py   # Risk assessment prompts
```

**Requirements:**
- Prompts as Python strings (multi-line)
- Template variables clearly marked (e.g., {text}, {entities})
- Version each prompt (v1, v2 if prompt engineering evolves)
- Include examples in prompts

**Success Criteria:**
- Prompts readable and maintainable
- No LLM provider-specific code in prompts
- Prompt changes don't require infrastructure changes

### 3.2 Application Layer

**REQ-I3-A-004**: Orchestrator  
**Source**: REQ-A-018, REQ-A-019, REQ-A-020  
**Status**: NEW IMPLEMENTATION

**Required Structure:**
```
application/
├── orchestrator.py             # Main orchestrator
├── orchestration/
│   └── sequential_orchestrator.py
└── config.py                   # Configuration models
```

**Requirements:**
- AnonymizationOrchestrator class
- Dependency injection (agents injected via constructor)
- Async method: `async def anonymize_document(document) -> AnonymizationResult`
- Retry logic for Agent 2 failures
- Configurable max iterations

**Success Criteria:**
- Orchestrator coordinates agents without direct LLM calls
- Agents are swappable via DI
- Configuration drives behavior

**REQ-I3-A-005**: Use Cases  
**Source**: REQ-A-021, REQ-A-022  
**Status**: OPTIONAL FOR iteration 4

**Structure:**
```
application/use_cases/
├── anonymize_document.py
└── batch_anonymize.py  # Optional
```

**Requirements:**
- Thin wrappers around orchestrator
- DTO conversions (if needed)

**Success Criteria:**
- Use cases callable from interface layer
- No business logic in use cases (delegate to orchestrator/domain)

### 3.3 Infrastructure Layer

**REQ-I3-A-006**: LLM Adapters  
**Source**: REQ-A-027, REQ-A-028, REQ-A-029, REQ-A-030  
**Status**: MIGRATION + ENHANCEMENT

**Structure:**
```
infrastructure/adapters/llm/
├── base.py                 # BaseLLMAdapter
├── ollama_adapter.py
├── claude_adapter.py
├── openai_adapter.py
└── factory.py              # LLMAdapterFactory
```

**Requirements:**
- Migrate Iteration 1 LLM clients to adapters
- All adapters implement ILLMProvider
- BaseLLMAdapter with common functionality
- Factory pattern for provider selection
- Async methods throughout

**Success Criteria:**
- Adapters interchangeable via configuration
- No business logic in adapters
- Provider-specific code isolated

**REQ-I3-A-007**: Agent Implementations  
**Source**: REQ-A-031, REQ-A-032, REQ-A-033  
**Status**: NEW IMPLEMENTATION

**Structure:**
```
infrastructure/agents/
├── agent1_anon_exec.py
├── agent2_direct_check.py
└── agent3_risk_assess.py
```

**Requirements:**
- Each implements respective domain interface
- Load prompts from domain layer
- Use injected ILLMProvider
- Parse LLM responses to domain models
- Handle malformed responses gracefully

**Success Criteria:**
- Agents testable with mocked LLM provider
- Prompt changes don't require agent code changes
- LLM provider swappable without agent changes

**REQ-I3-A-008**: Configuration Loader  
**Source**: REQ-A-036, REQ-A-037  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- Load config.yaml
- Pydantic models for validation
- Environment variable substitution
- Type-safe access to configuration

**Success Criteria:**
- Invalid YAML rejected with clear error
- Missing environment variables reported
- Configuration accessible throughout application

### 3.4 Interface Layer

**REQ-I3-A-009**: FastAPI Structure  
**Source**: REQ-A-040  
**Status**: NEW IMPLEMENTATION

**Structure:**
```
interfaces/rest/
├── main.py                 # FastAPI app
├── dependencies.py         # DI container
├── routers/
│   ├── anonymization.py
│   └── health.py
├── schemas/
│   ├── requests.py         # Pydantic models
│   └── responses.py
└── middleware/
    ├── logging.py
    └── error_handling.py
```

**Requirements:**
- FastAPI application with CORS
- Request/response schemas with Pydantic
- Dependency injection via FastAPI Depends()
- Global error handler
- Request logging middleware

**Success Criteria:**
- API starts without errors
- /docs endpoint shows OpenAPI spec
- All endpoints functional

**REQ-I3-A-010**: Dependency Injection  
**Source**: REQ-A-044, REQ-A-045  
**Status**: NEW IMPLEMENTATION

**Requirements:**
- Singletons: Config, LLM provider
- Per-request: Orchestrator, agents
- Composition root in dependencies.py
- Clear dependency chain

**Success Criteria:**
- Dependencies injected automatically
- No global state except singletons
- Easy to mock for testing

---

## 4. Migration Tasks

### 4.1 Phase 1: Domain Layer (Days 1-3)

**Tasks:**
1. Create domain/models/ structure
2. Define all domain models (Document, Entity, etc.)
3. Create domain/ports/ with all interfaces
4. Move prompts to domain/agents/prompts/
5. Define agent_definitions.py

**Deliverables:**
- domain/ directory with all models
- domain/ directory with zero external dependencies
- All ports defined

**Validation:**
- Import test: `from domain.models import Document` works
- No imports from infrastructure/application in domain
- mypy passes in strict mode

### 4.2 Phase 2: Infrastructure Adapters (Days 4-6)

**Tasks:**
1. Create infrastructure/adapters/llm/ structure
2. Migrate Iteration 1 LLM clients to adapters
3. Implement BaseLLMAdapter
4. Create LLMAdapterFactory
5. Add async/await support

**Deliverables:**
- All LLM adapters implementing ILLMProvider
- Factory creating adapters from config
- Adapters tested with real LLM providers

**Validation:**
- Adapter swapping via config works
- All adapters return consistent format
- Async calls functional

### 4.3 Phase 3: Agent Implementations (Days 7-10)

**Tasks:**
1. Create infrastructure/agents/ structure
2. **Migrate Agent1Implementation from simple.py** - same entity extraction logic
3. **Migrate Agent2Implementation from validation.py** - same validation logic
4. **Migrate Agent3Implementation from risk.py** - KEEP AS STUB (returns NEGLIGIBLE)
5. Extract prompts to domain/agents/prompts/

**Deliverables:**

- Three agent implementations with **IDENTICAL behavior** to current code
- Each agent returning proper domain models
- Agent 1 and 2 **working exactly as before**
- Agent 3 stub **still returning NEGLIGIBLE**

**Validation:**
- Each agent testable independently
- **Output identical to current implementation**
- Agents coordinate via orchestrator
- Retry loop functions correctly

### 4.4 Phase 4: Application Layer (Days 11-13)

**Tasks:**
1. Create application/ structure
2. Implement AnonymizationOrchestrator
3. Implement sequential workflow
4. Add retry logic
5. Create configuration models

**Deliverables:**
- Working orchestrator
- Configuration system functional
- YAML config loading

**Validation:**
- Full workflow (Agent 1 → 2 → 3) works
- Retry loop triggers correctly
- Configuration drives behavior

### 4.5 Phase 5: FastAPI Interface (Days 14-17)

**Tasks:**
1. Create interfaces/rest/ structure
2. Implement FastAPI application
3. Create routers and schemas
4. Implement dependency injection
5. Add error handling and logging

**Deliverables:**
- Working REST API
- All endpoints functional
- OpenAPI documentation

**Validation:**
- API starts successfully
- POST /api/v1/anonymize works
- Health check returns 200
- Error responses formatted correctly

### 4.6 Phase 6: Integration & Testing (Days 18-21)

**Tasks:**
1. End-to-end testing
2. Configuration validation
3. Error scenario testing
4. Performance testing
5. Documentation updates

**Deliverables:**
- Tested system
- Updated README
- Configuration examples
- Known limitations documented

**Validation:**
- All acceptance criteria met
- Performance targets achieved
- Documentation complete

---

## 5. Directory Structure

**REQ-I3-A-011**: Final Structure  
**Source**: REQ-A-064  
**Status**: TARGET ARCHITECTURE

```
anonymization-system/
├── pyproject.toml
├── README.md
├── config/
│   ├── config.yaml
│   └── config.yaml.example
├── .env.example
│
├── src/anonymization/
│   ├── __init__.py
│   │
│   ├── domain/                    # DOMAIN LAYER
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   ├── entity.py
│   │   │   ├── anonymization_mapping.py
│   │   │   ├── validation_result.py
│   │   │   └── risk_assessment.py
│   │   ├── services/
│   │   │   ├── gdpr_compliance.py
│   │   │   └── risk_calculator.py
│   │   ├── ports/
│   │   │   ├── agent_interfaces.py
│   │   │   ├── llm_provider_interface.py
│   │   │   └── storage_interface.py
│   │   ├── agents/
│   │   │   ├── agent_definitions.py
│   │   │   └── prompts/
│   │   │       ├── agent1_prompts.py
│   │   │       ├── agent2_prompts.py
│   │   │       └── agent3_prompts.py
│   │   └── exceptions.py
│   │
│   ├── application/               # APPLICATION LAYER
│   │   ├── orchestrator.py
│   │   ├── orchestration/
│   │   │   └── sequential_orchestrator.py
│   │   └── config.py
│   │
│   ├── infrastructure/            # INFRASTRUCTURE LAYER
│   │   ├── adapters/
│   │   │   └── llm/
│   │   │       ├── base.py
│   │   │       ├── ollama_adapter.py
│   │   │       ├── claude_adapter.py
│   │   │       ├── openai_adapter.py
│   │   │       └── factory.py
│   │   ├── agents/
│   │   │   ├── agent1_anon_exec.py
│   │   │   ├── agent2_direct_check.py
│   │   │   └── agent3_risk_assess.py
│   │   └── config_loader.py
│   │
│   └── interfaces/                # INTERFACE LAYER
│       └── rest/
│           ├── main.py
│           ├── dependencies.py
│           ├── routers/
│           │   ├── anonymization.py
│           │   └── health.py
│           ├── schemas/
│           │   ├── requests.py
│           │   └── responses.py
│           └── middleware/
│               ├── logging.py
│               └── error_handling.py
│
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   └── integration/
│
└── docs/
    └── architecture/
```

---

## 6. Configuration

### 6.1 Config File Structure

**REQ-I3-A-012**: YAML Configuration  
**Source**: REQ-A-036  
**Status**: NEW REQUIREMENT

**config/config.yaml**:
```yaml
llm:
  provider: "claude"  # or "openai" or "ollama"
  model: "claude-sonnet-4.5"
  temperature: 0.7
  max_tokens: 4096
  api_key_env: "ANTHROPIC_API_KEY"

agents:
  agent1:
    name: "ANON-EXEC"
    enabled: true
    prompt_version: "v1"
  
  agent2:
    name: "DIRECT-CHECK"
    enabled: true
    strictness: "normal"  # strict | normal | lenient
  
  agent3:
    name: "RISK-ASSESS"
    enabled: true

orchestration:
  max_iterations: 3
  timeout_seconds: 300

logging:
  level: "INFO"
  format: "json"
  output: "logs/anonymization.log"
```

**Success Criteria:**
- All configuration options functional
- Environment variable substitution works
- Invalid config rejected with helpful error

---

## 7. Technology Stack Updates

**REQ-I3-A-013**: Dependencies  
**Source**: REQ-A-065  
**Status**: ADDITIONS TO ITERATION 1

**New Dependencies:**
- FastAPI ≥0.100
- uvicorn ≥0.27 (ASGI server)
- Pydantic ≥2.0
- PyYAML ≥6.0
- python-dotenv ≥1.0
- httpx ≥0.27 (async HTTP client)
- Loguru ≥0.7 (structured logging)

**Development Dependencies:**
- pytest ≥8.0
- pytest-asyncio ≥0.23
- pytest-cov ≥4.1
- mypy ≥1.8
- ruff ≥0.1

**Success Criteria:**
- All dependencies installable via Poetry
- No conflicts with existing dependencies
- Lock file updated

---

## 8. Acceptance Criteria

### 8.1 Functional Acceptance

**The iteration is considered functionally complete when:**

1. ✅ Full multi-agent workflow operational (Agent 1 → 2 → 3)
2. ✅ Agent 2 verification identifies remaining identifiers
3. ✅ Agent 3 provides risk assessment with 5 dimensions
4. ✅ Retry loop works (Agent 2 fail → retry Agent 1)
5. ✅ FastAPI endpoints all functional
6. ✅ Configuration via YAML works
7. ✅ Health check endpoint returns system status
8. ✅ OpenAPI documentation accessible
9. ✅ Error handling provides clear messages
10. ✅ Logging captures all operations

### 8.2 Architectural Acceptance

**Hexagonal architecture is validated when:**

1. ✅ Domain layer has zero external dependencies
2. ✅ All dependencies point inward
3. ✅ Adapters implement domain ports
4. ✅ Agent prompts in domain layer
5. ✅ LLM provider swappable via config
6. ✅ Infrastructure can be changed without domain changes
7. ✅ Application orchestrator independent of infrastructure
8. ✅ Four layers clearly separated

### 8.3 Quality Gates

1. ✅ Type checking passes (mypy strict mode)
2. ✅ Basic tests pass (unit tests for domain models)
3. ✅ API responds within performance targets (<5s for small docs)
4. ✅ Configuration validation catches invalid configs
5. ✅ Error messages are user-friendly
6. ✅ Logging doesn't expose sensitive data
7. ✅ Documentation updated (README, architecture diagrams)

---

## 9. Testing Strategy

### 9.1 Unit Tests (Basic)

**Scope:**
- Domain models (validation, behavior)
- Agent implementations (with mocked LLM)
- Configuration validation

**Target:** >70% coverage (basic safety net)

### 9.2 Integration Tests

**Scope:**
- Orchestrator with real agents
- API endpoints with mocked orchestrator
- Configuration loading

**Target:** All happy paths covered

### 9.3 End-to-End Tests

**Scope:**
- Full workflow with real LLM provider
- API call → complete anonymization → response
- Error scenarios (invalid input, LLM failure)

**Target:** 3-5 critical paths tested

---

## 10. Performance Targets

**REQ-I3-NF-001**: Performance  
**Source**: REQ-F-045  
**Status**: TARGETS FOR iteration 4

**Targets:**
- Small documents (<100 words): <10 seconds (3 agents sequentially)
- Medium documents (100-500 words): <30 seconds
- API response time: <15 seconds (P95)
- Health check: <100ms

**Note:** Performance optimization deferred to future iterations. Focus is correctness and architecture.

---

## 11. Documentation Requirements

**REQ-I3-DOC-001**: Documentation Updates  
**Status**: REQUIRED FOR COMPLETION

**Required Documentation:**
1. **README.md**: Updated for iteration 4
   - Architecture overview
   - Configuration guide
   - API usage examples
   - Deployment instructions

2. **Architecture Diagrams**:
   - Hexagonal architecture diagram
   - Component interaction diagram
   - Data flow diagram

3. **API Documentation**:
   - Automatically generated via FastAPI OpenAPI
   - Example requests/responses
   - Error codes reference

4. **Configuration Reference**:
   - All config options documented
   - Examples for common scenarios
   - Troubleshooting guide

---

## 12. Migration from Iteration 1

### 12.1 Backward Compatibility

**REQ-I3-COMPAT-001**: POC Compatibility  
**Status**: TEMPORARY REQUIREMENT

**Requirements:**
- Iteration 1 `anonymize_simple()` continues working during migration
- Can be called for comparison testing
- Marked as deprecated with migration guide

**Success Criteria:**
- POC function coexists with new architecture
- Clear deprecation warnings
- Migration path documented

### 12.2 Deprecation Process

**Phase 1** (During iteration 4): Mark POC as deprecated  
**Phase 2** (Iteration 4): Remove POC code  

---

## 13. Risks and Mitigation

### 13.1 Technical Risks

**Risk 1: Complexity Increase**
- **Impact**: HIGH - Team might struggle with hexagonal architecture
- **Mitigation**: Clear documentation, code reviews, pair programming
- **Contingency**: Simplify layers if team feedback indicates issues

**Risk 2: Performance Degradation**
- **Impact**: MEDIUM - More layers might slow execution
- **Mitigation**: Async/await, profiling, optimization where needed
- **Contingency**: Accept slightly slower performance for architectural benefits

**Risk 3: Async/Await Migration Complexity**

- **Impact**: MEDIUM - Converting existing sync code to async
- **Mitigation**: Incremental migration, test thoroughly, use async LLM clients
- **Contingency**: Start with sync code, migrate to async in future iteration

### 13.2 Schedule Risks

**Risk 4: Scope Creep**

- **Impact**: HIGH - Could delay completion
- **Mitigation**: Strict adherence to non-goals, STRUCTURE-ONLY migration
- **Contingency**: Defer FastAPI to future iteration, focus on domain/infrastructure first

**Risk 5: Integration Issues**

- **Impact**: MEDIUM - Layers might not integrate smoothly
- **Mitigation**: Incremental integration, continuous testing
- **Contingency**: Extra integration phase if needed (Days 22-24)

---

## 14. Definition of Done

### 14.1 Code Complete
- [ ] All domain models implemented
- [ ] All ports defined
- [ ] All adapters functional
- [ ] All three agents working
- [ ] Orchestrator coordinating agents
- [ ] FastAPI application running
- [ ] Configuration system functional

### 14.2 Documentation Complete
- [ ] README updated
- [ ] Architecture diagrams created
- [ ] API documentation generated
- [ ] Configuration reference written
- [ ] Migration guide from Iteration 1

### 14.3 Testing Complete
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] End-to-end tests passing
- [ ] Performance targets met
- [ ] Error scenarios handled

### 14.4 Validation Complete
- [ ] All functional acceptance criteria met
- [ ] All architectural acceptance criteria met
- [ ] All quality gates passed
- [ ] Technical review completed
- [ ] Stakeholder demo successful

---

## 15. Success Metrics

**Quantitative:**
- Domain layer imports: 0 external dependencies
- Test coverage: >70%
- API response time: <15s (P95)
- Type coverage: 100% (mypy strict)

**Qualitative:**
- Code reviewers understand architecture
- Developers can add new features easily
- Clear separation of concerns evident
- Production-ready feel

---

## 16. Next Iteration Preview

**Iteration 4 will add:**
- Comprehensive testing suite (>85% coverage)
- AutoGen orchestration (optional)
- CLI interface
- Batch processing
- File I/O operations
- Advanced error handling
- Production logging and monitoring

---

**END OF iteration 4 REQUIREMENTS**

**Status**: READY FOR IMPLEMENTATION  
**Estimated Effort**: 2-3 weeks  
**Team Size**: 1-2 developers + architect reviews  
**Dependencies**: Iteration 1 complete (✅), Iteration 2 specified (✅)