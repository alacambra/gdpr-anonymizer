"""Agent 1 Implementation - Entity Anonymization (ANON-EXEC).

Migrated from simple.py - maintains exact same logic.
"""

import json
import logging
import re
from typing import Dict, List, Optional
from pydantic import ValidationError

from ...domain.models import Entity, EntityType, AnonymizationMapping
from ...domain.ports import ILLMProvider
from ...domain.agents.prompts import AGENT1_ENTITY_IDENTIFICATION_PROMPT

logger = logging.getLogger(__name__)


class Agent1Implementation:
    """Agent 1: Entity identification and anonymization execution.

    Migrated from simple.py with identical behavior.
    """

    def __init__(self, llm_provider: ILLMProvider) -> None:
        """Initialize Agent 1 with an LLM provider.

        Args:
            llm_provider: LLM provider adapter for entity detection
        """
        self.llm = llm_provider

    def _clean_json_response(self, response: str) -> Optional[str]:
        """Clean and extract JSON from LLM response.

        Handles common issues:
        - Markdown code fences (```json ... ```)
        - Extra whitespace
        - Unescaped quotes in values
        - Truncated responses

        Args:
            response: Raw LLM response

        Returns:
            Cleaned JSON string or None if no valid JSON found
        """
        # Remove markdown code fences
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*', '', response)

        # Find JSON array boundaries
        start = response.find('[')
        end = response.rfind(']') + 1

        # Handle case where opening bracket exists but no closing bracket (truncation)
        if start != -1 and end <= start:
            logger.warning("JSON appears truncated (no closing bracket found)")
            json_str = response[start:]
        elif start == -1:
            return None
        else:
            json_str = response[start:end]

        # Try to fix common escaping issues
        try:
            # Attempt 1: Parse as-is
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError as e:
            # Attempt 2: Check if it's truncated (missing closing bracket)
            if not json_str.rstrip().endswith(']'):
                logger.warning(f"JSON appears truncated, attempting to fix: {e}")
                # Try to close the last object and array
                fixed = json_str.rstrip()
                # Remove any incomplete object at the end
                last_complete = fixed.rfind('},')
                if last_complete != -1:
                    fixed = fixed[:last_complete + 1] + ']'
                    try:
                        json.loads(fixed)
                        logger.info("Successfully fixed truncated JSON")
                        return fixed
                    except json.JSONDecodeError:
                        pass

            # Attempt 3: Try to escape unescaped quotes in values
            # This is risky, so we only do it as a last resort
            try:
                # Find all string values and escape internal quotes
                fixed = re.sub(
                    r'("value"\s*:\s*")(.*?)("(?:\s*[,}]))',
                    lambda m: m.group(1) + m.group(2).replace('"', '\\"') + m.group(3),
                    json_str
                )
                json.loads(fixed)
                logger.info("Successfully fixed unescaped quotes in JSON")
                return fixed
            except (json.JSONDecodeError, re.error):
                pass

        return json_str  # Return original if all fixes failed

    async def anonymize(self, text: str) -> AnonymizationMapping:
        """Identify and replace personal data entities in text.

        Args:
            text: Original text to anonymize

        Returns:
            AnonymizationMapping with replacements and entity list

        Raises:
            ValueError: If entity parsing fails after retries
        """
        # Handle empty input
        if not text.strip():
            return AnonymizationMapping(
                original_text=text,
                anonymized_text=text,
                mappings={},
                entities=[]
            )

        # Retry logic for LLM calls
        max_attempts = 2
        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                # Generate prompt and call LLM
                prompt = AGENT1_ENTITY_IDENTIFICATION_PROMPT(text)
                response = await self.llm.generate(prompt)

                # Parse entities from response (with automatic cleaning/fixing)
                entities = self._parse_entities(response, attempt)

                # Build mappings from entities
                mappings = self._build_mappings(entities)

                # Apply replacements to text
                anonymized_text = self._apply_replacements(text, mappings)

                return AnonymizationMapping(
                    original_text=text,
                    anonymized_text=anonymized_text,
                    mappings=mappings,
                    entities=entities
                )

            except (ValueError, json.JSONDecodeError) as e:
                last_error = e
                if attempt >= max_attempts:
                    # Final attempt failed - raise with full context
                    raise ValueError(
                        f"Failed to parse LLM response after {max_attempts} attempts. "
                        f"Last error: {str(e)}"
                    )
                logger.warning(f"Attempt {attempt}/{max_attempts} failed, retrying: {e}")
                continue

        # Should never reach here, but satisfy type checker
        raise ValueError(f"Unexpected error in anonymization: {last_error}")

    def _parse_entities(self, response: str, attempt: int = 1) -> List[Entity]:
        """Parse entity list from LLM JSON response.

        Args:
            response: LLM response containing JSON array
            attempt: Current attempt number (for logging)

        Returns:
            List of Entity objects

        Raises:
            ValueError: If response cannot be parsed
            json.JSONDecodeError: If JSON is malformed
        """
        try:
            # Clean and extract JSON from response
            json_str = self._clean_json_response(response)

            if json_str is None:
                logger.error(f"No JSON array found in LLM response (attempt {attempt})")
                logger.debug(f"Full response: {response}")
                raise ValueError("No JSON array found in LLM response")

            # Parse JSON
            data = json.loads(json_str)

            # Validate it's a list
            if not isinstance(data, list):
                logger.error(f"Expected JSON array, got {type(data).__name__}")
                raise ValueError(f"Expected JSON array, got {type(data).__name__}")

            # Convert to Entity objects
            entities = []
            for idx, item in enumerate(data):
                try:
                    entity = Entity(
                        type=EntityType(item["type"]),
                        value=item["value"]
                    )
                    entities.append(entity)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Skipping invalid entity at index {idx}: {item}. Error: {e}")
                    continue

            return entities

        except (ValueError, ValidationError, KeyError, json.JSONDecodeError) as e:
            # Log full response for debugging
            logger.error(f"Failed to parse LLM response (attempt {attempt}): {e}")
            logger.debug(f"Full LLM response:\n{response}")

            # Raise with detailed error but don't truncate
            raise ValueError(
                f"Failed to parse LLM response as valid entities. "
                f"Error: {str(e)}. "
                f"Response length: {len(response)} chars. "
                f"Response preview: {response[:500]}..."
            ) from e

    def _build_mappings(self, entities: List[Entity]) -> Dict[str, str]:
        """Build mappings from original values to placeholders.

        Args:
            entities: List of detected entities

        Returns:
            Dictionary mapping original values to placeholders
        """
        mappings = {}
        counters = {"NAME": 0, "EMAIL": 0, "PHONE": 0, "ADDRESS": 0, "OTHER": 0}

        for entity in entities:
            entity_type = entity.type.value
            value = entity.value

            # Skip if already mapped
            if value in mappings:
                continue

            # Create placeholder
            counters[entity_type] += 1
            placeholder = f"[{entity_type}_{counters[entity_type]}]"
            mappings[value] = placeholder

        return mappings

    def _apply_replacements(self, text: str, mappings: Dict[str, str]) -> str:
        """Apply all entity replacements to text.

        Args:
            text: Original text
            mappings: Dictionary of value -> placeholder mappings

        Returns:
            Text with all replacements applied
        """
        result = text

        # Sort by length (longest first) to avoid partial replacements
        sorted_items = sorted(
            mappings.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for original, placeholder in sorted_items:
            result = result.replace(original, placeholder)

        return result
