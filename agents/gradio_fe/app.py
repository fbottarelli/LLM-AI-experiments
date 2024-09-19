from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url=os.getenv("OPENROUTER_API_URL"))

# List of available models
available_models = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "openai/gpt-3.5-turbo",
    # Add more models as needed
]

def predict(message, history, model):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history_openai_format,
        temperature=1.0,
        stream=True
    )

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

# Create the Gradio interface with a model selector
with gr.Blocks(theme="soft") as demo:
    model_selector = gr.Dropdown(choices=available_models, value=available_models[0], label="Select Model")
    chat_interface = gr.ChatInterface(predict, 
                                      additional_inputs=[model_selector],
                                    #   multimodal=True,
                                      chatbot=gr.Chatbot(height=650),
                                      textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7),)

demo.launch()
