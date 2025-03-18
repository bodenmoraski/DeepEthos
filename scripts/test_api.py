"""
Simple test script to verify that our API calls are working correctly.
"""

import api
import sys

def test_apis():
    """Test all three API calls with a simple prompt."""
    
    # Simple test prompt
    test_prompt = "Explain the concept of artificial intelligence in one paragraph."
    
    print("=" * 80)
    print("TESTING API CONNECTIONS")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    print("-" * 80)
    
    # Test OpenAI
    print("\nTesting OpenAI API...")
    try:
        openai_response = api.generate_openai_response(test_prompt)
        word_count = len(openai_response.split())
        print(f"✅ OpenAI Response ({word_count} words):")
        print("-" * 40)
        print(openai_response)
    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Test Anthropic
    print("Testing Anthropic API...")
    try:
        anthropic_response = api.generate_anthropic_response(test_prompt)
        word_count = len(anthropic_response.split())
        if "Error" in anthropic_response:
            print(f"❌ Anthropic API Error: {anthropic_response}")
        else:
            print(f"✅ Anthropic Response ({word_count} words):")
            print("-" * 40)
            print(anthropic_response)
    except Exception as e:
        print(f"❌ Anthropic API Error: {str(e)}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Test Gemini
    print("Testing Google Gemini API...")
    try:
        gemini_response = api.generate_gemini_response(test_prompt)
        word_count = len(gemini_response.split())
        if "Error" in gemini_response or "No suitable" in gemini_response:
            print(f"❌ Gemini API Error: {gemini_response}")
        else:
            print(f"✅ Gemini Response ({word_count} words):")
            print("-" * 40)
            print(gemini_response)
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    test_apis() 