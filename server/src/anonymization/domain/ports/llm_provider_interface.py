"""LLM Provider interface - Port for infrastructure adapters."""

from typing import Protocol


class ILLMProvider(Protocol):
    """Interface for LLM provider adapters.

    All LLM adapters (Ollama, Claude, OpenAI) must implement this interface.
    This allows the domain and application layers to remain independent of
    specific LLM provider implementations.

    Example:
        >>> class MyLLMAdapter:
        ...     async def generate(self, prompt: str) -> str:
        ...         return "response from LLM"
    """

    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The prompt text to send to the LLM

        Returns:
            The text response from the LLM

        Raises:
            Exception: If LLM call fails
        """
        ...
