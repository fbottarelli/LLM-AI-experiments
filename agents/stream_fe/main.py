import streamlit as st

st.set_page_config(page_title="Agent Experiment", page_icon="🧪")

st.write("# Welcome to the Agent Experiment! 🧪")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This multi-page app allows you to experiment with different AI agents and models.
    
    ### Pages:
    - **Home**: This welcome page
    - **Chat**: Interact with the AI agent
    - **Model Selection**: Choose the AI model to use
    
    Select a page from the sidebar to get started!
    """
)