import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict, Sequence
from langchain_core.messages import BaseMessage
import chainlit as cl

load_dotenv()

# Initialize LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Import the prompts dictionary
from libs.prompts import prompts

# Define the get_prompt function to retrieve prompts from the dictionary
def get_prompt(prompts, name):
    return prompts.get(name, f"Prompt with name '{name}' not found.")

# Use the get_prompt function to retrieve the desired prompts
system_prompt_sentinel_EDA = get_prompt(prompts, "system_prompt_memory_sentinel_EDA")
system_prompt_memory_manager = get_prompt(prompts, "system_prompt_memory_manager_EDA")
system_prompt_query_answering = get_prompt(prompts, "system_prompt_query_answering")

# Set up Agent: Memory Sentinel
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

llm = ChatOpenAI(
    model="gpt-4-0613",
    streaming=True,
    temperature=0.0,
)

sentinel_runnable = {"messages": RunnablePassthrough()} | prompt | llm

# Set up Agent: Memory Manager
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from enum import Enum
from typing import Optional

class Category(str, Enum):
    KEY_VARIABLES = "key_variables"
    CURRENT_EDA_STATUS = "current_eda_status"
    NEXT_STEPS = "next_steps"

class Action(str, Enum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"

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

MEMORY_FILE = "memories.json"

def modify_knowledge(
    knowledge: str,
    category: Category,
    action: Action,
    knowledge_old: str = "",
) -> dict:
    print(f"Modifying Dataset Description: {action} {category} - {knowledge}")
    if knowledge_old:
        print(f"Old information: {knowledge_old}")
    
    try:
        with open(MEMORY_FILE, 'r') as f:
            memories = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        memories = {cat.value: [] for cat in Category}
    
    if action == Action.ADD:
        memories[category].append(knowledge)
    elif action == Action.UPDATE:
        if knowledge_old in memories[category]:
            index = memories[category].index(knowledge_old)
            memories[category][index] = knowledge
        else:
            # If the old knowledge is not found, add the new knowledge
            memories[category].append(knowledge)
    elif action == Action.DELETE:
        memories[category] = [item for item in memories[category] if item != knowledge_old]
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memories, f)
    
    return memories

tool_modify_knowledge = StructuredTool.from_function(
    func=modify_knowledge,
    name="Knowledge_Modifier",
    description="Add, update, or delete information in the dataset description",
    args_schema=AddKnowledge,
)

agent_tools = [tool_modify_knowledge]

tool_executor = ToolExecutor(agent_tools)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_memory_manager),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI(
    model="gpt-4-0613",
    streaming=True,
    temperature=0.0,
)

from langchain_core.utils.function_calling import convert_to_openai_function
tools = [convert_to_openai_function(t) for t in agent_tools]

knowledge_master_runnable = prompt | llm.bind_tools(tools)

# Set up the Graph
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    memories: Sequence[str]
    contains_information: str

from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolInvocation

def call_sentinel(state):
    messages = state["messages"]
    response = sentinel_runnable.invoke(messages)
    return {"contains_information": "TRUE" in response.content and "yes" or "no"}

def should_continue(state):
    last_message = state["messages"][-1]
    if "tool_calls" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

def call_knowledge_master(state):
    messages = state["messages"]
    memories = state["memories"]
    response = knowledge_master_runnable.invoke(
        {"messages": messages, "memories": memories}
    )
    return {"messages": messages + [response]}

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

from langgraph.graph import StateGraph, END

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

def load_memories():
    try:
        with open(MEMORY_FILE, 'r') as f:
            memories = json.load(f)
        return memories
    except (FileNotFoundError, json.JSONDecodeError):
        return {cat.value: [] for cat in Category}

def generate_response(question, memories):
    context = "\n".join([f"{cat}: {', '.join(items)}" for cat, items in memories.items()])
    
    system_message = get_prompt(prompts, "system_prompt_query_answering").format(context=context)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    return response.content

@cl.on_chat_start
def start():
    cl.user_session.set("memories", load_memories())

@cl.on_message
async def main(message: cl.Message):
    memories = cl.user_session.get("memories")
    
    # Display current memories
    await cl.Message(content="Current Dataset Description:").send()
    for category, items in memories.items():
        await cl.Message(content=f"**{category.replace('_', ' ').title()}:**").send()
        for item in items:
            await cl.Message(content=f"- {item}").send()
    
    # Prepare inputs for the LangGraph app
    inputs = AgentState(
        messages=[HumanMessage(content=message.content)],
        memories=memories,
        contains_information=""
    )
    
    # Run the LangGraph app
    result = app.invoke(inputs)
    
    # Generate a response based on the question and updated memories
    updated_memories = load_memories()
    response = generate_response(message.content, updated_memories)
    
    # Send the response
    await cl.Message(content=response).send()
    
    # Update the session memories
    cl.user_session.set("memories", updated_memories)
    
    # Display updated memories if they've changed
    if updated_memories != memories:
        await cl.Message(content="Updated Dataset Description:").send()
        for category, items in updated_memories.items():
            await cl.Message(content=f"**{category.replace('_', ' ').title()}:**").send()
            for item in items:
                await cl.Message(content=f"- {item}").send()

if __name__ == "__main__":
    cl.run()

