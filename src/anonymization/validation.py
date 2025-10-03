"""
Agent 2: Direct Identifier Verification

Validates anonymized text to detect any remaining direct identifiers
that were missed by Agent 1.
"""

from dataclasses import dataclass
from typing import List
import json

from .llm import LLMClient


@dataclass(frozen=True)
class Issue:
    """Represents a remaining identifier found by Agent 2.

    Attributes:
        identifier_type: Type of identifier (NAME|EMAIL|PHONE|ADDRESS|IP|USERNAME|ID)
        value: The actual identifier text found in document
        context: ±20 characters around the identifier
        location_hint: Human-readable location description
    """
    identifier_type: str
    value: str
    context: str
    location_hint: str


@dataclass(frozen=True)
class ValidationResult:
    """Result of Agent 2 verification.

    Attributes:
        passed: True if no remaining identifiers found
        issues: List of remaining identifiers (empty if passed=True)
        agent_reasoning: Human-readable explanation of findings
        confidence: Agent's confidence in analysis (0.0-1.0)
    """
    passed: bool
    issues: List[Issue]
    agent_reasoning: str
    confidence: float


def validate_anonymization(anonymized_text: str) -> ValidationResult:
    """
    Validate that anonymized text contains no remaining direct identifiers.

    This function acts as Agent 2 (DIRECT-CHECK), independently scanning
    anonymized text to detect any personal identifiers that Agent 1 missed.

    Args:
        anonymized_text: The text after Agent 1 processing

    Returns:
        ValidationResult with pass/fail status and any issues found

    Raises:
        ValueError: If anonymized_text is None or not a string
        RuntimeError: If LLM client is not available

    Example:
        >>> result = validate_anonymization("[NAME_1] contacted [EMAIL_1]")
        >>> result.passed
        True
        >>> result = validate_anonymization("[NAME_1] and John contacted us")
        >>> result.passed
        False
        >>> len(result.issues)
        1
    """
    # Input validation
    if anonymized_text is None:
        raise ValueError("anonymized_text cannot be None")

    if not isinstance(anonymized_text, str):
        raise ValueError(f"anonymized_text must be a string, got {type(anonymized_text)}")

    # Handle empty input
    if not anonymized_text.strip():
        return ValidationResult(
            passed=True,
            issues=[],
            agent_reasoning="Empty document, nothing to validate",
            confidence=1.0
        )

    # Get LLM client
    llm = LLMClient()

    # Construct validation prompt
    prompt = _create_validation_prompt(anonymized_text)

    # Call LLM with retry logic
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            response = llm.generate(prompt)
            result = _parse_validation_response(response)
            return result
        except (ValueError, json.JSONDecodeError) as e:
            if attempt >= max_attempts:
                raise ValueError(f"Failed to parse LLM response after {max_attempts} attempts: {e}")
            # Retry on next iteration
            continue


def _create_validation_prompt(anonymized_text: str) -> str:
    """Create LLM prompt for validation task."""
    return f"""You are DIRECT-CHECK, the Direct Data Verification Agent. Your mission is to scan anonymized documents and flag ANY remaining direct personal identifiers.

IMPORTANT CONTEXT:
- This document has ALREADY been processed by an anonymization agent
- You will see placeholders like [NAME_1], [EMAIL_2], [PHONE_3], [ADDRESS_4]
- These placeholders are CORRECT and should be IGNORED
- Your job is to find identifiers that were MISSED

DIRECT IDENTIFIERS TO DETECT:
1. NAMES: Person names (first, last, full names, nicknames, initials like "J. Smith" or "JS")
2. EMAILS: Email addresses (full or partial like "@domain.com", "john@")
3. PHONES: Phone numbers (any format, including partial patterns)
4. ADDRESSES: Physical addresses (street addresses, postal codes)
5. IP: IP addresses or device identifiers
6. USERNAME: Account handles, usernames, social media handles
7. ID: Identification numbers (SSN, employee ID, etc.)

DO NOT FLAG:
- Existing placeholders ([NAME_X], [EMAIL_X], etc.)
- Generic terms (person, customer, user, company)
- Product names or common nouns
- Job titles alone (without identifying context)

DOCUMENT TO VERIFY:
---
{anonymized_text}
---

RESPOND IN JSON FORMAT ONLY:
{{
  "passed": boolean,
  "issues": [
    {{
      "type": "NAME|EMAIL|PHONE|ADDRESS|IP|USERNAME|ID",
      "value": "the actual identifier found",
      "context": "±20 chars around it",
      "location": "paragraph X" or "line Y"
    }}
  ],
  "reasoning": "explanation of findings",
  "confidence": 0.0 to 1.0
}}

EXAMPLES:

Example 1 - Clean document (all identifiers replaced):
Document: "[NAME_1] contacted [EMAIL_1] about the issue."
Response: {{
  "passed": true,
  "issues": [],
  "reasoning": "All identifiers properly anonymized with placeholders.",
  "confidence": 0.95
}}

Example 2 - Missed identifier:
Document: "[NAME_1] and John Smith contacted [EMAIL_1]."
Response: {{
  "passed": false,
  "issues": [
    {{
      "type": "NAME",
      "value": "John Smith",
      "context": "[NAME_1] and John Smith contacted",
      "location": "paragraph 1"
    }}
  ],
  "reasoning": "Found 1 remaining name that was not anonymized.",
  "confidence": 0.92
}}

Example 3 - Multiple issues:
Document: "Contact john@email.com or call 555-0123 for help."
Response: {{
  "passed": false,
  "issues": [
    {{
      "type": "EMAIL",
      "value": "john@email.com",
      "context": "Contact john@email.com or call",
      "location": "paragraph 1"
    }},
    {{
      "type": "PHONE",
      "value": "555-0123",
      "context": "or call 555-0123 for help",
      "location": "paragraph 1"
    }}
  ],
  "reasoning": "Found 2 remaining identifiers: 1 email and 1 phone number.",
  "confidence": 0.90
}}

Now verify the document above and respond with JSON only:"""


def _parse_validation_response(response: str) -> ValidationResult:
    """Parse LLM JSON response into ValidationResult."""
    # Extract JSON from response
    start = response.find('{')
    end = response.rfind('}') + 1

    if start == -1 or end <= start:
        raise ValueError("No JSON object found in response")

    json_str = response[start:end]
    data = json.loads(json_str)

    # Validate and normalize data
    passed = bool(data.get('passed', False))
    raw_issues = data.get('issues', [])
    reasoning = data.get('reasoning', 'No reasoning provided')
    confidence = float(data.get('confidence', 0.5))

    # Clamp confidence to valid range
    confidence = max(0.0, min(1.0, confidence))

    # Fix inconsistencies
    if passed and len(raw_issues) > 0:
        passed = False  # LLM made an error, issues exist so cannot pass
    elif not passed and len(raw_issues) == 0:
        passed = True  # LLM made an error, no issues so should pass

    # Create Issue objects
    issues = []
    for issue_data in raw_issues:
        issue = Issue(
            identifier_type=issue_data.get('type', 'UNKNOWN'),
            value=issue_data.get('value', ''),
            context=issue_data.get('context', ''),
            location_hint=issue_data.get('location', 'unknown location')
        )
        issues.append(issue)

    return ValidationResult(
        passed=passed,
        issues=issues,
        agent_reasoning=reasoning,
        confidence=confidence
    )
