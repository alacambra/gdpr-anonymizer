#!/usr/bin/env python3
"""Simple tests for Pydantic validation and error handling.

Tests:
1. Valid LLM response - should pass validation
2. Invalid LLM response (wrong structure) - should fail validation and return error
"""

from pydantic import ValidationError

# Import the validation models
import sys
sys.path.insert(0, 'src')

from anonymization.infrastructure.agents.agent1_anon_exec import (
    LLMEntityResponse,
    LLMEntitiesListResponse
)
from anonymization.interfaces.rest.schemas.responses import AnonymizeResponse


def assert_raises(exception_type, func):
    """Simple assert raises helper."""
    try:
        func()
        raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
    except exception_type:
        return True


class TestPydanticValidation:
    """Test Pydantic validation for LLM responses."""

    def test_valid_entity_response(self):
        """Test that valid entity passes validation."""
        # Valid entity with correct structure
        valid_data = {
            "type": "NAME",
            "value": "John Smith"
        }

        # Should not raise exception
        entity = LLMEntityResponse(**valid_data)

        assert entity.type == "NAME"
        assert entity.value == "John Smith"
        print("✅ Valid entity passed validation")

    def test_invalid_entity_missing_type(self):
        """Test that entity without 'type' field fails validation."""
        # Invalid entity - missing 'type'
        invalid_data = {
            "procedure_date": "2024",
            "intervention_details": []
        }

        # Should raise ValidationError
        try:
            LLMEntityResponse(**invalid_data)
            raise AssertionError("Expected ValidationError but none was raised")
        except ValidationError as e:
            # Check that error mentions missing 'type'
            error_str = str(e)
            assert "type" in error_str.lower()
            print(f"✅ Invalid entity correctly rejected: {error_str[:100]}")

    def test_invalid_entity_missing_value(self):
        """Test that entity without 'value' field fails validation."""
        # Invalid entity - has type but no value
        invalid_data = {
            "type": "NAME"
            # missing 'value'
        }

        # Should raise ValidationError
        try:
            LLMEntityResponse(**invalid_data)
            raise AssertionError("Expected ValidationError but none was raised")
        except ValidationError as e:
            error_str = str(e)
            assert "value" in error_str.lower()
            print(f"✅ Invalid entity correctly rejected: {error_str[:100]}")

    def test_invalid_entity_type_value(self):
        """Test that entity with invalid type value fails validation."""
        # Invalid entity - type not in allowed list
        invalid_data = {
            "type": "INVALID_TYPE_XYZ",
            "value": "some value"
        }

        # Should raise ValidationError
        try:
            LLMEntityResponse(**invalid_data)
            raise AssertionError("Expected ValidationError but none was raised")
        except ValidationError as e:
            error_str = str(e)
            assert "invalid entity type" in error_str.lower()
            print(f"✅ Invalid type correctly rejected: {error_str[:100]}")

    def test_valid_entities_list(self):
        """Test that valid list of entities passes validation."""
        # Valid list
        valid_list = [
            {"type": "NAME", "value": "John Smith"},
            {"type": "EMAIL", "value": "john@example.com"},
            {"type": "PHONE", "value": "123-456-7890"}
        ]

        # Should not raise exception
        entities_list = LLMEntitiesListResponse(entities=valid_list)

        assert len(entities_list.entities) == 3
        assert entities_list.entities[0].type == "NAME"
        print("✅ Valid entities list passed validation")


class TestErrorResponseSchema:
    """Test that AnonymizeResponse schema includes error field."""

    def test_success_response_no_error(self):
        """Test successful response has error=None."""
        from datetime import datetime

        response = AnonymizeResponse(
            document_id="test-123",
            anonymized_text="Contact [NAME_1]",
            mappings={"John": "[NAME_1]"},
            validation={
                "passed": True,
                "issues": [],
                "reasoning": "All good",
                "confidence": 1.0,
            },
            risk_assessment={
                "overall_score": 95,
                "risk_level": "LOW",
                "gdpr_compliant": True,
                "confidence": 0.95,
                "reasoning": "Properly anonymized",
                "assessment_date": datetime.now()
            },
            iterations=1,
            success=True,
            llm_provider="claude",
            llm_model="claude-3-5-sonnet",
            error=None  # No error on success
        )

        assert response.success is True
        assert response.error is None
        assert response.anonymized_text == "Contact [NAME_1]"
        print("✅ Success response has error=None")

    def test_failure_response_with_error(self):
        """Test failure response includes error message."""
        from datetime import datetime

        error_message = "No valid entities found in LLM response"

        response = AnonymizeResponse(
            document_id="test-456",
            anonymized_text="",  # Empty on failure
            mappings={},
            validation={
                "passed": False,
                "issues": [],
                "reasoning": f"Parsing error: {error_message}",
                "confidence": 0.0
            },
            risk_assessment={
                "overall_score": 25,
                "risk_level": "CRITICAL",
                "gdpr_compliant": False,
                "confidence": 0.0,
                "reasoning": "Cannot assess risk due to parsing failure",
                "assessment_date": datetime.now()  # Use current datetime instead of None
            },
            iterations=0,
            success=False,
            llm_provider="claude",
            llm_model="claude-3-5-sonnet",
            error=error_message  # Error populated on failure
        )

        assert response.success is False
        assert response.error == error_message
        assert response.anonymized_text == ""
        assert response.mappings == {}
        print(f"✅ Failure response has error: '{response.error}'")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Running Pydantic Validation Tests")
    print("="*80 + "\n")

    # Run tests manually
    test_validation = TestPydanticValidation()
    test_errors = TestErrorResponseSchema()

    tests_run = 0
    tests_passed = 0

    # Test 1
    try:
        print("\n[Test 1/7] Valid entity response...")
        test_validation.test_valid_entity_response()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    # Test 2
    try:
        print("\n[Test 2/7] Invalid entity missing type...")
        test_validation.test_invalid_entity_missing_type()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    # Test 3
    try:
        print("\n[Test 3/7] Invalid entity missing value...")
        test_validation.test_invalid_entity_missing_value()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    # Test 4
    try:
        print("\n[Test 4/7] Invalid entity type value...")
        test_validation.test_invalid_entity_type_value()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    # Test 5
    try:
        print("\n[Test 5/7] Valid entities list...")
        test_validation.test_valid_entities_list()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    # Test 6
    try:
        print("\n[Test 6/7] Success response no error...")
        test_errors.test_success_response_no_error()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    # Test 7
    try:
        print("\n[Test 7/7] Failure response with error...")
        test_errors.test_failure_response_with_error()
        tests_passed += 1
    except Exception as e:
        print(f"❌ FAILED: {e}")
    tests_run += 1

    print("\n" + "="*80)
    print(f"Results: {tests_passed}/{tests_run} tests passed")
    print("="*80 + "\n")

    if tests_passed == tests_run:
        print("✅ All tests passed!")
        exit(0)
    else:
        print(f"❌ {tests_run - tests_passed} test(s) failed")
        exit(1)
