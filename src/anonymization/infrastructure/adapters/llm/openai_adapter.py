"""OpenAI LLM adapter implementation."""

import os
from .base import BaseLLMAdapter


class OpenAIAdapter(BaseLLMAdapter):
    """Adapter for OpenAI's GPT models.

    Requires OPENAI_API_KEY environment variable.
    """

    def __init__(
        self,
        model: str = "gpt-4",
        max_tokens: int = 4096,
        temperature: float = 0.1
    ) -> None:
        """Initialize OpenAI adapter.

        Args:
            model: OpenAI model identifier (e.g., gpt-4, gpt-3.5-turbo)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        super().__init__()

    def _initialize_client(self) -> None:
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set"
            )

        self.client = OpenAI(api_key=api_key)

    async def generate(self, prompt: str) -> str:
        """Generate response using OpenAI.

        Args:
            prompt: The prompt text

        Returns:
            Text response from OpenAI

        Raises:
            Exception: If OpenAI API call fails
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        content = response.choices[0].message.content
        return str(content) if content else ""
