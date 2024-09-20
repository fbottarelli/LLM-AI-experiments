import gradio as gr
from common.llm import LLM
from common.vector_db import VectorDB
from subapps.chatbot import chatbot_interface
from subapps.chatbot_vector import chatbot_with_vector_interface
from subapps.langgraph_agents import langgraph_agents_interface

def main():
    # Initialize common resources
    llm = LLM(api_key="YOUR_OPENAI_API_KEY")
    vector_db = VectorDB(dimension=768)  # Ensure dimension matches your embedding model

    # Create interfaces for each subapp
    chatbot = chatbot_interface(llm)
    upload, chatbot_vector = chatbot_with_vector_interface(llm, vector_db)
    langgraph = langgraph_agents_interface(llm)

    # Main menu
    with gr.Blocks() as demo:
        gr.Markdown("# Modular Application with Gradio")
        with gr.Tab("Normal Chatbot"):
            chatbot.launch(share=False, inline=True)
        with gr.Tab("Chatbot with Vector Database"):
            upload.render()
            chatbot_vector.launch(share=False, inline=True)
        with gr.Tab("LangGraph with Agents"):
            langgraph.launch(share=False, inline=True)

    demo.launch()

if __name__ == "__main__":
    main()