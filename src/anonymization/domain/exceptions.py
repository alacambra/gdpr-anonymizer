"""Domain-level exceptions."""


class DomainException(Exception):
    """Base exception for all domain-level errors."""
    pass


class InvalidDocumentError(DomainException):
    """Raised when a document is invalid or cannot be processed."""
    pass


class AnonymizationError(DomainException):
    """Raised when anonymization processing fails."""
    pass


class ValidationError(DomainException):
    """Raised when validation processing fails."""
    pass


class RiskAssessmentError(DomainException):
    """Raised when risk assessment processing fails."""
    pass
