"""Agent 2 Implementation - Direct Identifier Verification (DIRECT-CHECK).

Migrated from validation.py - maintains exact same logic.
"""

import json
from ...domain.models import ValidationResult, ValidationIssue
from ...domain.ports import ILLMProvider
from ...domain.agents.prompts import AGENT2_VALIDATION_PROMPT


class Agent2Implementation:
    """Agent 2: Direct identifier verification.

    Migrated from validation.py with identical behavior.
    """

    def __init__(self, llm_provider: ILLMProvider) -> None:
        """Initialize Agent 2 with an LLM provider.

        Args:
            llm_provider: LLM provider adapter for validation
        """
        self.llm = llm_provider

    async def validate(self, anonymized_text: str) -> ValidationResult:
        """Validate anonymized text for remaining identifiers.

        Args:
            anonymized_text: Text after Agent 1 processing

        Returns:
            ValidationResult with pass/fail status and issues

        Raises:
            ValueError: If anonymized_text is invalid or parsing fails
        """
        # Input validation
        if anonymized_text is None:
            raise ValueError("anonymized_text cannot be None")

        if not isinstance(anonymized_text, str):
            raise ValueError(
                f"anonymized_text must be a string, got {type(anonymized_text)}"
            )

        # Handle empty input
        if not anonymized_text.strip():
            return ValidationResult(
                passed=True,
                issues=[],
                reasoning="Empty document, nothing to validate",
                confidence=1.0
            )

        # Generate prompt
        prompt = AGENT2_VALIDATION_PROMPT(anonymized_text)

        # Retry logic for LLM calls
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                response = await self.llm.generate(prompt)
                result = self._parse_validation_response(response)
                return result
            except (ValueError, json.JSONDecodeError) as e:
                if attempt >= max_attempts:
                    raise ValueError(
                        f"Failed to parse LLM response after {max_attempts} attempts: {e}"
                    )
                continue

        # This should never be reached due to the raise above
        raise RuntimeError(
            "Unexpected error: validation loop completed without returning or raising"
        )

    def _parse_validation_response(self, response: str) -> ValidationResult:
        """Parse LLM JSON response into ValidationResult.

        Args:
            response: LLM response containing JSON

        Returns:
            ValidationResult object

        Raises:
            ValueError: If response cannot be parsed
            json.JSONDecodeError: If JSON is malformed
        """
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

        # Fix inconsistencies between passed and issues
        if passed and len(raw_issues) > 0:
            passed = False  # Issues exist, cannot pass
        elif not passed and len(raw_issues) == 0:
            passed = True  # No issues, should pass

        # Create ValidationIssue objects
        issues = []
        for issue_data in raw_issues:
            issue = ValidationIssue(
                identifier_type=issue_data.get('type', 'UNKNOWN'),
                value=issue_data.get('value', ''),
                context=issue_data.get('context', ''),
                location_hint=issue_data.get('location', 'unknown location')
            )
            issues.append(issue)

        return ValidationResult(
            passed=passed,
            issues=issues,
            reasoning=reasoning,
            confidence=confidence
        )
