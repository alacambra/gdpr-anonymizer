"""Agent 1 Implementation - Entity Anonymization (ANON-EXEC).

Migrated from simple.py - maintains exact same logic.
"""

import json
import logging
import re
from typing import Dict, List, Optional
from pydantic import BaseModel, ValidationError, field_validator

from ...domain.models import Entity, EntityType, AnonymizationMapping
from ...domain.ports import ILLMProvider
from ...domain.agents.prompts import AGENT1_ENTITY_IDENTIFICATION_PROMPT

class LLMEntityResponse(BaseModel):

    """Pydantic model for validating LLM entity response structure."""
    type: str
    value: str

    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate that type is one of the allowed EntityType values."""
        valid_types = {"NAME", "EMAIL", "PHONE", "ADDRESS", "DATE", "AGE",
                       "ID", "LOCATION", "ORGANIZATION", "MEDICATION", "CONDITION", "OTHER"}
        if v.upper() not in valid_types:
            raise ValueError(
                f"Invalid entity type: {v}. Must be one of {valid_types}")
        return v.upper()


class LLMEntitiesListResponse(BaseModel):
    """Pydantic model for validating the complete LLM response (array of entities)."""
    entities: List[LLMEntityResponse]


class Agent1Implementation:
    logger = logging.getLogger(__name__)
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
            self.logger.warning("JSON appears truncated (no closing bracket found)")
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
                self.logger.warning(
                    f"JSON appears truncated, attempting to fix: {e}")
                # Try to close the last object and array
                fixed = json_str.rstrip()
                # Remove any incomplete object at the end
                last_complete = fixed.rfind('},')
                if last_complete != -1:
                    fixed = fixed[:last_complete + 1] + ']'
                    try:
                        json.loads(fixed)
                        self.logger.info("Successfully fixed truncated JSON")
                        return fixed
                    except json.JSONDecodeError:
                        pass

            # Attempt 3: Try to escape unescaped quotes in values
            # This is risky, so we only do it as a last resort
            try:
                # Find all string values and escape internal quotes
                fixed = re.sub(
                    r'("value"\s*:\s*")(.*?)("(?:\s*[,}]))',
                    lambda m: m.group(
                        1) + m.group(2).replace('"', '\\"') + m.group(3),
                    json_str
                )
                json.loads(fixed)
                self.logger.info("Successfully fixed unescaped quotes in JSON")
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

                self.logger.warning("sending AGENT1_ENTITY_IDENTIFICATION_PROMPT")
                self.logger.info(prompt)

                response = await self.llm.generate(prompt)

                self.logger.info("response received")

                # Parse entities from response (with automatic cleaning/fixing)
                result: tuple[list[Entity], list[Entity]] = self._parse_entities(
                    response, attempt)

                skippedEntites = result[1]
                entities = result[0]
                mappings = self._build_mappings(entities)

                # Apply replacements to text
                anonymized_text = self._apply_replacements(text, mappings)

                return AnonymizationMapping(
                    original_text=text,
                    anonymized_text=anonymized_text,
                    mappings=mappings,
                    entities=entities,
                    skippedEntites=skippedEntites
                )

            except (ValueError, json.JSONDecodeError) as e:
                last_error = e
                if attempt >= max_attempts:
                    # Final attempt failed - raise with full context
                    raise ValueError(
                        f"Failed to parse LLM response after {max_attempts} attempts. "
                        f"Last error: {str(e)}"
                    )
                self.logger.warning(
                    f"Attempt {attempt}/{max_attempts} failed, retrying: {e}")
                continue

        # Should never reach here, but satisfy type checker
        raise ValueError(f"Unexpected error in anonymization: {last_error}")

    def _parse_entities(self, response: str, attempt: int = 1) -> tuple[list[Entity], list[Entity]]:
        """Parse entity list from LLM JSON response with Pydantic validation.

        Args:
            response: LLM response containing JSON array
            attempt: Current attempt number (for logging)

        Returns:
            List of Entity objects

        Raises:
            ValueError: If response cannot be parsed or has no valid entities
            json.JSONDecodeError: If JSON is malformed
        """
        skipped_entities = []

        try:
            # Clean and extract JSON from response
            json_str = self._clean_json_response(response)

            if json_str is None:
                self.logger.error(
                    f"No JSON array found in LLM response (attempt {attempt})")
                self.logger.debug(f"Full response: {response}")
                raise ValueError("No JSON array found in LLM response")

            # Parse JSON
            data = json.loads(json_str)

            # Validate it's a list
            if not isinstance(data, list):
                self.logger.error(f"Expected JSON array, got {type(data).__name__}")
                raise ValueError(
                    f"Expected JSON array, got {type(data).__name__}")

            # Pydantic validation: validate entire structure first
            try:
                validated_response = LLMEntitiesListResponse(entities=data)
                self.logger.info(
                    f"LLM response structure validated successfully with {len(validated_response.entities)} entities")
            except ValidationError as ve:
                self.logger.warning(
                    f"Pydantic validation failed, falling back to per-entity validation: {ve}")
                # Fall through to per-entity validation below

            # Convert to Entity objects (with per-entity error handling)
            entities = []
            for idx, item in enumerate(data):
                try:
                    # Validate individual entity with Pydantic
                    validated_entity = LLMEntityResponse(**item)

                    # Create domain Entity object
                    entity = Entity(
                        type=EntityType(validated_entity.type),
                        value=validated_entity.value
                    )
                    entities.append(entity)

                except (KeyError, ValueError, ValidationError) as e:
                    error_msg = f"Invalid entity at index {idx}: {item}. Error: {e}"
                    self.logger.warning(f"Skipping {error_msg}")
                    skipped_entities.append(
                        {"index": idx, "item": item, "error": str(e)})
                    continue

            # Log statistics
            total_entities = len(data)
            valid_entities = len(entities)
            invalid_entities = len(skipped_entities)

            self.logger.info(
                f"Entity parsing complete (attempt {attempt}): "
                f"{valid_entities}/{total_entities} valid, {invalid_entities} skipped"
            )

            all: tuple[list[Entity], list[Entity]] = entities, skipped_entities

            return all

        except (ValueError, ValidationError, KeyError, json.JSONDecodeError) as e:
            # Log full response for debugging
            self.logger.error(
                f"Failed to parse LLM response (attempt {attempt}): {e}")
            self.logger.debug(f"Full LLM response:\n{response}")

            # Raise with detailed error but don't truncate
            error_msg = (
                f"Failed to parse LLM response as valid entities. "
                f"Error: {str(e)}. "
                f"Response length: {len(response)} chars. "
                f"Response preview: {response[:500]}..."
            )

            if skipped_entities:
                error_msg += f"\n\nSkipped {len(skipped_entities)} invalid entities"

            raise ValueError(error_msg) from e

    def _build_mappings(self, entities: List[Entity]) -> Dict[str, str]:
        """Build mappings from original values to placeholders.

        Args:
            entities: List of detected entities

        Returns:
            Dictionary mapping original values to placeholders
        """
        mappings = {}
        counters = {"NAME": 0, "EMAIL": 0,
                    "PHONE": 0, "ADDRESS": 0, "OTHER": 0}

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
