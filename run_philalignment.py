#!/usr/bin/env python3
"""
Simple test script to verify imports
"""

import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Checking imports...")

try:
    # Try importing from code.providers
    from code.providers.multi_provider_integration import run_comparison, PROVIDERS, MODELS
    print("✅ Successfully imported from code.providers.multi_provider_integration")
except ImportError as e:
    print(f"❌ Failed to import from code.providers: {e}")
    try:
        # Try importing directly
        from code.multi_provider_integration import run_comparison, PROVIDERS, MODELS
        print("✅ Successfully imported from code.multi_provider_integration")
    except ImportError as e:
        print(f"❌ Failed to import from code.multi_provider_integration: {e}")

try:
    # Try importing from code.generation
    from code.generation.question_generator import generate_scenarios
    print("✅ Successfully imported from code.generation.question_generator")
except ImportError as e:
    print(f"❌ Failed to import from code.generation: {e}")
    try:
        # Try importing directly
        from code.question_generator import generate_scenarios
        print("✅ Successfully imported from code.question_generator")
    except ImportError as e:
        print(f"❌ Failed to import from code.question_generator: {e}")

print("\nScript completed.") 