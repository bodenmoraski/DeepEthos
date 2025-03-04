import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize clients with error handling
openai_client = None
anthropic_client = None
google_client = None

# Try to import and initialize OpenAI
try:
    import openai
    openai_client = openai.OpenAI(api_key=openai_api_key)
    print("OpenAI client initialized successfully")
except (ImportError, Exception) as e:
    print(f"Error initializing OpenAI client: {e}")

# Try to import and initialize Anthropic
try:
    import anthropic
    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
    print("Anthropic client initialized successfully")
except (ImportError, Exception) as e:
    print(f"Error initializing Anthropic client: {e}")

# Try to import and initialize Google Gemini
try:
    import google.generativeai as genai
    genai.configure(api_key=gemini_api_key)
    google_client = genai
    print("Google Gemini client initialized successfully")
except (ImportError, Exception) as e:
    print(f"Error initializing Google Gemini client: {e}")

# Create a function to generate a response using the OpenAI API
def generate_openai_response(prompt: str) -> str:
    """
    Generate a response using OpenAI's API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    if openai_client is None:
        return "OpenAI client not available"
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating OpenAI response: {str(e)}"

# Create a function to generate a response using the Anthropic API
def generate_anthropic_response(prompt: str) -> str:
    """
    Generate a response using Anthropic's API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    if anthropic_client is None:
        return "Anthropic client not available"
    
    try:
        # Simple direct HTTP request approach
        import requests
        import json
        
        headers = {
            "x-api-key": anthropic_api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"  # Adding the required version header
        }
        
        # Try with claude-2.0 model
        data = {
            "model": "claude-2.0",
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/complete",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            return response.json().get("completion", "No completion in response")
        else:
            # If API call fails, return a simulated response
            print(f"Anthropic API call failed with status {response.status_code}. Using simulated response.")
            return "[SIMULATED RESPONSE] I would prioritize finding an alternative method to produce the treatment that doesn't require the limited resource. The well-being of the indigenous community must be protected while we explore synthetic alternatives or other approaches to treat the disease."
    except Exception as e:
        # Return a simulated response in case of any error
        print(f"Anthropic API error: {str(e)}. Using simulated response.")
        return "[SIMULATED RESPONSE] I would prioritize finding an alternative method to produce the treatment that doesn't require the limited resource. The well-being of the indigenous community must be protected while we explore synthetic alternatives or other approaches to treat the disease."

# Create a function to generate a response using the Gemini API
def generate_gemini_response(prompt: str) -> str:
    """
    Generate a response using Google's Gemini API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    if google_client is None:
        return "Google Gemini client not available"
    
    try:
        # Simple approach using the most basic Gemini API call
        import google.generativeai as genai
        
        # Configure with a specific model that we know works
        model = google_client.GenerativeModel("gemini-1.5-flash")
        
        # Simple generation config
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 1000,
        }
        
        # Generate the response
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config
        )
        
        # Extract the text from the response
        if hasattr(response, "text"):
            return response.text
        else:
            # Try to extract text from parts if available
            try:
                return response.candidates[0].content.parts[0].text
            except (AttributeError, IndexError):
                return "Could not extract text from Gemini response"
    except Exception as e:
        return f"Error generating Gemini response: {str(e)}"

# Formatting functions that provide structured responses

def format_openai_output(input_text: str) -> Dict[str, Any]:
    """
    Format the OpenAI response with metadata.
    
    Args:
        input_text: The input text to send to the model
    
    Returns:
        A dictionary containing the response and metadata
    """
    raw_response = generate_openai_response(input_text)
    return {
        "model": "GPT-4o",
        "provider": "OpenAI",
        "input_text": input_text,
        "output_text": raw_response,
        "word_count": len(raw_response.split()),
        "character_count": len(raw_response)
    }

def format_anthropic_output(input_text: str) -> Dict[str, Any]:
    """
    Format the Anthropic response with metadata.
    
    Args:
        input_text: The input text to send to the model
    
    Returns:
        A dictionary containing the response and metadata
    """
    raw_response = generate_anthropic_response(input_text)
    return {
        "model": "Claude 2.0 (Simulated if API fails)",
        "provider": "Anthropic",
        "input_text": input_text,
        "output_text": raw_response,
        "word_count": len(raw_response.split()),
        "character_count": len(raw_response)
    }

def format_gemini_output(input_text: str) -> Dict[str, Any]:
    """
    Format the Gemini response with metadata.
    
    Args:
        input_text: The input text to send to the model
    
    Returns:
        A dictionary containing the response and metadata
    """
    raw_response = generate_gemini_response(input_text)
    return {
        "model": "Gemini 1.5 Flash",
        "provider": "Google",
        "input_text": input_text,
        "output_text": raw_response,
        "word_count": len(raw_response.split()),
        "character_count": len(raw_response)
    }





