"""Dependency injection for FastAPI."""

from pathlib import Path
from functools import lru_cache
from typing import Any

from ...application.config import AppConfig
from ...application.orchestrator import AnonymizationOrchestrator
from ...infrastructure.config_loader import ConfigLoader
from ...infrastructure.adapters.llm import create_llm_provider
from ...infrastructure.agents import (
    Agent1Implementation,
    Agent2Implementation,
    Agent3Implementation
)


@lru_cache()
def get_config() -> AppConfig:
    """Get application configuration (singleton).

    Returns:
        AppConfig instance loaded from config.yaml

    Raises:
        FileNotFoundError: If config file not found
        ValueError: If config is invalid
    """
    config_path = Path("config/config.yaml")
    return ConfigLoader.load_from_file(config_path)


@lru_cache()
def get_llm_provider() -> Any:
    """Get LLM provider instance (singleton).

    Returns:
        LLM provider adapter instance

    Raises:
        ValueError: If provider configuration is invalid
    """
    config = get_config()
    llm_config = {
        "model": config.llm.model,
        "temperature": config.llm.temperature,
        "max_tokens": config.llm.max_tokens
    }

    # Add ollama-specific configuration if present
    if config.llm.ollama:
        llm_config["ollama"] = {
            "base_url": config.llm.ollama.base_url,
            "auth_token": config.llm.ollama.auth_token
        }

    return create_llm_provider(
        provider=config.llm.provider,
        config=llm_config
    )


def get_orchestrator() -> AnonymizationOrchestrator:
    """Get orchestrator instance (per-request).

    Returns:
        AnonymizationOrchestrator with configured agents
    """
    config = get_config()
    llm_provider = get_llm_provider()

    # Create agent instances
    agent1 = Agent1Implementation(llm_provider)
    agent2 = Agent2Implementation(llm_provider)
    agent3 = Agent3Implementation(llm_provider)

    # Create and return orchestrator
    return AnonymizationOrchestrator(
        agent1=agent1,
        agent2=agent2,
        agent3=agent3,
        max_iterations=config.orchestration.max_iterations
    )
