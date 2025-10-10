"""Main orchestrator for the anonymization workflow."""

from dataclasses import dataclass
from typing import Optional

from ..domain.models import (
    Document,
    AnonymizationMapping,
    ValidationResult,
    RiskAssessment
)
from ..domain.ports import IAgent1, IAgent2, IAgent3


@dataclass
class AnonymizationResult:
    """Complete result of the anonymization workflow.

    Attributes:
        document: Original document
        anonymization: Final anonymization mapping
        validation: Validation result from Agent 2
        risk_assessment: Risk assessment from Agent 3
        iterations: Number of iterations required
        success: Whether anonymization succeeded
    """
    document: Document
    anonymization: AnonymizationMapping
    validation: ValidationResult
    risk_assessment: RiskAssessment
    iterations: int
    success: bool


class AnonymizationOrchestrator:
    """Orchestrates the complete anonymization workflow.

    Coordinates Agent 1 (anonymization), Agent 2 (validation), and
    Agent 3 (risk assessment) with retry logic.
    """

    def __init__(
        self,
        agent1: IAgent1,
        agent2: IAgent2,
        agent3: IAgent3,
        max_iterations: int = 3
    ) -> None:
        """Initialize the orchestrator with agents.

        Args:
            agent1: Agent 1 (ANON-EXEC) implementation
            agent2: Agent 2 (DIRECT-CHECK) implementation
            agent3: Agent 3 (RISK-ASSESS) implementation
            max_iterations: Maximum retry iterations for validation failures
        """
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent3 = agent3
        self.max_iterations = max_iterations

    async def anonymize_document(
        self,
        document: Document
    ) -> AnonymizationResult:
        """Execute the complete anonymization workflow.

        Workflow:
        1. Agent 1: Anonymize text
        2. Agent 2: Validate anonymization
        3. If validation fails, retry Agent 1 (up to max_iterations)
        4. Agent 3: Assess risk

        Args:
            document: Document to anonymize

        Returns:
            AnonymizationResult with all agent outputs

        Raises:
            ValueError: If document is invalid
            RuntimeError: If max iterations exceeded
        """
        if document.is_empty():
            raise ValueError("Cannot anonymize empty document")

        anonymization: Optional[AnonymizationMapping] = None
        validation: Optional[ValidationResult] = None
        iteration = 0

        # Retry loop: Agent 1 -> Agent 2
        for iteration in range(1, self.max_iterations + 1):
            # Agent 1: Anonymize
            anonymization = await self.agent1.anonymize(document.content)

            # Agent 2: Validate
            validation = await self.agent2.validate(anonymization.anonymized_text)

            # If validation passed, break out of retry loop
            if validation.passed:
                break

        # At this point, validation must have passed or we exhausted iterations
        if anonymization is None or validation is None:
            raise RuntimeError("Unexpected state: anonymization or validation is None")

        # Agent 3: Risk Assessment
        risk_assessment = await self.agent3.assess_risk(
            anonymization.anonymized_text,
            anonymization.mappings
        )

        return AnonymizationResult(
            document=document,
            anonymization=anonymization,
            validation=validation,
            risk_assessment=risk_assessment,
            iterations=iteration,
            success=validation.passed
        )
