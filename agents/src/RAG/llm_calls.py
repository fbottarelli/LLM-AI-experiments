from openai import OpenAI
import os
import litellm
import dotenv

dotenv.load_dotenv()


available_models = ["openai/gpt-4o-mini", "openai/gpt-4o", "qwen/qwen-2.5-72b-instruct"]
litellm_models = ["bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0", "bedrock/anthropic.claude-3-haiku-20240307-v1:0"]

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


def llm_unified(query: str, model: str, docs_list: list[docs_input] = None, images_list: list[images_input] = None):

    retrieved_docs = []

    messages = [
        {"role": "system", "content": "You are a helpful assistant. You will be provided with a query"}
    ]

    if images_list:
        messages[0]["content"] += ", one or more images"
        messages.extend([
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image.page_content}"
                }
            } for image in images_list
        ])

    if docs_list:
        messages[0]["content"] += ", and context extracted from documents"
        context = docs_to_context(docs_list)
        messages.append({"role": "user", "content": f"Here is the context: {context}"})

    messages[0]["content"] += ". You will need to answer the query and use the provided information to help you answer if needed."
    messages.append({"role": "user", "content": f"Here is the query: {query}"})

    response = litellm.completion(
        model=model,
        messages=messages,
        temperature=0.2,
        stream=True
    )
    
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
