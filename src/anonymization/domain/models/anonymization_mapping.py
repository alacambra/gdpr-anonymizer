"""Anonymization mapping for tracking replacements."""

from typing import Dict, List
from pydantic import BaseModel, Field
from .entity import Entity


class AnonymizationMapping(BaseModel):
    """Tracks the mapping between original values and placeholders.

    This value object represents the complete set of anonymization
    replacements performed on a document.

    Attributes:
        original_text: The unmodified input text
        anonymized_text: Text with all entities replaced by placeholders
        mappings: Dictionary mapping original values to placeholders
        entities: List of detected entities

    Example:
        >>> mapping = AnonymizationMapping(
        ...     original_text="Contact John",
        ...     anonymized_text="Contact [NAME_1]",
        ...     mappings={"John": "[NAME_1]"},
        ...     entities=[]
        ... )
    """

    original_text: str = Field(description="Original unmodified text")
    anonymized_text: str = Field(description="Text with replacements applied")
    mappings: Dict[str, str] = Field(
        default_factory=dict,
        description="Map from original values to placeholders"
    )
    entities: List[Entity] = Field(
        default_factory=list,
        description="List of detected entities"
    )

    def entity_count(self) -> int:
        """Get total number of entities detected."""
        return len(self.entities)

    def replacement_count(self) -> int:
        """Get number of unique replacements made."""
        return len(self.mappings)

    class Config:
        frozen = True  # Immutable value object
