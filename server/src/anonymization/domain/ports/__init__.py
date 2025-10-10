"""Port interfaces for hexagonal architecture."""

from .agent_interfaces import IAgent1, IAgent2, IAgent3
from .llm_provider_interface import ILLMProvider

__all__ = [
    "IAgent1",
    "IAgent2",
    "IAgent3",
    "ILLMProvider",
]
