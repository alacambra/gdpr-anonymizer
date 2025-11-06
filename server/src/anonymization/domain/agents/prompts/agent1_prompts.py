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
    return f"""<TASK>
Identify all personal data in the text provided below and return it as a JSON array.
</TASK>

<ENTITY_TYPES>
- NAME: Person names (first names, last names, full names)
- EMAIL: Email addresses
- PHONE: Phone numbers in any format
- ADDRESS: Physical addresses including street addresses and cities with street information
- ID: Identifiable numbers such as customer IDs, account numbers, patient numbers, insurance policy numbers, or transaction IDs

Do NOT include:

General demographic information like age, gender, or occupation unless combined with other identifying information
Medical conditions or diagnoses
Generic references like “patient” or “customer” without specific identifiers </ENTITY_TYPES>

</ENTITY_TYPES>

<OUTPUT_FORMAT>
Return your findings as a JSON array using this structure:
```json
[
  {{"type": "NAME", "value": "actual name found"}},
  {{"type": "EMAIL", "value": "actual email found"}},
  {{"type": "PHONE", "value": "actual phone found"}},
  {{"type": "ADDRESS", "value": "actual address found"}},
  {{"type": "ID", "value": "actual ID found"}}
]
```

Only include entities that you actually find in the text. If you find multiple instances of the same type, include each one as a separate object in the array.
</OUTPUT_FORMAT>
<TEXT_TO_ANALYZE>{text}</TEXT_TO_ANALYZE>
"""
