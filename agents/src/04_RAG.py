from openai import OpenAI  # Import OpenAI client for chat completions
import streamlit as st  # Import Streamlit for web app interface
import os  # Import os for environment variable access
from dotenv import load_dotenv  # Import dotenv to load environment variables from .env file
# qdrant
from qdrant_client import QdrantClient  # Import Qdrant client for vector database interactions
from RAG.qdrant import list_collections
load_dotenv()  # Load environment variables from .env file

# LLM calls
from RAG.llm_calls import llm_summarize, llm_generic, llm_generic_openai
from RAG.ingestion import gateway_ingestion

st.title("Chat with AI Agent")  # Set the title of the Streamlit app


# List of available models for the AI agent
available_models = [
    "openai/gpt-4o-mini",  # Mini version of GPT-4
    "openai/gpt-4",  # Full version of GPT-4
    # Add more models as needed
]


def handle_messages():

    # Add sidebar for model selection
    with st.sidebar:
        st.header("Model Selection")  # Sidebar header
        selected_model = st.selectbox("Choose a model:", available_models)  # Dropdown for model selection
        st.session_state["model"] = selected_model  # Update selected model in session state
        # RAG
        qdrant_client = QdrantClient(host="localhost", port=6333)
        selected_collection = st.selectbox("Choose a collection:", list_collections(qdrant_client))  # Dropdown for model selection
        st.session_state["qdrant_collection"] = selected_collection  # Update selected model in session state
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])  # File uploader for various file types
        if uploaded_file:
            with st.spinner("Ingesting..."):
                etracted_text = gateway_ingestion(uploaded_file)
                # upload to qdrant
                qdrant_client.add(selected_collection, etracted_text)
                


    # Initialize messages in session state if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):  # Display message based on role (user/assistant)
            st.markdown(message["content"])  # Render message content

    # USER INPUT
    if prompt := st.chat_input("What is up?"):  # Prompt user for input
        st.session_state.messages.append({"role": "user", "content": prompt})  # Store user message
        with st.chat_message("user"):  # Display user message
            st.markdown(prompt)

        # ASSISTANT RESPONSE
        with st.chat_message("assistant"):  # Prepare to display assistant's response
            import time  # Import time module to measure execution time
            
            start_time_ell = time.time()  # Start timer for ell call
            with st.spinner("ell call"):
                stream = llm_generic(st.session_state.messages[-1]["content"])
                response = st.write(stream)  # Write the streamed response from ell
            ell_duration = time.time() - start_time_ell  # Calculate duration for ell call
            
            # Log the durations for comparison
            st.write(f"Ell call duration: {ell_duration:.2f} seconds")
            
            
        st.session_state.messages.append({"role": "assistant", "content": response})  # Store assistant's response
    if st.button("Delete Messages"):  # Button to clear chat history
        st.session_state.messages = []  # Clear the messages



handle_messages()  # Call the function to handle chat messages