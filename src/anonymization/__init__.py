"""
GDPR Text Anonymization System - Iteration 1
Minimal proof-of-concept for text anonymization using LLMs.
"""

from dataclasses import dataclass
from typing import Dict

__version__ = "0.1.0"


@dataclass
class AnonymizationResult:
    """Result of text anonymization operation.

    Attributes:
        anonymized_text: Text with personal data replaced by placeholders
        mappings: Dictionary mapping original values to placeholders
        original_text: Copy of the original input text
    """
    anonymized_text: str
    mappings: Dict[str, str]
    original_text: str


from .models import Entity, EntityList, EntityType
from .simple import anonymize_simple

__all__ = ["anonymize_simple", "AnonymizationResult", "Entity", "EntityList", "EntityType"]
