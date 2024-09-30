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
chat_page = st.Page("RAG.py", title="Chat with RAG", icon="💬")
model_page = st.Page("Calculator.py", title="Calculator Agent", icon="🤖")
qdrant_page = st.Page("qdrant_managment.py", title="Qdrant", icon="🧪")

pg = st.navigation([home_page, chat_page, model_page, qdrant_page]) 
st.set_page_config(page_title="Esperimento Agente", page_icon="🧪")

pg.run()