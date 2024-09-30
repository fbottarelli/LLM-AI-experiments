from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from libs.RAG.llm_calls import llm_rag_openai, llm_rag_vision_openai, llm_generic_openai, llm_vision_openai 
from libs.RAG.llm_calls import docs_input, images_input
from libs.RAG.ingestion import gateway_ingestion, encode_image
from libs.RAG.embeddings import create_embeddings_openai, create_embeddings_bedrock
load_dotenv()
from io import StringIO

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

def RAG_sidebar():
    # Add sidebar for model selection
    with st.sidebar:
        st.header("Model Selection")  # Sidebar header
        selected_model = st.selectbox("Choose a model:", available_models)  # Dropdown for model selection
        st.session_state["model"] = selected_model  # Update selected model in session state
        
        # Context adding option
        add_context = st.radio("Add context to prompt?", ("Yes", "No"))
        st.session_state["add_context"] = add_context == "Yes"  # Store context adding preference in session state
        st.session_state["attachments"] = []

        # Upload file
        if st.session_state["add_context"]:
            uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["pdf", "txt", "md", "jpeg", "png"])
            if uploaded_files:
                st.session_state["has_docs"] = False
                st.session_state["has_images"] = False
                st.session_state["doc_list"] = []
                st.session_state["image_list"] = []
                
                for file in uploaded_files:
                    # st.session_state["attachments"].append(gateway_ingestion(file))
                    
                    if file.name.endswith((".pdf", ".txt", ".md")):
                        st.write(f"Current file: {file.name}")
                        st.session_state["has_docs"] = True
                        st.session_state["doc_list"].append(docs_input(page_content=(StringIO(file.getvalue().decode("utf-8")).read()), metadata={"source": file.name}))
                        st.write(f"Current case: {st.session_state['case']}")
                        st.write(f"Current doc_list: {st.session_state['doc_list']}")
                    elif file.name.endswith((".jpeg", ".png")):
                        st.session_state["has_images"] = True
                        st.session_state["image_list"].append(images_input(page_content=encode_image(file), metadata={"source": file.name}))
                
                # Determine the case based on uploaded files
                if st.session_state["has_docs"] and st.session_state["has_images"]:
                    st.session_state["case"] = "docs_and_images"
                elif st.session_state["has_docs"]:
                    st.session_state["case"] = "docs_only"
                elif st.session_state["has_images"]:
                    st.session_state["case"] = "images_only"
                else:
                    st.session_state["case"] = "no_context"
        else:
            st.session_state["case"] = "no_context"

def handle_messages():
    # Initialize the "case" key in session state if it doesn't exist
    if "case" not in st.session_state:
        st.session_state["case"] = "no_context"

    RAG_sidebar()

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
            if st.session_state["case"]:
                if st.session_state["case"] == "no_context":
                    stream = llm_generic_openai(query, st.session_state["model"], openrouter_client)
                elif st.session_state["case"] == "docs_only":
                    stream = llm_rag_openai(query, st.session_state["doc_list"], st.session_state["model"], openrouter_client)
                elif st.session_state["case"] == "images_only":
                    stream = llm_vision_openai(query, st.session_state["image_list"], st.session_state["model"], openrouter_client)
                elif st.session_state["case"] == "docs_and_images":
                    stream = llm_rag_vision_openai(query, st.session_state["image_list"], st.session_state["doc_list"], st.session_state["model"], openrouter_client)
                
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add a delete button to clear messages
    if st.button("Delete Messages"):
        st.session_state.messages = []  # Clear the messages

handle_messages()
