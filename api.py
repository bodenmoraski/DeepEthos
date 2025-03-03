import openai 
import anthropic
from google import genai
import os
from typing import Dict, Any, List

# Set API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize clients
google_client = genai.Client(api_key=gemini_api_key)
openai_client = openai.OpenAI(api_key=openai.api_key)
anthropic_client = anthropic.Anthropic(api_key=anthropic.api_key)

# Create a function to generate a response using the OpenAI API
def generate_openai_response(prompt: str) -> str:
    """
    Generate a response using OpenAI's API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Create a function to generate a response using the Anthropic API
def generate_anthropic_response(prompt: str) -> str:
    """
    Generate a response using Anthropic's API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response.content[0].text

# Create a function to generate a response using the Gemini API
def generate_gemini_response(prompt: str) -> str:
    """
    Generate a response using Google's Gemini API.
    
    Args:
        prompt: The input text to send to the model
    
    Returns:
        The model's response as a string
    """
    generation_config = {
        'temperature': 0.7,
        'max_output_tokens': 1000
    }
    
    response = google_client.generate_content(
        prompt,
        generation_config=generation_config
    )
    return response.text

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
        "model": "Claude 3.5 Sonnet",
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
        "model": "Gemini Pro",
        "provider": "Google",
        "input_text": input_text,
        "output_text": raw_response,
        "word_count": len(raw_response.split()),
        "character_count": len(raw_response)
    }





