

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_openai_response(prompt: str) -> str:
    """
    Generate a response using OpenAI's API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    try:
        from openai import OpenAI
        
        # Initialize the client
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a more widely available model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except ImportError:
        return "Error: OpenAI package not installed. Install with 'pip install openai'"
    except Exception as e:
        return f"Error generating OpenAI response: {str(e)}"

def generate_anthropic_response(prompt: str) -> str:
    """
    Generate a response using Anthropic's API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    # Due to compatibility issues with the current Anthropic client version,
    # we'll use a simpler approach with requests
    try:
        import requests
        import json
        
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            response_json = response.json()
            if "content" in response_json and len(response_json["content"]) > 0:
                return response_json["content"][0]["text"]
            else:
                return "No content in Anthropic response"
        else:
            return f"Anthropic API error: {response.status_code} - {response.text}"
            
    except ImportError:
        return "Error: Requests package not installed. Install with 'pip install requests'"
    except Exception as e:
        return f"Error generating Anthropic response: {str(e)}"

def generate_gemini_response(prompt: str) -> str:
    """
    Generate a response using Google's Gemini API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    try:
        import requests
        import json
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            if "candidates" in response_json and len(response_json["candidates"]) > 0:
                if "content" in response_json["candidates"][0]:
                    content = response_json["candidates"][0]["content"]
                    if "parts" in content and len(content["parts"]) > 0:
                        return content["parts"][0]["text"]
            
            return "No content in Gemini response"
        else:
            return f"Gemini API error: {response.status_code} - {response.text}"
            
    except ImportError:
        return "Error: Requests package not installed. Install with 'pip install requests'"
    except Exception as e:
        return f"Error generating Gemini response: {str(e)}"

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
        "model": "GPT-3.5 Turbo",
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
        "model": "Claude 3 Haiku",
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





