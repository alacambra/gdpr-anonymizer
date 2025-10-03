"""
Data models for anonymization entities using Pydantic.

Provides type-safe serialization/deserialization for entity detection.
"""

from enum import Enum
from typing import Iterator, List

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

    Example:
        >>> entity = Entity(type="NAME", value="John Smith")
        >>> entity.model_dump_json()
        '{"type":"NAME","value":"John Smith"}'
    """
    type: EntityType = Field(description="Type of personal data entity")
    value: str = Field(min_length=1, description="Actual value of the entity")

    @field_validator('value')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Ensure value is stripped of leading/trailing whitespace."""
        return v.strip()


class EntityList(BaseModel):
    """Container for a list of entities with validation.

    Provides convenient methods for serialization/deserialization.

    Example:
        >>> data = '[{"type": "NAME", "value": "John"}, {"type": "EMAIL", "value": "j@e.com"}]'
        >>> entities = EntityList.from_json(data)
        >>> len(entities.entities)
        2
    """
    entities: List[Entity] = Field(default_factory=list)

    @classmethod
    def from_json(cls, json_str: str) -> "EntityList":
        """Parse JSON string directly to EntityList.

        Args:
            json_str: JSON array string of entities

        Returns:
            EntityList instance with validated entities

        Raises:
            ValidationError: If JSON doesn't match schema
        """
        import json
        data = json.loads(json_str)
        return cls(entities=[Entity(**item) for item in data])

    @classmethod
    def from_list(cls, items: List[dict]) -> "EntityList":
        """Create EntityList from list of dictionaries.

        Args:
            items: List of entity dictionaries

        Returns:
            EntityList instance with validated entities
        """
        return cls(entities=[Entity(**item) for item in items])

    def to_dict_list(self) -> List[dict]:
        """Convert to list of dictionaries.

        Returns:
            List of entity dictionaries with string values
        """
        return [{"type": e.type.value, "value": e.value} for e in self.entities]

    def __len__(self) -> int:
        return len(self.entities)

    def __iter__(self) -> Iterator[Entity]:
        return iter(self.entities)
