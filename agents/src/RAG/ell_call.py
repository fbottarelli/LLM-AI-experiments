import ell

# langsmith
from langsmith import traceable


ell.init()
@traceable
@ell.simple(model="openai/gpt-4o-mini", temperature=0.2, client=openrouter_client)
def llm_summarize(text: str):
    return [
        ell.system("You are a helpful assistant."),
        ell.user(f"Summarize the following document: {text}"),
        ell.user(text)
    ]

@traceable
@ell.simple(model="openai/gpt-4o-mini", temperature=0.2, client=openrouter_client)
def llm_generic(query: str):
    return [
        ell.system("You are a helpful assistant."),
        ell.user(query)
    ]