"""
LLM provider abstraction for anonymization.
Auto-detects and uses available LLM providers.
"""

import os
from typing import Any, Optional


class LLMClient:
    """Auto-detecting LLM client that uses the first available provider."""

    def __init__(self) -> None:
        self.provider: Optional[str] = None
        self.client: Any = None
        self._detect_provider()

    def _detect_provider(self) -> None:
        """Auto-detect available LLM provider in order: Ollama, Claude, OpenAI."""
        # Try Ollama first (local or remote)
        try:
            import ollama  # type: ignore[import-untyped]
            ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            ollama_token = os.getenv("OLLAMA_AUTH_TOKEN")

            # Build headers if auth token is provided
            headers = {}
            if ollama_token:
                headers["Authorization"] = f"Bearer {ollama_token}"

            self.provider = "ollama"
            self.client = ollama.Client(
                host=ollama_host,
                headers=headers if headers else None
            )
            return
        except ImportError:
            pass

        # Try Claude (Anthropic)
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                from anthropic import Anthropic  # type: ignore[import-untyped]
                self.provider = "claude"
                self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                return
            except ImportError:
                pass

        # Try OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI  # type: ignore[import-untyped]
                self.provider = "openai"
                self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                return
            except ImportError:
                pass

        raise ValueError(
            "No LLM provider available. Please either:\n"
            "1. Install and run Ollama locally (poetry install -E ollama)\n"
            "2. Set ANTHROPIC_API_KEY environment variable (poetry install -E claude)\n"
            "3. Set OPENAI_API_KEY environment variable (poetry install -E openai)"
        )

    def generate(self, prompt: str) -> str:
        """Send prompt to LLM and return text response.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Text response from the LLM
        """
        if self.provider == "ollama":
            response = self.client.generate(model="llama2", prompt=prompt)  # type: ignore[attr-defined]
            return str(response["response"])

        elif self.provider == "claude":
            message = self.client.messages.create(  # type: ignore[attr-defined]
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return str(message.content[0].text)

        elif self.provider == "openai":
            response = self.client.chat.completions.create(  # type: ignore[attr-defined]
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=4096
            )
            content = response.choices[0].message.content
            return str(content) if content else ""

        raise ValueError(f"Unknown provider: {self.provider}")
