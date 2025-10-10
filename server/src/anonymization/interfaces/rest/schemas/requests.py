"""API request schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AnonymizeRequest(BaseModel):
    """Request to anonymize a single document.

    Example:
        {
            "text": "Contact John Smith at john@email.com",
            "document_id": "doc-123"
        }
    """

    text: str = Field(
        description="Text content to anonymize",
        min_length=1
    )
    document_id: Optional[str] = Field(
        default=None,
        description="Optional unique identifier for the document"
    )


class BatchAnonymizeRequest(BaseModel):
    """Request to anonymize multiple documents.

    Example:
        {
            "documents": [
                {"text": "Document 1", "document_id": "doc-1"},
                {"text": "Document 2", "document_id": "doc-2"}
            ]
        }
    """

    documents: List[AnonymizeRequest] = Field(
        description="List of documents to anonymize",
        min_length=1
    )
