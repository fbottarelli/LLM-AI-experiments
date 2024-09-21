from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
# qdrant
from qdrant_client import QdrantClient


load_dotenv()

st.title("Chat with AI Agent")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# List of available models
available_models = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    # Add more models as needed
]

def handle_messages():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = available_models[0]  # Default model

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
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add a delete button to clear messages
    if st.button("Delete Messages"):
        st.session_state.messages = []  # Clear the messages

    # Add sidebar for model selection
    with st.sidebar:
        st.header("Model Selection")
        selected_model = st.selectbox("Choose a model:", available_models, index=available_models.index(st.session_state["openai_model"]))
        st.session_state["openai_model"] = selected_model

handle_messages()