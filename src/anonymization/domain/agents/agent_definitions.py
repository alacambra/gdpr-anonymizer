"""Core agent role definitions."""

from enum import Enum


class AgentRole(str, Enum):
    """Enumeration of agent roles in the anonymization system."""

    ANON_EXEC = "ANON-EXEC"
    """Agent 1: Entity identification and anonymization execution"""

    DIRECT_CHECK = "DIRECT-CHECK"
    """Agent 2: Direct identifier verification"""

    RISK_ASSESS = "RISK-ASSESS"
    """Agent 3: GDPR compliance risk assessment"""
