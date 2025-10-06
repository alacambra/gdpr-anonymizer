"""Application configuration models."""

from typing import Optional
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """LLM provider configuration."""

    provider: str = Field(description="LLM provider (ollama, claude, openai)")
    model: str = Field(description="Model identifier")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, gt=0)
    api_key_env: Optional[str] = Field(
        default=None,
        description="Environment variable name for API key"
    )


class AgentConfig(BaseModel):
    """Configuration for an individual agent."""

    name: str = Field(description="Agent name")
    enabled: bool = Field(default=True, description="Whether agent is enabled")
    prompt_version: str = Field(default="v1", description="Prompt version to use")


class OrchestrationConfig(BaseModel):
    """Orchestration configuration."""

    max_iterations: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum retry iterations for validation failures"
    )
    timeout_seconds: int = Field(
        default=300,
        gt=0,
        description="Overall timeout for anonymization process"
    )


class AppConfig(BaseModel):
    """Complete application configuration."""

    llm: LLMConfig = Field(description="LLM configuration")
    agent1: AgentConfig = Field(description="Agent 1 configuration")
    agent2: AgentConfig = Field(description="Agent 2 configuration")
    agent3: AgentConfig = Field(description="Agent 3 configuration")
    orchestration: OrchestrationConfig = Field(description="Orchestration configuration")
