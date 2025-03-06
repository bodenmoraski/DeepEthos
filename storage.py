import os
import json
import datetime
from typing import Dict, Any, List

# Define the path for our storage file
STORAGE_DIR = "responses"
STORAGE_FILE = os.path.join(STORAGE_DIR, "ai_responses.json")

def ensure_storage_exists():
    """
    Ensure that the storage directory and file exist.
    Creates them if they don't exist.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    
    # Create the file if it doesn't exist
    if not os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'w') as f:
            json.dump([], f)

def load_responses() -> List[Dict[str, Any]]:
    """
    Load all stored responses from the JSON file.
    
    Returns:
        A list of response dictionaries
    """
    ensure_storage_exists()
    
    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file is empty or invalid JSON, return an empty list
        return []

def save_response(scenario_id: int, scenario_text: str, openai_response: Dict[str, Any], 
                 anthropic_response: Dict[str, Any], gemini_response: Dict[str, Any]):
    """
    Save a new set of responses to the storage file.
    
    Args:
        scenario_id: The ID of the scenario
        scenario_text: The text of the scenario
        openai_response: The response from OpenAI
        anthropic_response: The response from Anthropic
        gemini_response: The response from Gemini
    """
    # Load existing responses
    responses = load_responses()
    
    # Create a new response entry
    new_response = {
        "timestamp": datetime.datetime.now().isoformat(),
        "scenario_id": scenario_id,
        "scenario_text": scenario_text,
        "responses": {
            "openai": openai_response,
            "anthropic": anthropic_response,
            "gemini": gemini_response
        }
    }
    
    # Add the new response to the list
    responses.append(new_response)
    
    # Save the updated list back to the file
    ensure_storage_exists()
    with open(STORAGE_FILE, 'w') as f:
        json.dump(responses, f, indent=2)
    
    print(f"Responses saved to {STORAGE_FILE}")

def get_response_by_id(response_id: int) -> Dict[str, Any]:
    """
    Get a specific response by its index in the storage.
    
    Args:
        response_id: The index of the response to retrieve
        
    Returns:
        The response dictionary or None if not found
    """
    responses = load_responses()
    
    if 0 <= response_id < len(responses):
        return responses[response_id]
    else:
        return None

def get_responses_by_scenario(scenario_id: int) -> List[Dict[str, Any]]:
    """
    Get all responses for a specific scenario.
    
    Args:
        scenario_id: The ID of the scenario
        
    Returns:
        A list of response dictionaries for the scenario
    """
    responses = load_responses()
    
    return [r for r in responses if r["scenario_id"] == scenario_id]

def get_response_count() -> int:
    """
    Get the total number of stored responses.
    
    Returns:
        The number of responses
    """
    return len(load_responses()) 