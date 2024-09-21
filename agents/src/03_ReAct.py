# langchain
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
# frontend
import streamlit as st
# env
import os
from dotenv import load_dotenv
load_dotenv()

# langraph

# memory
from langgraph.checkpoint.memory import MemorySaver


# tools
import tools
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState
class MessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built 
    pass


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from PIL import Image as PILImage  # Import PIL Image


## start streamlit app
st.title("ReAct Agent")

# List of available models
available_models = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    # Add more models as needed
]

llm = ChatOpenAI(
    # base_url="https://openrouter.ai/api/v1",
    # api_key=os.getenv("OPENROUTER_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.0
)



tools = [tools.multiply, tools.add, tools.divide]

llm_with_tools = llm.bind_tools(tools)

# System message
system_message = """
You are a helpful assistant that can multiply, add, and divide numbers.
"""

# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([system_message] + state["messages"])]}

memory = MemorySaver()
# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
graph = builder.compile(checkpointer=memory)


# Convert the graph image to a PIL Image before displaying
graph_image = graph.get_graph(xray=True).draw_mermaid_png()  # Convert to 


def main():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = available_models[0]  # Default model

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        # st.write(message)
        with st.chat_message(message.type):
            st.markdown(message.content)

    # Capture user input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append(HumanMessage(content=prompt, name="user"))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            ### LLM call
            # response = llm.invoke(st.session_state.messages)
            inputs = {"messages": st.session_state.messages}
            response = graph.invoke(inputs)
            print(response)
            st.write(response["messages"][-1].content)
            st.write(response["messages"][-1].tool_calls)
        
        st.session_state.messages = response["messages"] 

    # Add a delete button to clear messages
    if st.button("Delete Messages"):
        st.session_state.messages = []  # Clear the messages

    # Add sidebar for model selection
    with st.sidebar:
        st.header("Model Selection")
        selected_model = st.selectbox("Choose a model:", available_models, index=available_models.index(st.session_state["openai_model"]))
        st.session_state["openai_model"] = selected_model
        st.header("Agent Graph")
        # View
        st.image(graph_image)

main()