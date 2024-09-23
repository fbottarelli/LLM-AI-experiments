from openai import OpenAI
import os
# prompt 
import ell

# langsmith
from langsmith import traceable


# Initialize OpenAI client with base URL and API key
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  # Get API key from environment variable
)

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Get API key from environment variable
)

ell.init()

@traceable
@ell.simple(model="gpt-4o-mini", temperature=0.2, client=openrouter_client)
def llm_summarize(text: str):
    return [
        ell.system("You are a helpful assistant."),
        ell.user(f"Summarize the following document: {text}"),
        ell.user(text)
    ]

@traceable
@ell.simple(model="gpt-4o-mini", temperature=0.2, client=openrouter_client)
def llm_generic(query: str):
    return [
        ell.system("You are a helpful assistant."),
        ell.user(query)
    ]



# Normal openai calls

@traceable
def llm_generic_openai(query: str):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content