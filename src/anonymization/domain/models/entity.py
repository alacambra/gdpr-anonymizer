"""Entity value object for personal data detection."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EntityType(str, Enum):
    """Supported entity types for personal data detection."""
    NAME = "NAME"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    ADDRESS = "ADDRESS"
    OTHER = "OTHER"


class Entity(BaseModel):
    """Represents a detected personal data entity.

    This is an immutable value object representing a piece of
    personally identifiable information detected in text.

    Attributes:
        type: The category of personal data (NAME, EMAIL, etc.)
        value: The actual text value of the entity
        confidence: Optional confidence score (0.0-1.0) from detection

    Example:
        >>> entity = Entity(type=EntityType.NAME, value="John Smith")
        >>> entity.value
        'John Smith'
    """

    type: EntityType = Field(description="Type of personal data entity")
    value: str = Field(min_length=1, description="Actual value of the entity")
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score of detection (0.0-1.0)"
    )

    @field_validator('value')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Ensure value is stripped of leading/trailing whitespace."""
        return v.strip()

    class Config:
        frozen = True  # Immutable value object
