import streamlit as st

def home():
    st.write("# Benvenuti Agenti! 🧪")
    st.markdown(
        """
        Questa app multi-pagina ti permette di sperimentare con diversi agenti e modelli AI.
        
        Seleziona una pagina dal menu di navigazione per iniziare!
        """
    )

home_page = st.Page(home, title="Home", icon="🏠")
chat_page = st.Page("01_Chat.py", title="Chat", icon="💬")
model_page = st.Page("02_Model_Selection.py", title="Linkedin Agent", icon="💶")
react_agent_page = st.Page("03_ReAct.py", title="ReAct Agent", icon="🤖")
rag_page = st.Page("04_RAG.py", title="RAG Agent", icon="🧪")
qdrant_page = st.Page("05_qdrant.py", title="Qdrant", icon="🧪")

pg = st.navigation([home_page, chat_page, rag_page, qdrant_page, model_page, react_agent_page])
st.set_page_config(page_title="Esperimento Agente", page_icon="🧪")

pg.run()