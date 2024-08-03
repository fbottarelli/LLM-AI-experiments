import os
from dotenv import load_dotenv
import chainlit as cl
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage
from typing import TypedDict, Sequence
from langchain_core.messages import BaseMessage

load_dotenv()

# Your existing code for setting up the LangGraph components
# (Include all the necessary imports and function definitions)

# Set model variables
# OPENAI_BASE_URL = "https://api.openai.com/v1"
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")

# Initialize LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] = "Demos"


# ### Import the prompts dictionary
from libs.prompts import prompts

# Define the get_prompt function to retrieve prompts from the dictionary
def get_prompt(prompts, name):
    return prompts.get(name, f"Prompt with name '{name}' not found.")

# Use the get_prompt function to retrieve the desired prompts
system_prompt_sentinel_EDA = get_prompt(prompts, "system_prompt_memory_sentinel_EDA")
system_prompt_memory_manager = get_prompt(prompts, "system_prompt_memory_manager_EDA")



# ### Set up Agent: Memory Sentinel

# Import necessary modules
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough

# Define the prompt for the Memory Sentinel
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_sentinel_EDA),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember, only respond with TRUE or FALSE. Do not provide any other information.",
        ),
    ]
)

# Initialize the LLM for the Memory Sentinel
llm = ChatOpenAI(
    model="gpt-4o-mini",
    streaming=True,
    temperature=0.0,
)

# Create the runnable for the Memory Sentinel
sentinel_runnable = {"messages": RunnablePassthrough()} | prompt | llm

# ### Set up Agent: Memory Manager

# Import necessary modules and define data structures
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from enum import Enum
from typing import Optional

# Define enums for categories and actions
class Category(str, Enum):
    KEY_VARIABLES = "key_variables"
    CURRENT_EDA_STATUS = "current_eda_status"
    NEXT_STEPS = "next_steps"

class Action(str, Enum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"

# Define the structure for adding knowledge
class AddKnowledge(BaseModel):
    knowledge: str = Field(
        ...,
        description="Structured information about the dataset or EDA progress to be saved or updated",
    )
    knowledge_old: Optional[str] = Field(
        None,
        description="If updating or deleting, the complete, exact phrase that needs to be modified",
    )
    category: Category = Field(
        ..., description="Category that this information belongs to"
    )
    action: Action = Field(
        ...,
        description="Whether this information is adding a new record, updating a record, or deleting a record",
    )

import json

# Function to modify the knowledge base
def modify_knowledge(
    knowledge: str,
    category: Category,
    action: Action,
    knowledge_old: str = "",
) -> dict:
    print(f"Modifying Dataset Description: {action} {category} - {knowledge}")
    if knowledge_old:
        print(f"Old information: {knowledge_old}")
    
    # Load existing memories
    try:
        with open(MEMORY_FILE, 'r') as f:
            memories = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        memories = {cat.value: [] for cat in Category}
    
    # Modify memories based on action
    if action == Action.ADD:
        memories[category].append(knowledge)
    elif action == Action.UPDATE:
        if knowledge_old in memories[category]:
            index = memories[category].index(knowledge_old)
            memories[category][index] = knowledge
    elif action == Action.DELETE:
        memories[category] = [item for item in memories[category] if item != knowledge_old]
    
    # Save updated memories
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memories, f)
    
    return memories  # Return the memories directly, not wrapped in a dict

# Create a tool for modifying knowledge
tool_modify_knowledge = StructuredTool.from_function(
    func=modify_knowledge,
    name="Knowledge_Modifier",
    description="Add, update, or delete information in the dataset description",
    args_schema=AddKnowledge,
)

# Set up the tools to execute them from the graph
from langgraph.prebuilt import ToolExecutor

# Set up the agent's tools
agent_tools = [tool_modify_knowledge]

tool_executor = ToolExecutor(agent_tools)

# Import necessary modules for the Memory Manager
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.utils.function_calling import convert_to_openai_function

# Define the prompt for the Memory Manager
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_memory_manager),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize the LLM for the Memory Manager
llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    temperature=0.0,
)

# Create the tools to bind to the model
tools = [convert_to_openai_function(t) for t in agent_tools]

# Create the runnable for the Memory Manager
knowledge_master_runnable = prompt | llm.bind_tools(tools)

# ### Set up the Graph

# Import necessary modules for the graph
from typing import TypedDict, Sequence
from langchain_core.messages import BaseMessage

# Define the state structure for the agent
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]  # The list of previous messages in the conversation
    memories: Sequence[str]  # The long-term memories to remember
    contains_information: str  # Whether the information is relevant

import json
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolInvocation

# Function to call the Memory Sentinel
def call_sentinel(state):
    messages = state["messages"]
    response = sentinel_runnable.invoke(messages)
    return {"contains_information": "TRUE" in response.content and "yes" or "no"}

# Function to determine whether to continue or not
def should_continue(state):
    last_message = state["messages"][-1]
    if "tool_calls" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

# Function to call the Memory Manager
def call_knowledge_master(state):
    messages = state["messages"]
    memories = state["memories"]
    response = knowledge_master_runnable.invoke(
        {"messages": messages, "memories": memories}
    )
    return {"messages": messages + [response]}

# Function to execute tools
def call_tool(state):
    messages = state["messages"]
    memories = state["memories"]
    last_message = messages[-1]

    for tool_call in last_message.additional_kwargs["tool_calls"]:
        action = ToolInvocation(
            tool=tool_call["function"]["name"],
            tool_input=json.loads(tool_call["function"]["arguments"]),
            id=tool_call["id"],
        )

        response = tool_executor.invoke(action)
        function_message = ToolMessage(
            content=str(response), name=action.tool, tool_call_id=tool_call["id"]
        )

        messages.append(function_message)
        if isinstance(response, dict) and "updated_memories" in response:
            memories = response["updated_memories"]

    return {"messages": messages, "memories": memories}

# Import necessary modules for the graph
from langgraph.graph import StateGraph, END

# Initialize a new graph
graph = StateGraph(AgentState)

# Define the nodes in the graph
graph.add_node("sentinel", call_sentinel)
graph.add_node("knowledge_master", call_knowledge_master)
graph.add_node("action", call_tool)

# Set the starting edge
graph.set_entry_point("sentinel")

# Add conditional edges
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

# Add normal edge
graph.add_edge("action", END)

# Compile the entire workflow as a runnable
app = graph.compile()

### CHAINLIT CONFIGURATION
import os
import chainlit as cl
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

import json

MEMORY_FILE = "memories.json"

# Function to load memories from file
def load_memories():
    try:
        with open(MEMORY_FILE, 'r') as f:
            memories = json.load(f)
        return memories
    except (FileNotFoundError, json.JSONDecodeError):
        return {cat.value: [] for cat in Category}

# Function to display memories in the chat
async def display_memories(memories):
    if not memories:
        await cl.Message(content="No memories saved.").send()
        return

    formatted_memories = []
    for category, items in memories.items():
        formatted_memories.append(f"## {category.replace('_', ' ').title()}:")
        formatted_memories.extend([f"- {item}" for item in items])
        formatted_memories.append("")  # Add a blank line between categories

    memory_text = "\n".join(formatted_memories)
    await cl.Message(content=f"# Dataset Description\n\n{memory_text}").send()

# Function to generate a response based on the question and memories
def generate_response(question, memories):
    context = "\n".join([f"{cat}: {', '.join(items)}" for cat, items in memories.items()])
    
    system_message = f"""You are an AI assistant helping with Exploratory Data Analysis (EDA). 
    Use the following context about the dataset and EDA progress to answer the user's question:

    {context}

    If the context doesn't contain enough information to answer the question, say so and suggest what additional analysis might help answer the question."""

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    return response.content

# Chainlit start function
@cl.on_chat_start
async def start():
    memories = load_memories()
    cl.user_session.set("memories", memories)
    await display_memories(memories)

# Chainlit message handler
@cl.on_message
async def run_conversation(message: cl.Message):
    memories = load_memories()  # Always load the latest memories from file
    
    # Prepare inputs for the LangGraph app
    inputs = AgentState(
        messages=[HumanMessage(content=message.content)],
        memories=memories,
        contains_information=""
    )
    
    # Configure the LangChain callback handler
    config = RunnableConfig(
        callbacks=[
            cl.LangchainCallbackHandler(
                stream_final_answer=True,
                to_ignore=["ChannelRead", "RunnableLambda", "ChannelWrite", "__start__", "_execute"]
            )
        ]
    )
    
    # Run the LangGraph app
    result = app.invoke(inputs, config=config)
    
    # Generate a response based on the question and updated memories
    updated_memories = load_memories()
    response = generate_response(message.content, updated_memories)
    
    # Send the generated response
    await cl.Message(content=response).send()

    # Display tool usage if any
    final_message = result["messages"][-1]
    if "tool_calls" in final_message.additional_kwargs:
        for tool_call in final_message.additional_kwargs["tool_calls"]:
            await cl.Message(
                content=f"Tool used: {tool_call['function']['name']}\n"
                        f"Input: {tool_call['function']['arguments']}"
            ).send()
    
    # Display updated memories after each interaction
    await display_memories(updated_memories)

