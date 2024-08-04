# memEDA: LangGraph Agent Structure

This README provides an explanation of the LangGraph agent structure used in the memEDA project, which is designed to assist with Exploratory Data Analysis (EDA).

## Overview

The memEDA project uses LangGraph to create a multi-agent system for managing and updating a dataset description during the EDA process. The system consists of three main components:

1. Memory Sentinel
2. Knowledge Master
3. Tool Executor

These components work together in a graph structure to process user inputs, update the dataset description, and provide responses.

## Agent Structure

### 1. Memory Sentinel

- **Purpose**: Determines if a given message contains information worth recording or updating in the dataset description.
- **Input**: User message
- **Output**: Boolean (TRUE or FALSE)
- **Implementation**: Uses the `sentinel_runnable` with a specific prompt template and LLM.

### 2. Knowledge Master

- **Purpose**: Analyzes messages for new information and decides how to update the dataset description.
- **Input**: User message and current memories (dataset description)
- **Output**: Updated messages, potentially including tool calls
- **Implementation**: Uses the `knowledge_master_runnable` with a prompt template, LLM, and bound tools.

### 3. Tool Executor

- **Purpose**: Executes tool calls made by the Knowledge Master to modify the dataset description.
- **Input**: Tool invocations
- **Output**: Tool responses, updated memories
- **Implementation**: Uses the `ToolExecutor` class with the `modify_knowledge` function.

## Graph Structure

The LangGraph structure is implemented as a `StateGraph` with the following flow:

1. Entry Point: Sentinel
2. Conditional Edge: 
   - If Sentinel returns "yes" → Knowledge Master
   - If Sentinel returns "no" → End
3. Knowledge Master Node
4. Conditional Edge:
   - If should continue (tool calls present) → Action (Tool Executor)
   - If should end (no tool calls) → End
5. Action Node (Tool Executor) → End

## Key Functions

- `call_sentinel`: Invokes the Memory Sentinel
- `call_knowledge_master`: Invokes the Knowledge Master
- `call_tool`: Executes tool calls made by the Knowledge Master
- `should_continue`: Determines whether to continue processing or end based on the presence of tool calls

## Workflow

1. User input is first processed by the Memory Sentinel to determine if it contains relevant information.
2. If relevant, the Knowledge Master analyzes the input and current memories to decide on necessary updates.
3. The Knowledge Master may make tool calls to modify the dataset description.
4. Tool calls are executed by the Tool Executor.
5. The process continues until no more tool calls are made.
6. Finally, a response is generated based on the updated dataset description.

This LangGraph structure allows for a flexible and extensible system that can efficiently manage and update the dataset description throughout the EDA process.
