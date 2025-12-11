#!/usr/bin/env python
"""Test transaction parsing"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot_service import parse_natural_language

test_cases = [
    "bought lunch 60 baht",
    "spent 100 baht on coffee",
    "got salary 15000",
    "bought dinner 200 baht yesterday",
    "lunch 50",
    "60 baht",
    "bought something for 75",
]

print("=" * 60)
print("Testing Transaction Parsing")
print("=" * 60)

for test_input in test_cases:
    print(f"\nInput: '{test_input}'")
    result = parse_natural_language(test_input, uid=None)
    print(f"  Type: {result.get('type')}")
    print(f"  Amount: {result.get('amount')}")
    print(f"  Category: {result.get('category')}")
    print(f"  Date: {result.get('date')}")
    print(f"  Time: {result.get('time')}")
    print(f"  Action: {result.get('action')}")
    if result.get('action'):
        print(f"  Message: {result.get('message', '')[:50]}")
    
    # Check if it's valid transaction data
    if result.get('type') and result.get('amount') and result.get('amount') > 0:
        print("  ✓ Valid transaction")
    elif result.get('action') == 'conversation':
        print("  ✓ Conversational response")
    elif result.get('action') == 'analyze':
        print("  ✓ Analysis request")
    else:
        print("  ✗ Invalid - missing type or amount")

print("\n" + "=" * 60)
