"""
Core anonymization logic - Iteration 1 minimal implementation.
"""

import json
from typing import Any, Dict, List

from . import AnonymizationResult
from .llm import LLMClient


def anonymize_simple(text: str) -> AnonymizationResult:
    """
    Anonymize text containing personal information.

    This function identifies and replaces personal data (names, emails, phone numbers,
    addresses) with standardized placeholders like [NAME_1], [EMAIL_1], etc.

    Args:
        text: Plain text string to anonymize

    Returns:
        AnonymizationResult with anonymized_text, mappings, and original_text

    Example:
        >>> result = anonymize_simple("Contact John Smith at john@email.com")
        >>> print(result.anonymized_text)
        Contact [NAME_1] at [EMAIL_1]
        >>> print(result.mappings)
        {'John Smith': '[NAME_1]', 'john@email.com': '[EMAIL_1]'}
    """
    # Handle empty input
    if not text.strip():
        return AnonymizationResult(
            anonymized_text=text,
            mappings={},
            original_text=text
        )

    # Initialize LLM client
    llm = LLMClient()

    # Create prompt for entity identification
    prompt = _create_entity_identification_prompt(text)

    # Get LLM response
    response = llm.generate(prompt)

    # Parse entities from response
    entities = _parse_entities(response)

    # Build entity mappings with placeholders
    mappings = _build_mappings(entities)

    # Apply replacements to text
    anonymized_text = _apply_replacements(text, mappings)

    return AnonymizationResult(
        anonymized_text=anonymized_text,
        mappings=mappings,
        original_text=text
    )


def _create_entity_identification_prompt(text: str) -> str:
    """Create prompt for LLM to identify personal data entities."""
    return f"""Identify all personal data in the following text and return ONLY a JSON array.

Entity types to identify:
- NAME: Person names (first, last, full names)
- EMAIL: Email addresses
- PHONE: Phone numbers (any format)
- ADDRESS: Physical addresses (street addresses, cities with street info)

Return format (JSON only, no other text):
[
  {{"type": "NAME", "value": "John Smith"}},
  {{"type": "EMAIL", "value": "john@email.com"}},
  {{"type": "PHONE", "value": "555-123-4567"}},
  {{"type": "ADDRESS", "value": "123 Main Street"}}
]

Text to analyze:
{text}

JSON array:"""


def _parse_entities(response: str) -> List[Dict[str, str]]:
    """Parse entity list from LLM JSON response."""
    try:
        # Try to find JSON array in response
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            entities: List[Dict[str, Any]] = json.loads(json_str)
            # Validate that we have a list of dicts with string values
            result: List[Dict[str, str]] = []
            for entity in entities:
                if isinstance(entity, dict):
                    result.append({
                        "type": str(entity.get("type", "")),
                        "value": str(entity.get("value", ""))
                    })
            return result
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON. Response excerpt: {response[:200]}") from e


def _build_mappings(entities: List[Dict[str, str]]) -> Dict[str, str]:
    """Build mappings from original values to placeholders."""
    mappings = {}
    counters = {"NAME": 0, "EMAIL": 0, "PHONE": 0, "ADDRESS": 0}

    for entity in entities:
        entity_type = entity.get("type", "").upper()
        value = entity.get("value", "").strip()

        if not value or value in mappings:
            continue

        if entity_type in counters:
            counters[entity_type] += 1
            placeholder = f"[{entity_type}_{counters[entity_type]}]"
            mappings[value] = placeholder

    return mappings


def _apply_replacements(text: str, mappings: Dict[str, str]) -> str:
    """Apply all entity replacements to text."""
    result = text

    # Sort by length (longest first) to avoid partial replacements
    sorted_items = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)

    for original, placeholder in sorted_items:
        result = result.replace(original, placeholder)

    return result
