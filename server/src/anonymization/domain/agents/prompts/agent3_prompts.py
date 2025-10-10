"""Agent 3 (RISK-ASSESS) prompts for risk assessment.

Version: v1 (Stub)
Last Updated: 2025-10-06

Note: This is a stub implementation. Agent 3 does not currently use LLM
      and returns hardcoded NEGLIGIBLE risk. This prompt is reserved for
      future implementation.
"""


def AGENT3_RISK_ASSESSMENT_PROMPT(anonymized_text: str) -> str:
    """Create prompt for Agent 3 risk assessment.

    Note: Currently unused as Agent 3 is a stub implementation.

    Args:
        anonymized_text: The text after Agent 1 + Agent 2 processing

    Returns:
        Formatted prompt string for the LLM (reserved for future use)
    """
    return f"""You are RISK-ASSESS, the GDPR Compliance Risk Assessment Agent.

DOCUMENT TO ASSESS:
---
{anonymized_text}
---

Evaluate re-identification risk across 5 dimensions (1-5 each):
1. Direct Identifier Risk
2. Quasi-Identifier Risk
3. Contextual Disclosure Risk
4. Linkability Risk
5. Inference Risk

Respond with JSON:
{{
  "overall_score": 5-25,
  "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|NEGLIGIBLE",
  "gdpr_compliant": boolean,
  "reasoning": "explanation",
  "confidence": 0.0-1.0
}}

NOTE: This prompt is currently unused. Agent 3 is a stub."""
