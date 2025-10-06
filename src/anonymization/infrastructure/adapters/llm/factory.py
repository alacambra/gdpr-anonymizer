"""Factory for creating LLM provider adapters."""

from typing import Any, Dict
from .ollama_adapter import OllamaAdapter
from .claude_adapter import ClaudeAdapter
from .openai_adapter import OpenAIAdapter


def create_llm_provider(provider: str, config: Dict[str, Any]) -> Any:
    """Create an LLM provider adapter based on configuration.

    Args:
        provider: Provider name ("ollama", "claude", or "openai")
        config: Configuration dictionary for the provider

    Returns:
        Initialized LLM adapter instance

    Raises:
        ValueError: If provider is unknown

    Example:
        >>> config = {"model": "gpt-4", "temperature": 0.1}
        >>> adapter = create_llm_provider("openai", config)
    """
    provider = provider.lower()

    if provider == "ollama":
        return OllamaAdapter(
            model=config.get("model", "gemma-custom")
        )
    elif provider == "claude":
        return ClaudeAdapter(
            model=config.get("model", "claude-3-5-sonnet-20241022"),
            max_tokens=config.get("max_tokens", 4096),
            temperature=config.get("temperature", 0.1)
        )
    elif provider == "openai":
        return OpenAIAdapter(
            model=config.get("model", "gpt-4"),
            max_tokens=config.get("max_tokens", 4096),
            temperature=config.get("temperature", 0.1)
        )
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider}. "
            f"Supported providers: ollama, claude, openai"
        )
