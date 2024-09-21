import streamlit as st

def home():
    st.write("# Benvenuti all'Esperimento Agente! 🧪")
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

pg = st.navigation([home_page, chat_page, model_page, react_agent_page])
st.set_page_config(page_title="Esperimento Agente", page_icon="🧪")

pg.run()