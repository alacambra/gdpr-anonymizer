"""Claude (Anthropic) LLM adapter implementation."""

import os
from .base import BaseLLMAdapter


class ClaudeAdapter(BaseLLMAdapter):
    """Adapter for Anthropic's Claude LLM.

    Requires ANTHROPIC_API_KEY environment variable.
    """

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 0.1
    ) -> None:
        """Initialize Claude adapter.

        Args:
            model: Claude model identifier
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        super().__init__()

    def _initialize_client(self) -> None:
        """Initialize Anthropic client."""
        try:
            from anthropic import Anthropic  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set"
            )

        self.client = Anthropic(api_key=api_key)

    async def generate(self, prompt: str) -> str:
        """Generate response using Claude.

        Args:
            prompt: The prompt text

        Returns:
            Text response from Claude

        Raises:
            Exception: If Claude API call fails
        """
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return str(message.content[0].text)
