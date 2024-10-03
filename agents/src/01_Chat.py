from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from RAG.llm_calls import llm_unified
from RAG.llm_calls import docs_input, images_input
from RAG.ingestion import gateway_ingestion, encode_image
load_dotenv()
from io import StringIO
import litellm

st.title("Chat with AI Agent")

# Initialize LiteLLM client
litellm_client = litellm.completion

# Update available models (you may need to adjust this list based on your LiteLLM setup)
available_models = ["gpt-4o", "gpt-4o-mini"]  # Update with models supported by your LiteLLM setup

def lstr_to_generator(lstr_instance):
    for char in lstr_instance:
        yield char

def handle_messages():
    # Initialize session state variables
    if "add_context" not in st.session_state:
        st.session_state["add_context"] = False
    if "doc_list" not in st.session_state:
        st.session_state["doc_list"] = None
    if "image_list" not in st.session_state:
        st.session_state["image_list"] = None

    # Add sidebar for model selection and context options
    with st.sidebar:
        st.header("Model Selection")
        selected_model = st.selectbox("Choose a model:", available_models)
        st.session_state["model"] = selected_model

        # Context adding option
        add_context = st.radio("Add context to prompt?", ("Yes", "No"))
        st.session_state["add_context"] = add_context == "Yes"

        # Upload file
        if st.session_state["add_context"]:
            uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["pdf", "txt", "md", "jpeg", "png"])
            if uploaded_files:
                st.session_state["doc_list"] = []
                st.session_state["image_list"] = []
                
                for file in uploaded_files:
                    if file.name.endswith((".pdf", ".txt", ".md")):
                        st.write(f"Current file: {file.name}")
                        st.session_state["doc_list"].append(docs_input(page_content=(StringIO(file.getvalue().decode("utf-8")).read()), metadata={"source": file.name}))
                    elif file.name.endswith((".jpeg", ".png")):
                        st.session_state["image_list"].append(images_input(page_content=encode_image(file), metadata={"source": file.name}))
                
                if not st.session_state["doc_list"]:
                    st.session_state["doc_list"] = None
                if not st.session_state["image_list"]:
                    st.session_state["image_list"] = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Capture user input
    if query := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            stream = llm_unified(
                query=query,
                model=st.session_state["model"],
                docs_list=st.session_state["doc_list"],
                images_list=st.session_state["image_list"]
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add a delete button to clear messages
    if st.button("Delete Messages"):
        st.session_state.messages = []  # Clear the messages

handle_messages()
