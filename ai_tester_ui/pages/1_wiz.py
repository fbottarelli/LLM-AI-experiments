import asyncio, json 
import streamlit as st
from src.components.sidebar import side_info
from src.modules.model import llm_stream, initialise_model
from src.components.ui import display_search_result, display_chat_messages, feedback, document, followup_questions, example_questions, add_image
from src.utils import initialise_session_state, clear_chat_history, abort_chat
from src.modules.chain import generate_answer_prompt, generate_summary_prompt
from src.modules.tools.langfuse import start_trace, end_trace

@st.fragment
async def main():
    # Check if this is the first message in the chat
    if len(st.session_state.messages) == 1:
        col1, col2, col = st.columns([4, 4, 6])
        with col1:
            document()  # Display document component
        with col2:
            add_image()  # Display image component

    # Display chat messages
    display_chat_messages(st.session_state.messages)
    
    # If this is the first message, show example questions
    if len(st.session_state.messages) == 1:
        example_questions()
            
    st.session_state.search_results = None  # Initialize search results
    # Process user query if the last message is not from the assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        query = st.session_state.messages[-1]["content"]
        start_trace(query)  # Start tracing the query

        try:
            # Generate prompt based on whether a summary exists
            if "summary" in st.session_state.messages[-1] and st.session_state.messages[-1]["summary"]:
                prompt = await generate_summary_prompt()
                followup_query_asyncio = None
            else:
                prompt, followup_query_asyncio = await generate_answer_prompt()
        except Exception as e:
            end_trace(str(e), "ERROR")  # End trace on error
            abort_chat(f"An error occurred: {e}")  # Abort chat with error message

        # Display search results if available
        if st.session_state.search_results:
            display_search_result(st.session_state.search_results)

        # Handle follow-up queries if available
        if followup_query_asyncio:
            followup_query = await followup_query_asyncio
            if followup_query:
                followup_query = "[" + followup_query.split("[")[1].split("]")[0] + "]"
                try:
                    st.session_state.followup_query = json.loads(followup_query)  # Parse follow-up query
                except json.JSONDecodeError:
                    st.session_state.followup_query = []  # Set to empty if JSON decode fails

        # Send the final answer from the assistant
        with st.chat_message("assistant", avatar="✨"):
            st.write_stream(llm_stream(prompt, "Final Answer"))
        end_trace(st.session_state.messages[-1]["content"])  # End trace for the content

    # If there are more than one messages, show options for new chat and feedback
    if len(st.session_state.messages) > 1:
        col1, col2 = st.columns([1, 4])
        col1.button('New Chat', on_click=clear_chat_history)  # Button to start a new chat
        with col2:
            feedback()  # Display feedback component
        followup_questions()  # Show follow-up questions

    # Handle chat input based on chat state
    if st.session_state.chat_aborted:
        st.chat_input("Enter your search query here...", disabled=True)  # Disable input if chat is aborted
    elif query := st.chat_input("Enter your search query here..."):
        st.session_state.messages.append({"role": "user", "content": query})  # Append user query to messages
        st.rerun()  # Rerun the app to process the new query

if __name__ == "__main__":
    st.set_page_config(page_title="Mir Assistant", page_icon="✨")  # Set page configuration
    st.title("🔍 :orange[AI] Playground")  # Set the title of the app
    side_info()  # Display side information
    initialise_session_state()  # Initialize session state
    initialise_model()  # Initialize the model
    asyncio.run(main())  # Run the main async function