import openai

class LLM:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate_response(self, prompt: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Replace with desired model
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()