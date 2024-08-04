import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict, Sequence
from langchain_core.messages import BaseMessage

load_dotenv()

# Initialize LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Streamlit page config
st.set_page_config(page_title="EDA Assistant", page_icon="📊", layout="wide")
st.title("EDA Assistant")

# Import the prompts dictionary
from libs.prompts import prompts

# Define the get_prompt function to retrieve prompts from the dictionary
def get_prompt(prompts, name):
    return prompts.get(name, f"Prompt with name '{name}' not found.")

# Use the get_prompt function to retrieve the desired prompts
system_prompt_sentinel_EDA = get_prompt(prompts, "system_prompt_memory_sentinel_EDA")
system_prompt_memory_manager = get_prompt(prompts, "system_prompt_memory_manager_EDA")
system_prompt_query_answering = get_prompt(prompts, "system_prompt_query_answering")

# ... [Rest of the Streamlit app code, including the graph setup and main function]

# Main Streamlit app logic
def main():
    memories = load_memories()
    display_memories(memories)

    # Initialize session state for user input if it doesn't exist
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Display previous response if it exists
    if 'response' in st.session_state:
        st.write("Response:", st.session_state.response)

        # Display tool usage if any
        if 'tool_calls' in st.session_state:
            st.subheader("Tools Used:")
            for tool_call in st.session_state.tool_calls:
                st.write(f"Tool: {tool_call['function']['name']}")
                st.write(f"Input: {tool_call['function']['arguments']}")
        
        # Display updated memories
        st.subheader("Updated Dataset Description")
        display_memories(load_memories())

    # User input section
    user_input = st.text_input("Ask a question about the dataset or EDA progress:", key="user_input")
    if user_input:
        with st.spinner("Analyzing and generating response..."):
            # Prepare inputs for the LangGraph app
            inputs = AgentState(
                messages=[HumanMessage(content=user_input)],
                memories=memories,
                contains_information=""
            )
            
            # Run the LangGraph app
            result = app.invoke(inputs)
            
            # Generate a response based on the question and updated memories
            updated_memories = load_memories()
            response = generate_response(user_input, updated_memories)
            
            # Store the response and tool calls in session state
            st.session_state.response = response
            st.session_state.tool_calls = result["messages"][-1].additional_kwargs.get("tool_calls", [])

            # Rerun the app to display the new response
            st.rerun()

if __name__ == "__main__":
    main()
