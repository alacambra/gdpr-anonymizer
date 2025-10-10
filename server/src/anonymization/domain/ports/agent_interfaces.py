"""Agent interfaces - Ports for the three anonymization agents."""

from typing import Protocol, Dict
from ..models import AnonymizationMapping, ValidationResult, RiskAssessment


class IAgent1(Protocol):
    """Interface for Agent 1 (ANON-EXEC) - Entity Anonymization.

    Agent 1 is responsible for identifying and replacing personal data
    entities with placeholders.
    """

    async def anonymize(self, text: str) -> AnonymizationMapping:
        """Identify and replace personal data entities in text.

        Args:
            text: Original text to anonymize

        Returns:
            AnonymizationMapping with replacements and entity list

        Raises:
            Exception: If anonymization fails
        """
        ...


class IAgent2(Protocol):
    """Interface for Agent 2 (DIRECT-CHECK) - Validation.

    Agent 2 verifies that anonymized text contains no remaining
    direct identifiers.
    """

    async def validate(self, anonymized_text: str) -> ValidationResult:
        """Validate anonymized text for remaining identifiers.

        Args:
            anonymized_text: Text after Agent 1 processing

        Returns:
            ValidationResult with pass/fail status and issues

        Raises:
            Exception: If validation fails
        """
        ...


class IAgent3(Protocol):
    """Interface for Agent 3 (RISK-ASSESS) - Risk Assessment.

    Agent 3 evaluates re-identification risk for GDPR compliance.
    """

    async def assess_risk(
        self,
        anonymized_text: str,
        mappings: Dict[str, str]
    ) -> RiskAssessment:
        """Assess re-identification risk of anonymized text.

        Args:
            anonymized_text: Text after Agent 1 + Agent 2 processing
            mappings: Dictionary of original values to placeholders

        Returns:
            RiskAssessment with risk score and compliance status

        Raises:
            Exception: If risk assessment fails
        """
        ...
