"""Ollama LLM adapter implementation."""

import os
from typing import Any
from .base import BaseLLMAdapter


class OllamaAdapter(BaseLLMAdapter):
    """Adapter for Ollama LLM provider.

    Supports both local and remote Ollama instances with optional authentication.
    """

    def __init__(self, model: str = "gemma-custom") -> None:
        """Initialize Ollama adapter.

        Args:
            model: Name of the Ollama model to use
        """
        self.model = model
        super().__init__()

    def _initialize_client(self) -> None:
        """Initialize Ollama client with host and auth configuration."""
        try:
            import ollama  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Ollama package not installed. Install with: pip install ollama"
            )

        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_token = os.getenv("OLLAMA_AUTH_TOKEN")

        headers = {}
        if ollama_token:
            headers["Authorization"] = f"Bearer {ollama_token}"

        self.client = ollama.Client(
            host=ollama_host,
            headers=headers if headers else None
        )

    async def generate(self, prompt: str) -> str:
        """Generate response using Ollama.

        Args:
            prompt: The prompt text

        Returns:
            Text response from Ollama

        Raises:
            Exception: If Ollama call fails
        """
        response = self.client.generate(model=self.model, prompt=prompt)
        return str(response["response"])
