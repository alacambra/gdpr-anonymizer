"""Ollama LLM adapter implementation."""

import os
from typing import Any, Optional
from .base import BaseLLMAdapter


class OllamaAdapter(BaseLLMAdapter):
    """Adapter for Ollama LLM provider.

    Supports both local and remote Ollama instances with optional authentication.
    Configuration priority: config params > environment variables > defaults
    """

    def __init__(
        self,
        model: str = "gemma-custom",
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None
    ) -> None:
        """Initialize Ollama adapter.

        Args:
            model: Name of the Ollama model to use
            base_url: Ollama server URL (falls back to OLLAMA_HOST env var)
            auth_token: Optional authentication token (falls back to OLLAMA_AUTH_TOKEN env var)
        """
        self.model = model
        self.base_url = base_url
        self.auth_token = auth_token
        super().__init__()

    def _initialize_client(self) -> None:
        """Initialize Ollama client with host and auth configuration.

        Priority for configuration:
        1. Constructor parameters (from config file)
        2. Environment variables (OLLAMA_HOST, OLLAMA_AUTH_TOKEN)
        3. Defaults (http://localhost:11434)
        """
        try:
            import ollama  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Ollama package not installed. Install with: pip install ollama"
            )

        # Priority: config param > env var > default
        ollama_host = self.base_url or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_token = self.auth_token or os.getenv("OLLAMA_AUTH_TOKEN")

        # Build client kwargs - only pass headers if auth token is provided
        # Note: ollama.Client doesn't handle None for headers parameter correctly
        client_kwargs = {"host": ollama_host}
        if ollama_token:
            client_kwargs["headers"] = {"Authorization": f"Bearer {ollama_token}"}

        self.client = ollama.Client(**client_kwargs)

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
