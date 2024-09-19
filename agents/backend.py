# backend.py

from openai import OpenAI
from os import getenv

# Function to initialize OpenRouter client
def init_openrouter_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY")
    )

# Function to call OpenRouter API and get a response
def get_openrouter_response(user_message):
    client = init_openrouter_client()
    
    # Prepare conversation context
    messages = [{"role": "user", "content": user_message}]
    
    # Call OpenRouter API for chat completion
    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages
    )
    
    # Return the model's response
    return completion.choices[0].message.content
