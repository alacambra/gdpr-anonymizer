#!/usr/bin/env python3
"""
Demo script for GDPR Anonymization System - Iteration 1
Run this to see anonymization in action.
"""

import sys
import os

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from anonymization import anonymize_simple
from examples.sample_texts import ALL_EXAMPLES


def print_separator() -> None:
    """Print a visual separator line."""
    print("\n" + "=" * 80 + "\n")


def print_result(title: str, text: str) -> None:
    """Display anonymization results in a clear format."""
    print(f"📋 {title}")
    print("-" * 80)

    try:
        result = anonymize_simple(text)

        print("\n🔍 ORIGINAL TEXT:")
        print(text)

        print("\n✅ ANONYMIZED TEXT:")
        print(result.anonymized_text)

        print("\n🔑 MAPPINGS:")
        if result.mappings:
            for original, placeholder in result.mappings.items():
                print(f"  {original:40} → {placeholder}")
        else:
            print("  (No personal data found)")

        print_separator()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print_separator()
        sys.exit(1)


def main() -> None:
    """Run the demo script with all examples."""
    print_separator()
    print("🛡️  GDPR TEXT ANONYMIZATION SYSTEM - ITERATION 1")
    print("   Minimal Proof-of-Concept Demo")
    print_separator()

    # Run all examples
    for title, text in ALL_EXAMPLES:
        print_result(title, text)

    print("✨ Demo completed successfully!")
    print("\nTo use in your code:")
    print("  from anonymization import anonymize_simple")
    print("  result = anonymize_simple('Your text here')")
    print("  print(result.anonymized_text)")
    print()


if __name__ == "__main__":
    main()
