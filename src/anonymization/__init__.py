"""
GDPR Text Anonymization System - Iteration 2
Multi-agent anonymization with validation layer.
"""

__version__ = "0.2.0"

from .models import Entity, EntityList, EntityType
from .simple import AnonymizationResult, anonymize_simple
from .validation import Issue, ValidationResult, validate_anonymization

__all__ = [
    "anonymize_simple",
    "AnonymizationResult",
    "Entity",
    "EntityList",
    "EntityType",
    "validate_anonymization",
    "ValidationResult",
    "Issue",
]
