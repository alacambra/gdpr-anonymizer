"""Agent prompts for the anonymization system."""

from .agent1_prompts import AGENT1_ENTITY_IDENTIFICATION_PROMPT
from .agent2_prompts import AGENT2_VALIDATION_PROMPT
from .agent3_prompts import AGENT3_RISK_ASSESSMENT_PROMPT

__all__ = [
    "AGENT1_ENTITY_IDENTIFICATION_PROMPT",
    "AGENT2_VALIDATION_PROMPT",
    "AGENT3_RISK_ASSESSMENT_PROMPT",
]
