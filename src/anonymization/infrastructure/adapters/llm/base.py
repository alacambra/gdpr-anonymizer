"""Base LLM adapter with common functionality."""

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMAdapter(ABC):
    """Abstract base class for LLM provider adapters.

    Provides common functionality and enforces interface contract
    for all LLM providers.
    """

    def __init__(self) -> None:
        """Initialize the LLM adapter."""
        self.client: Any = None
        self._initialize_client()

    @abstractmethod
    def _initialize_client(self) -> None:
        """Initialize the provider-specific client.

        This method must be implemented by each concrete adapter.
        """
        pass

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The prompt text to send to the LLM

        Returns:
            The text response from the LLM

        Raises:
            Exception: If LLM call fails
        """
        pass
