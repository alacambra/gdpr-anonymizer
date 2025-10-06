"""Agent 1 (ANON-EXEC) prompts for entity identification and anonymization.

Version: v1
Last Updated: 2025-10-06
"""


def AGENT1_ENTITY_IDENTIFICATION_PROMPT(text: str) -> str:
    """Create prompt for Agent 1 to identify personal data entities.

    Args:
        text: The text to analyze for personal data

    Returns:
        Formatted prompt string for the LLM
    """
    return f"""Identify all personal data in the following text and return ONLY a JSON array.

Entity types to identify:
- NAME: Person names (first, last, full names)
- EMAIL: Email addresses
- PHONE: Phone numbers (any format)
- ADDRESS: Physical addresses (street addresses, cities with street info)
- OTHER: Any other identifiable information (IDs, account numbers, patient numbers, insurance policy numbers, transaction references, medical record numbers, etc.)

Return format (JSON only, no other text):
[
  {{"type": "NAME", "value": "John Smith"}},
  {{"type": "EMAIL", "value": "john@email.com"}},
  {{"type": "PHONE", "value": "555-123-4567"}},
  {{"type": "ADDRESS", "value": "123 Main Street"}},
  {{"type": "OTHER", "value": "PAT-12345"}}
]

Text to analyze:
{text}

JSON array:"""
