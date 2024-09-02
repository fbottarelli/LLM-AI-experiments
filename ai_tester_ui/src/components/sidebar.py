import streamlit as st
from src.modules.tools.vectorstore import all_collections, delete_collection

@st.dialog("App Settings")
def system_settings():
    if "vectorstore" in st.session_state and st.session_state.vectorstore:
        st.slider("Top K results", min_value=1, max_value=10, value=4, key="top_k")
    col1, col2 = st.columns(2)
    col1.slider("Temperature", min_value=0.0, max_value=2.0, step=0.1, value=0.1, key="temperature")
    col2.slider("Max Tokens", min_value=0, max_value=8000, value=2500, key="max_tokens")
    collections = all_collections()
    st.subheader("Manage Documents")
    if len(collections):
        col1, col2, col3 = st.columns([4, 1, 1])
        collection_name = col1.selectbox("Select a document", collections, index=0, label_visibility="collapsed")
        if col2.button("➕", use_container_width=True):
            st.session_state.collection_name = collection_name
            st.session_state.vectorstore = True
            st.rerun()
        if col3.button("🗑️", use_container_width=True):
            delete_collection(collection_name)
            st.rerun()
    else:
        st.warning("No documents found")

# Function to display sidebar information and settings
def side_info():
    with st.sidebar:
        # Display the application title logo
        st.logo("src/assets/title.png", icon_image="src/assets/title.png", link="https://github.com/SSK-14")
        # Display the main logo
        st.image("src/assets/logo.png", use_column_width=True)
        # Display the header image
        st.image("src/assets/header.png", use_column_width=True)

        # Input for Model Base URL if not already set in secrets
        if "MODEL_BASE_URL" not in st.secrets:
            st.text_input("Model Base URL", key="model_base_url", value="https://api.groq.com/openai/v1", placeholder="Eg : https://api.openai.com/v1")

        # Input for Model API Key if not already set in secrets
        if "MODEL_API_KEY" not in st.secrets:
            st.text_input(
                "Model API Key",
                type="password",
                placeholder="Enter your API key here",
                help="Get your API key from [openai](https://platform.openai.com/account/api-keys) or [groq](https://console.groq.com/keys)",
                key="model_api_key"
            )

        # Input for Model ID if not already set in secrets
        if "MODEL_NAMES" not in st.secrets:
            st.text_input("Model ID", key="model_name", value="llama-3.1-8b-instant", placeholder="Eg : gpt-4o, llama3.1")

        # Dropdown to select Model if MODEL_NAMES is available in secrets
        if "MODEL_NAMES" in st.secrets:
            st.selectbox(
                "Select Model",
                options=st.secrets["MODEL_NAMES"],
                index=0,
                key="model_name"
            )

        # Input for Tavily API Key if not already set in secrets
        if "TAVILY_API_KEY" not in st.secrets:
            st.text_input(
                "Tavily API Key",
                type="password",
                placeholder="Paste your tavily key here",
                help="You can get your API key from https://app.tavily.com/home",
                key="tavily_api_key"
            )

        # Button to open system settings
        if st.button("⚙️ Wiz Settings", use_container_width=True):
            system_settings()

        # Separator line in the sidebar
        st.markdown("---")
        # Link to the source code repository
        st.link_button("🔗 Source Code", "https://github.com/SSK-14/WizSearch", use_container_width=True)

        # Determine available providers based on API keys in secrets
        providers = []
        if "OPENAI_MODEL_API_KEY" in st.secrets:
            providers.append("OpenAI")
        if "GROQ_MODEL_API_KEY" in st.secrets:
            providers.append("Groq")
        if "IS_AZURE" in st.secrets and st.secrets["IS_AZURE"]:
            providers.append("Azure")

        # Add provider selector if multiple providers are available
        if len(providers) > 1:
            st.selectbox(
                "Select Provider",
                options=providers,
                index=0,
                key="selected_provider"
            )
        elif len(providers) == 1:
            st.session_state.selected_provider = providers[0]
        else:
            st.warning("No API keys found in secrets.toml")