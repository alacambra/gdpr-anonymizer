"""
Sample texts for testing anonymization - Iteration 1
"""

SIMPLE_CUSTOMER_SUPPORT = """Customer John Smith (john.smith@email.com, 555-123-4567) reported an issue with his account. He lives at 123 Main Street, Springfield."""

MULTIPLE_PEOPLE_TEAM = """Our team consists of Sarah Johnson (sarah.j@company.com) from the New York office and Mike Chen (mike.chen@company.com, +1-415-555-9876) from San Francisco. Sarah can also be reached at 212-555-3344."""

REAL_WORLD_MEETING = """Meeting scheduled for next Tuesday with Dr. Emily Rodriguez at her office located at 456 Oak Avenue, Boston MA. Please confirm attendance by emailing emily.rodriguez@hospital.org or calling (617) 555-7890. Emily mentioned she'll bring documents from the last consultation."""

WITH_OTHER_ENTITIES = """Patient ID: #PAT-98765 was seen on 2024-03-15. Account number ACC-445566 needs verification. The insurance policy number is INS-2024-XY789. Transaction reference: TXN-20240315-001."""

ALL_EXAMPLES = [
    ("Simple Customer Support", SIMPLE_CUSTOMER_SUPPORT),
    ("Multiple People - Team", MULTIPLE_PEOPLE_TEAM),
    ("Real-World Meeting Notes", REAL_WORLD_MEETING),
    ("With Other Entity Types", WITH_OTHER_ENTITIES),
]
