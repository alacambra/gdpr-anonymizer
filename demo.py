#!/usr/bin/env python3
"""
Demo script for GDPR Anonymization System - Iteration 3
Complete 3-Agent Workflow: Anonymization + Validation + Risk Assessment
"""

import sys
import os

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from anonymization import anonymize_simple, validate_anonymization, assess_risk
from examples.sample_texts import ALL_EXAMPLES


def print_separator() -> None:
    """Print a visual separator line."""
    print("\n" + "=" * 80 + "\n")


def print_result(title: str, text: str) -> None:
    """Display dual-agent anonymization and validation results."""
    print(f"📋 {title}")
    print("-" * 80)

    try:
        # Agent 1: Anonymization
        print("\n🤖 AGENT 1: ANONYMIZATION (ANON-EXEC)")
        print("-" * 40)
        anon_result = anonymize_simple(text)

        print("\n🔍 ORIGINAL TEXT:")
        print(text)

        print("\n✅ ANONYMIZED TEXT:")
        print(anon_result.anonymized_text)

        print("\n🔑 MAPPINGS:")
        if anon_result.mappings:
            for original, placeholder in anon_result.mappings.items():
                print(f"  {original:40} → {placeholder}")
        else:
            print("  (No personal data found)")

        # Agent 2: Validation
        print("\n\n🔎 AGENT 2: VERIFICATION (DIRECT-CHECK)")
        print("-" * 40)
        validation_result = validate_anonymization(anon_result.anonymized_text)

        if validation_result.passed:
            print("\n✅ VERIFICATION PASSED - No remaining identifiers detected")
            print(f"\n📝 Reasoning: {validation_result.agent_reasoning}")
            print(f"🎯 Confidence: {validation_result.confidence:.0%}")
        else:
            print(f"\n❌ VERIFICATION FAILED - Found {len(validation_result.issues)} remaining identifier(s)")
            print(f"\n📝 Reasoning: {validation_result.agent_reasoning}")
            print(f"🎯 Confidence: {validation_result.confidence:.0%}")

            print("\n⚠️  ISSUES FOUND:")
            for i, issue in enumerate(validation_result.issues, 1):
                print(f"\n  Issue {i}:")
                print(f"    Type:     {issue.identifier_type}")
                print(f"    Value:    {issue.value}")
                print(f"    Context:  {issue.context}")
                print(f"    Location: {issue.location_hint}")

        # Agent 3: Risk Assessment (only runs if Agent 2 passes)
        if validation_result.passed:
            print("\n\n📊 AGENT 3: RISK ASSESSMENT (RISK-ASSESS)")
            print("-" * 40)
            risk_result = assess_risk(anon_result.anonymized_text, anon_result.mappings)

            print(f"\nRisk Level:      {risk_result.risk_level}")
            print(f"Overall Score:   {risk_result.overall_score}/25")
            print(f"GDPR Compliant:  {'✅ YES' if risk_result.gdpr_compliant else '❌ NO'}")
            print(f"Confidence:      {risk_result.confidence:.0%}")

            print(f"\n📝 Assessment:")
            print(f"{risk_result.reasoning}")

            if risk_result.gdpr_compliant:
                print("\n✅ RECOMMENDATION: SAFE TO PUBLISH")
            else:
                print("\n⚠️  RECOMMENDATION: NOT SAFE TO PUBLISH")

        print_separator()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print_separator()
        sys.exit(1)


def main() -> None:
    """Run the complete 3-agent demo with all examples."""
    print_separator()
    print("🛡️  GDPR TEXT ANONYMIZATION SYSTEM - ITERATION 3")
    print("   Complete 3-Agent Workflow: Anonymization + Validation + Risk Assessment")
    print_separator()

    # Run all examples
    for title, text in ALL_EXAMPLES:
        print_result(title, text)

    print("✨ Complete 3-agent workflow executed successfully!")
    print("\nTo use in your code:")
    print("  from anonymization import anonymize_simple, validate_anonymization, assess_risk")
    print("  ")
    print("  # Agent 1: Anonymize")
    print("  result = anonymize_simple('Your text here')")
    print("  ")
    print("  # Agent 2: Validate")
    print("  validation = validate_anonymization(result.anonymized_text)")
    print("  ")
    print("  # Agent 3: Assess Risk (if validation passes)")
    print("  if validation.passed:")
    print("      risk = assess_risk(result.anonymized_text, result.mappings)")
    print("      if risk.gdpr_compliant:")
    print("          print('Safe to publish!')")
    print()


if __name__ == "__main__":
    main()
