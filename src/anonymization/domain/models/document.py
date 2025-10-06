"""Document entity for text anonymization."""

from typing import Optional
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Represents a text document to be anonymized.

    This is the core domain entity representing a document that flows
    through the anonymization pipeline.

    Attributes:
        content: The text content of the document
        document_id: Optional unique identifier for the document
        metadata: Optional dictionary of document metadata

    Example:
        >>> doc = Document(content="Contact John at john@email.com")
        >>> doc.content
        'Contact John at john@email.com'
    """

    content: str = Field(description="Text content of the document")
    document_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the document"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Optional metadata about the document"
    )

    def is_empty(self) -> bool:
        """Check if document content is empty or whitespace only."""
        return not self.content.strip()

    def word_count(self) -> int:
        """Get approximate word count of document."""
        return len(self.content.split())

    class Config:
        frozen = True  # Immutable entity
