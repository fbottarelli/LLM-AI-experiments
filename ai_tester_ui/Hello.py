import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    ## 🌟 AI Project Overview
    Welcome to our AI project hub! Here, we explore various cutting-edge technologies including Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and computer vision. Our user-friendly interface allows you to easily navigate through different tests and experiments, making it simple to order and visualize results. Dive in and discover the potential of AI!

    🌟 Select a demo in the left sidebar to get started! 🚀
"""
)