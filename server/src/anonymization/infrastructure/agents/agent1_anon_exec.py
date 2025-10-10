"""Agent 1 Implementation - Entity Anonymization (ANON-EXEC).

Migrated from simple.py - maintains exact same logic.
"""

import json
from typing import Dict, List
from pydantic import ValidationError

from ...domain.models import Entity, EntityType, AnonymizationMapping
from ...domain.ports import ILLMProvider
from ...domain.agents.prompts import AGENT1_ENTITY_IDENTIFICATION_PROMPT


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

    async def anonymize(self, text: str) -> AnonymizationMapping:
        """Identify and replace personal data entities in text.

        Args:
            text: Original text to anonymize

        Returns:
            AnonymizationMapping with replacements and entity list

        Raises:
            ValueError: If entity parsing fails
        """
        # Handle empty input
        if not text.strip():
            return AnonymizationMapping(
                original_text=text,
                anonymized_text=text,
                mappings={},
                entities=[]
            )

        # Generate prompt and call LLM
        prompt = AGENT1_ENTITY_IDENTIFICATION_PROMPT(text)
        response = await self.llm.generate(prompt)

        # Parse entities from response
        entities = self._parse_entities(response)

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

    def _parse_entities(self, response: str) -> List[Entity]:
        """Parse entity list from LLM JSON response.

        Args:
            response: LLM response containing JSON array

        Returns:
            List of Entity objects

        Raises:
            ValueError: If response cannot be parsed
        """
        try:
            # Find JSON array in response
            start = response.find('[')
            end = response.rfind(']') + 1

            if start == -1 or end <= start:
                return []

            json_str = response[start:end]
            data = json.loads(json_str)

            # Convert to Entity objects
            entities = []
            for item in data:
                entity = Entity(
                    type=EntityType(item["type"]),
                    value=item["value"]
                )
                entities.append(entity)

            return entities

        except (ValueError, ValidationError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(
                f"Failed to parse LLM response as valid entities. "
                f"Response excerpt: {response[:200]}"
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
