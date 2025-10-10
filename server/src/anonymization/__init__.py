"""
GDPR Text Anonymization System - Iteration 3
Multi-agent anonymization with validation and risk assessment.
"""

__version__ = "0.3.0"

from .models import Entity, EntityList, EntityType
from .simple import AnonymizationResult, anonymize_simple
from .validation import Issue, ValidationResult, validate_anonymization
from .risk import RiskAssessment, RiskAssessmentError, assess_risk

__all__ = [
    "anonymize_simple",
    "AnonymizationResult",
    "Entity",
    "EntityList",
    "EntityType",
    "validate_anonymization",
    "ValidationResult",
    "Issue",
    "assess_risk",
    "RiskAssessment",
    "RiskAssessmentError",
]
