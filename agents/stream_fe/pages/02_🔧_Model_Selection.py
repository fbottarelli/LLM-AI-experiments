import streamlit as st

st.set_page_config(page_title="Model Selection", page_icon="🔧")

st.title("Model Selection")

models = [
    "openai/gpt-4-turbo-preview",
    "openai/gpt-3.5-turbo",
    "anthropic/claude-2",
    "google/palm-2-chat-bison",
    "meta-llama/llama-2-70b-chat",
]

selected_model = st.selectbox("Choose a model:", models)

if st.button("Save Selection"):
    st.session_state["openai_model"] = selected_model
    st.success(f"Model set to: {selected_model}")

st.write("Currently selected model:", st.session_state.get("openai_model", "Not set"))