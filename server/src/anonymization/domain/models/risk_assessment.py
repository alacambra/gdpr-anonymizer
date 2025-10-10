"""Risk assessment result from Agent 3."""

from datetime import datetime
from pydantic import BaseModel, Field


class RiskAssessment(BaseModel):
    """Result of risk assessment by Agent 3 (RISK-ASSESS).

    Evaluates re-identification risk for GDPR compliance.

    Attributes:
        overall_score: Risk score from 5-25 (sum of 5 dimensions, 1-5 each)
        risk_level: Risk category (CRITICAL, HIGH, MEDIUM, LOW, NEGLIGIBLE)
        gdpr_compliant: True if safe to publish (LOW or NEGLIGIBLE risk)
        confidence: Assessment confidence level (0.0-1.0)
        reasoning: Human-readable explanation of the assessment
        assessment_date: UTC timestamp of when assessment was completed

    Example:
        >>> from datetime import datetime, UTC
        >>> assessment = RiskAssessment(
        ...     overall_score=5,
        ...     risk_level="NEGLIGIBLE",
        ...     gdpr_compliant=True,
        ...     confidence=1.0,
        ...     reasoning="Stub implementation",
        ...     assessment_date=datetime.now(UTC)
        ... )
    """

    overall_score: int = Field(
        ge=5,
        le=25,
        description="Overall risk score (5-25)"
    )
    risk_level: str = Field(
        description="Risk category (CRITICAL|HIGH|MEDIUM|LOW|NEGLIGIBLE)"
    )
    gdpr_compliant: bool = Field(
        description="True if safe to publish under GDPR"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in assessment (0.0-1.0)"
    )
    reasoning: str = Field(description="Explanation of risk assessment")
    assessment_date: datetime = Field(description="UTC timestamp of assessment")

    def is_safe_to_publish(self) -> bool:
        """Check if document is safe to publish."""
        return self.gdpr_compliant

    class Config:
        frozen = True
