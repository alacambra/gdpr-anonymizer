"""API response schemas."""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ValidationIssueResponse(BaseModel):
    """Validation issue in the response."""
    identifier_type: str
    value: str
    context: str
    location_hint: str


class ValidationResponse(BaseModel):
    """Validation result in the response."""
    passed: bool
    issues: List[ValidationIssueResponse]
    reasoning: str
    confidence: float


class RiskAssessmentResponse(BaseModel):
    """Risk assessment in the response."""
    overall_score: int
    risk_level: str
    gdpr_compliant: bool
    confidence: float
    reasoning: str
    assessment_date: datetime


class AnonymizeResponse(BaseModel):
    """Response from anonymizing a single document.

    Example:
        {
            "document_id": "doc-123",
            "anonymized_text": "Contact [NAME_1] at [EMAIL_1]",
            "mappings": {"John Smith": "[NAME_1]", "john@email.com": "[EMAIL_1]"},
            "validation": {...},
            "risk_assessment": {...},
            "iterations": 1,
            "success": true,
            "llm_provider": "claude",
            "llm_model": "claude-3-5-sonnet-20241022",
            "error": null
        }
    """

    document_id: Optional[str] = Field(
        default=None,
        description="Document identifier if provided"
    )
    anonymized_text: str = Field(description="Anonymized text (empty if no entities found)")
    mappings: Dict[str, str] = Field(description="Mapping of original to placeholder")
    validation: ValidationResponse = Field(description="Validation result")
    risk_assessment: RiskAssessmentResponse = Field(description="Risk assessment")
    iterations: int = Field(description="Number of iterations required")
    success: bool = Field(description="Whether anonymization succeeded")
    llm_provider: str = Field(description="LLM provider used (ollama, claude, openai)")
    llm_model: str = Field(description="Specific LLM model used")
    error: str = Field(
        default="",
        description="Error message if success=false, shown in UI error box"
    )


class BatchAnonymizeResponse(BaseModel):
    """Response from batch anonymization.

    Example:
        {
            "results": [...]
            "total": 2,
            "successful": 2,
            "failed": 0
        }
    """

    results: List[AnonymizeResponse] = Field(description="List of anonymization results")
    total: int = Field(description="Total number of documents processed")
    successful: int = Field(description="Number of successful anonymizations")
    failed: int = Field(description="Number of failed anonymizations")


class HealthResponse(BaseModel):
    """Health check response.

    Example:
        {
            "status": "healthy",
            "version": "0.4.0",
            "llm_provider": "claude"
        }
    """

    status: str = Field(description="Health status (healthy|unhealthy)")
    version: str = Field(description="Application version")
    llm_provider: str = Field(description="Currently configured LLM provider")


class ConfigResponse(BaseModel):
    """Configuration response."""

    llm_provider: str
    llm_model: str
    max_iterations: int
    agents_enabled: Dict[str, bool]


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    request_id: Optional[str] = Field(default=None, description="Request ID for tracing")
