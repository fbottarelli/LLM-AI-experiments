import gradio as gr
from common.llm import LLM

def chatbot_interface(llm: LLM):
    def respond(user_input):
        response = llm.generate_response(user_input)
        return response

    iface = gr.Interface(
        fn=respond,
        inputs="text",
        outputs="text",
        title="Normal Chatbot",
        description="A simple chatbot that uses an LLM model to respond to user input."
    )
    return iface