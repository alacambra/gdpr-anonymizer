#!/bin/bash

echo "Testing LLM Provider Info in API Response"
echo "=========================================="
echo ""

echo "Sending request to anonymize endpoint..."
echo ""

curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact John Smith at john@email.com or call 555-1234"
  }' | python -m json.tool | grep -A 2 "llm"

echo ""
echo ""
echo "Full response:"
echo ""

curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact John Smith at john@email.com"
  }' | python -m json.tool
