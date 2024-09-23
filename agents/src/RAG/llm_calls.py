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

available_models = ["openai/gpt-4o-mini", "openai/gpt-4o", "qwen/qwen-2.5-72b-instruct"]


# Normal openai calls
from typing import Dict
class docs_input(Dict):
    page_content: str
    metadata: Dict

class images_input(Dict):
    page_content: str
    metadata: Dict



def docs_to_context(docs_list: list[docs_input]):
    return "\n".join([f"Here is the page content: {doc.page_content}" for doc in docs_list])



@traceable
def llm_generic_openai(query: str, model: str, client: OpenAI):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        temperature=0.2,
        stream=True
    )
    return response

@traceable
def llm_rag_openai(query: str, docs_list: list[docs_input], model: str, client: OpenAI):
    context = docs_to_context(docs_list)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You will be provided with a query and a context. You will need to answer the query and use the context to help you answer the query if needed."},
            {"role": "user", "content": f"Here is the context: {context}"},
            {"role": "user", "content": f"Here is the query: {query}"},
        ],
        temperature=0.2,
        stream=True
    )
    return response


@traceable
def llm_vision_openai(query: str, images_list: images_input, model: str, client: OpenAI):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You will be provided with an image and a query. You will need to answer the query and use the image to help you answer the query if needed."},
            # Add images
            ({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
            },} for base64_image in images_list),
            # Add query
            {"role": "user", "content": f"Here is the query: {query}"},
        ],
        temperature=0.2,
        stream=True
    )
    return response


@traceable  
def llm_rag_vision_openai(query: str, images_list: images_input, docs_list: list[docs_input], model: str, client: OpenAI):
    context = docs_to_context(docs_list)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You will be provided with a query, one or more images, and a context extracted from documents. You will need to answer the query and use the images and context to help you answer the query if needed."},
            # Add images
            ({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
            },} for base64_image in images_list),
            # Add context
            {"role": "user", "content": f"Here is the context: {context}"},
            # Add query
            {"role": "user", "content": f"Here is the query: {query}"}
        ],
        temperature=0.2,
        stream=True
    )
    return response
