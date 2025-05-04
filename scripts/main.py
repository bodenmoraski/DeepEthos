import prompts
import scripts.api as api
import storage
from scripts.api import format_openai_output, format_anthropic_output, format_gemini_output
from final_prompt import construct_prompt
from scenarios import get_scenario

def main():
    try:
        # Get the scenario (default to scenario 1)
        scenario_id = 1
        scenario = get_scenario(scenario_id)
        print(f"Using scenario: {scenario[:100]}...")
        
        # Construct the prompt
        prompt = construct_prompt(scenario)
        print(f"Prompt constructed successfully. Length: {len(prompt)} characters")
        
        # Get responses from different models
        print("\nGetting responses from models...")
        
        try:
            openai_response = format_openai_output(prompt)
            print(f"OpenAI response received. Word count: {openai_response['word_count']}")
        except Exception as e:
            print(f"Error getting OpenAI response: {e}")
            openai_response = {"error": str(e), "output_text": "Error generating response"}
        
        try:
            anthropic_response = format_anthropic_output(prompt)
            print(f"Anthropic response received. Word count: {anthropic_response['word_count']}")
        except Exception as e:
            print(f"Error getting Anthropic response: {e}")
            anthropic_response = {"error": str(e), "output_text": "Error generating response"}
        
        try:
            gemini_response = format_gemini_output(prompt)
            print(f"Gemini response received. Word count: {gemini_response['word_count']}")
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            gemini_response = {"error": str(e), "output_text": "Error generating response"}
        
        # Save the responses to storage
        storage.save_response(
            scenario_id=scenario_id,
            scenario_text=scenario,
            openai_response=openai_response,
            anthropic_response=anthropic_response,
            gemini_response=gemini_response
        )
        
        # Print a summary
        print("\nResponse Summary:")
        print(f"OpenAI: {openai_response.get('word_count', 'Error')} words")
        print(f"Anthropic: {anthropic_response.get('word_count', 'Error')} words")
        print(f"Gemini: {gemini_response.get('word_count', 'Error')} words")
        
        # Print the actual responses
        print("\n" + "="*50)
        print("OPENAI RESPONSE:")
        print("="*50)
        print(openai_response.get('output_text', 'No response available'))
        
        print("\n" + "="*50)
        print("ANTHROPIC RESPONSE:")
        print("="*50)
        print(anthropic_response.get('output_text', 'No response available'))
        
        print("\n" + "="*50)
        print("GEMINI RESPONSE:")
        print("="*50)
        print(gemini_response.get('output_text', 'No response available'))
        
        # Print storage information
        response_count = storage.get_response_count()
        print(f"\nTotal responses stored: {response_count}")
        
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()