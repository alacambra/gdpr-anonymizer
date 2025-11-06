#!/usr/bin/env python3
"""Quick test script for Iteration 4 hexagonal architecture."""

import asyncio
from pathlib import Path

import pytest

from anonymization.application.config import AppConfig, LLMConfig, AgentConfig, OrchestrationConfig
from anonymization.application.orchestrator import AnonymizationOrchestrator
from anonymization.domain.models import Document
from anonymization.infrastructure.adapters.llm import create_llm_provider
from anonymization.infrastructure.agents import (
    Agent1Implementation,
    Agent2Implementation,
    Agent3Implementation
)



@pytest.mark.skip(reason="Integration test - requires running Ollama instance")
@pytest.mark.asyncio
async def test_basic_anonymization():
    """Test basic anonymization workflow."""
    print("=" * 80)
    print("GDPR Anonymizer - Iteration 4 Test")
    print("=" * 80)
    print()

    # Create simple config
    config = AppConfig(
        llm=LLMConfig(
            provider="ollama",
            model="ollama-3-5-sonnet-20241022",
            temperature=0.1,
            max_tokens=4096
        ),
        agent1=AgentConfig(name="ANON-EXEC", enabled=True, prompt_version="v1"),
        agent2=AgentConfig(name="DIRECT-CHECK", enabled=True, prompt_version="v1"),
        agent3=AgentConfig(name="RISK-ASSESS", enabled=True, prompt_version="v1"),
        orchestration=OrchestrationConfig(max_iterations=3, timeout_seconds=300)
    )

    print("Configuration:")
    print(f"  LLM Provider: {config.llm.provider}")
    print(f"  Model: {config.llm.model}")
    print(f"  Max Iterations: {config.orchestration.max_iterations}")
    print()

    # Create LLM provider
    print("Creating LLM provider...")
    llm_provider = create_llm_provider(
        provider=config.llm.provider,
        config={
            "model": config.llm.model,
            "temperature": config.llm.temperature,
            "max_tokens": config.llm.max_tokens
        }
    )
    print("✓ LLM provider created")
    print()

    # Create agents
    print("Creating agents...")
    agent1 = Agent1Implementation(llm_provider)
    agent2 = Agent2Implementation(llm_provider)
    agent3 = Agent3Implementation(llm_provider)
    print("✓ Agent 1 (ANON-EXEC) created")
    print("✓ Agent 2 (DIRECT-CHECK) created")
    print("✓ Agent 3 (RISK-ASSESS) created")
    print()

    # Create orchestrator
    print("Creating orchestrator...")
    orchestrator = AnonymizationOrchestrator(
        agent1=agent1,
        agent2=agent2,
        agent3=agent3,
        max_iterations=config.orchestration.max_iterations
    )
    print("✓ Orchestrator created")
    print()

    # Test document
    test_text = "Please contact John Smith at john.smith@email.com or call him at 555-123-4567."
    print("Test Document:")
    print(f"  Original: {test_text}")
    print()

    # Create document
    document = Document(
        content=test_text,
        document_id="test-doc-001"
    )

    # Run anonymization
    print("Running anonymization workflow...")
    print()
    result = await orchestrator.anonymize_document(document)

    # Display results
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    print(f"Anonymized Text:")
    print(f"  {result.anonymizationMapping.anonymized_text}")
    print()

    print(f"Mappings ({len(result.anonymizationMapping.mappings)} total):")
    for original, placeholder in result.anonymizationMapping.mappings.items():
        print(f"  {original:30s} → {placeholder}")
    print()

    print(f"Validation (Agent 2):")
    print(f"  Passed: {result.validation.passed}")
    print(f"  Confidence: {result.validation.confidence:.2f}")
    print(f"  Issues: {len(result.validation.issues)}")
    if result.validation.issues:
        for issue in result.validation.issues:
            print(f"    - {issue.identifier_type}: {issue.value}")
    print()

    print(f"Risk Assessment (Agent 3):")
    print(f"  Risk Level: {result.risk_assessment.risk_level}")
    print(f"  GDPR Compliant: {result.risk_assessment.gdpr_compliant}")
    print(f"  Overall Score: {result.risk_assessment.overall_score}/25")
    print(f"  Note: {result.risk_assessment.reasoning[:80]}...")
    print()

    print(f"Workflow:")
    print(f"  Iterations: {result.iterations}")
    print(f"  Success: {result.success}")
    print()

    print("=" * 80)
    print("✓ Test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_basic_anonymization())
