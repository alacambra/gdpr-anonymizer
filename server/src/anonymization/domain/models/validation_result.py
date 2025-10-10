"""Validation result from Agent 2."""

from typing import List
from pydantic import BaseModel, Field


class ValidationIssue(BaseModel):
    """Represents a remaining identifier found during validation.

    Attributes:
        identifier_type: Type of identifier (NAME, EMAIL, etc.)
        value: The actual identifier text found
        context: Surrounding text (±20 characters)
        location_hint: Human-readable location description
    """

    identifier_type: str = Field(description="Type of identifier found")
    value: str = Field(description="Actual identifier text")
    context: str = Field(description="Surrounding text context")
    location_hint: str = Field(description="Location in document")

    class Config:
        frozen = True


class ValidationResult(BaseModel):
    """Result of validation by Agent 2 (DIRECT-CHECK).

    Attributes:
        passed: True if no remaining identifiers were found
        issues: List of remaining identifiers (empty if passed)
        reasoning: Human-readable explanation of findings
        confidence: Agent's confidence in the analysis (0.0-1.0)

    Example:
        >>> result = ValidationResult(
        ...     passed=True,
        ...     issues=[],
        ...     reasoning="No identifiers found",
        ...     confidence=0.95
        ... )
    """

    passed: bool = Field(description="True if validation passed")
    issues: List[ValidationIssue] = Field(
        default_factory=list,
        description="List of validation issues found"
    )
    reasoning: str = Field(description="Explanation of findings")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in validation (0.0-1.0)"
    )

    def issue_count(self) -> int:
        """Get number of issues found."""
        return len(self.issues)

    class Config:
        frozen = True
