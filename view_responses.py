import storage
import argparse
from datetime import datetime

def format_timestamp(timestamp_str):
    """Format an ISO timestamp string into a readable format."""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

def list_responses():
    """List all stored responses with basic information."""
    responses = storage.load_responses()
    
    if not responses:
        print("No responses found in storage.")
        return
    
    print(f"Found {len(responses)} stored responses:\n")
    
    for i, response in enumerate(responses):
        timestamp = format_timestamp(response.get("timestamp", "Unknown"))
        scenario_id = response.get("scenario_id", "Unknown")
        
        # Get word counts
        openai_words = response.get("responses", {}).get("openai", {}).get("word_count", "N/A")
        anthropic_words = response.get("responses", {}).get("anthropic", {}).get("word_count", "N/A")
        gemini_words = response.get("responses", {}).get("gemini", {}).get("word_count", "N/A")
        
        print(f"Response #{i+1} - Scenario {scenario_id} - {timestamp}")
        print(f"  Word counts: OpenAI: {openai_words}, Anthropic: {anthropic_words}, Gemini: {gemini_words}")
        print()

def view_response(response_id):
    """View a specific response in detail."""
    # Adjust for 1-based indexing in display vs 0-based in storage
    response = storage.get_response_by_id(response_id - 1)
    
    if not response:
        print(f"Response #{response_id} not found.")
        return
    
    timestamp = format_timestamp(response.get("timestamp", "Unknown"))
    scenario_id = response.get("scenario_id", "Unknown")
    scenario_text = response.get("scenario_text", "Unknown")
    
    print(f"Response #{response_id} - Scenario {scenario_id} - {timestamp}\n")
    print("SCENARIO:")
    print("="*50)
    print(scenario_text)
    print("\n")
    
    # Print each model's response
    for model_name in ["openai", "anthropic", "gemini"]:
        model_response = response.get("responses", {}).get(model_name, {})
        model_text = model_response.get("output_text", "No response available")
        model_words = model_response.get("word_count", "N/A")
        
        print(f"{model_name.upper()} RESPONSE: ({model_words} words)")
        print("="*50)
        print(model_text)
        print("\n")

def main():
    parser = argparse.ArgumentParser(description="View stored AI responses")
    parser.add_argument("-l", "--list", action="store_true", help="List all stored responses")
    parser.add_argument("-v", "--view", type=int, help="View a specific response by ID")
    parser.add_argument("-s", "--scenario", type=int, help="List responses for a specific scenario")
    
    args = parser.parse_args()
    
    if args.list:
        list_responses()
    elif args.view:
        view_response(args.view)
    elif args.scenario:
        responses = storage.get_responses_by_scenario(args.scenario)
        if not responses:
            print(f"No responses found for scenario {args.scenario}.")
        else:
            print(f"Found {len(responses)} responses for scenario {args.scenario}:\n")
            for i, response in enumerate(responses):
                timestamp = format_timestamp(response.get("timestamp", "Unknown"))
                print(f"Response #{i+1} - {timestamp}")
                # You could add more details here if needed
            print("\nUse --view <id> to see a specific response.")
    else:
        # Default to listing if no arguments provided
        list_responses()

if __name__ == "__main__":
    main() 