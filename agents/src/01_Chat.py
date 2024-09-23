from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from RAG.llm_calls import llm_generic

load_dotenv()

st.title("Chat with AI Agent")


# Initialize OpenAI client with base URL and API key
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  # Get API key from environment variable
)
# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
# )
available_models = ["openai/gpt-4o-mini", "openai/gpt-4o", "qwen/qwen-2.5-72b-instruct"]


def lstr_to_generator(lstr_instance):
    for char in lstr_instance:
        yield char



def handle_messages():

    # Add sidebar for model selection
    with st.sidebar:
        st.header("Model Selection")  # Sidebar header
        selected_model = st.selectbox("Choose a model:", available_models)  # Dropdown for model selection
        st.session_state["model"] = selected_model  # Update selected model in session state
                

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Capture user input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = llm_generic(prompt, client=openrouter_client, api_params=dict(model=st.session_state["model"], temperature=0.2))
            response = st.write_stream(lstr_to_generator(stream))
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add a delete button to clear messages
    if st.button("Delete Messages"):
        st.session_state.messages = []  # Clear the messages

handle_messages()
