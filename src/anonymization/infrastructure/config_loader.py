"""Configuration loader with YAML support and environment variable substitution."""

import os
import re
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import ValidationError

from ..application.config import AppConfig, LLMConfig, AgentConfig, OrchestrationConfig


class ConfigLoader:
    """Loads and validates application configuration from YAML files.

    Supports environment variable substitution in the format ${VAR_NAME}.
    """

    @staticmethod
    def load_from_file(config_path: Path) -> AppConfig:
        """Load configuration from a YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            Validated AppConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
            ValidationError: If config doesn't match schema
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Read YAML file
        with open(config_path, 'r') as f:
            raw_config = yaml.safe_load(f)

        # Substitute environment variables
        config_dict = ConfigLoader._substitute_env_vars(raw_config)

        # Validate and construct AppConfig
        try:
            return AppConfig(
                llm=LLMConfig(**config_dict['llm']),
                agent1=AgentConfig(**config_dict['agents']['agent1']),
                agent2=AgentConfig(**config_dict['agents']['agent2']),
                agent3=AgentConfig(**config_dict['agents']['agent3']),
                orchestration=OrchestrationConfig(**config_dict['orchestration'])
            )
        except (KeyError, ValidationError) as e:
            raise ValueError(f"Invalid configuration: {e}") from e

    @staticmethod
    def _substitute_env_vars(data: Any) -> Any:
        """Recursively substitute environment variables in configuration.

        Supports ${VAR_NAME} syntax.

        Args:
            data: Configuration data (dict, list, string, etc.)

        Returns:
            Data with environment variables substituted
        """
        if isinstance(data, dict):
            return {k: ConfigLoader._substitute_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [ConfigLoader._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            return ConfigLoader._substitute_string(data)
        else:
            return data

    @staticmethod
    def _substitute_string(value: str) -> str:
        """Substitute environment variables in a string.

        Args:
            value: String that may contain ${VAR_NAME} patterns

        Returns:
            String with variables substituted

        Raises:
            ValueError: If required environment variable is not set
        """
        pattern = r'\$\{([^}]+)\}'

        def replace_var(match):
            var_name = match.group(1)
            env_value = os.getenv(var_name)
            if env_value is None:
                raise ValueError(f"Environment variable not set: {var_name}")
            return env_value

        return re.sub(pattern, replace_var, value)

    @staticmethod
    def create_default_config() -> Dict[str, Any]:
        """Create a default configuration dictionary.

        Returns:
            Default configuration as a dictionary
        """
        return {
            'llm': {
                'provider': 'claude',
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.1,
                'max_tokens': 4096,
                'api_key_env': 'ANTHROPIC_API_KEY'
            },
            'agents': {
                'agent1': {
                    'name': 'ANON-EXEC',
                    'enabled': True,
                    'prompt_version': 'v1'
                },
                'agent2': {
                    'name': 'DIRECT-CHECK',
                    'enabled': True,
                    'prompt_version': 'v1'
                },
                'agent3': {
                    'name': 'RISK-ASSESS',
                    'enabled': True,
                    'prompt_version': 'v1'
                }
            },
            'orchestration': {
                'max_iterations': 3,
                'timeout_seconds': 300
            }
        }
