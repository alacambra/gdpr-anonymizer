"""
GDPR Text Anonymization System - Iteration 1
Minimal proof-of-concept for text anonymization using LLMs.
"""

__version__ = "0.1.0"

from .models import Entity, EntityList, EntityType
from .simple import AnonymizationResult, anonymize_simple

__all__ = ["anonymize_simple", "AnonymizationResult", "Entity", "EntityList", "EntityType"]
