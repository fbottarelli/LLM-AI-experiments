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
import json
from enum import Enum

load_dotenv()

MEMORY_FILE = "memories.json"

class Category(str, Enum):
    KEY_VARIABLES = "key_variables"
    CURRENT_EDA_STATUS = "current_eda_status"
    NEXT_STEPS = "next_steps"

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    memories: Sequence[str]
    contains_information: str

def load_memories():
    try:
        with open(MEMORY_FILE, 'r') as f:
            memories = json.load(f)
        return memories
    except (FileNotFoundError, json.JSONDecodeError):
        return {cat.value: [] for cat in Category}

def display_memories(memories):
    if not memories:
        st.write("No memories saved.")
        return

    st.subheader("Dataset Description")
    for category, items in memories.items():
        st.write(f"**{category.replace('_', ' ').title()}:**")
        for item in items:
            st.write(f"- {item}")
        st.write("")  # Add a blank line between categories

def generate_response(question, memories):
    context = "\n".join([f"{cat}: {', '.join(items)}" for cat, items in memories.items()])
    
    system_message = get_prompt(prompts, "system_prompt_query_answering").format(context=context)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    return response.content

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

# Set up the Graph
graph = StateGraph(AgentState)

graph.add_node("sentinel", call_sentinel)
graph.add_node("knowledge_master", call_knowledge_master)
graph.add_node("action", call_tool)

graph.set_entry_point("sentinel")

graph.add_conditional_edges(
    "sentinel",
    lambda x: x["contains_information"],
    {
        "yes": "knowledge_master",
        "no": END,
    },
)
graph.add_conditional_edges(
    "knowledge_master",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

graph.add_edge("action", END)

app = graph.compile()

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
