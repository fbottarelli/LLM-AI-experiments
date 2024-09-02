import asyncio  # Importing asyncio for asynchronous programming
import streamlit as st  # Importing Streamlit for web app interface
from src.modules.model import llm_generate  # Importing the function to generate language model responses
from src.modules.tools.vectorstore import search_collection, all_points  # Importing functions for vector store operations
from src.modules.prompt import intent_prompt, search_rag_prompt, standalone_query_prompt  # Importing various prompt templates
from src.utils import abort_chat  # Importing utility to abort chat
from src.modules.tools.search import initialise_tavily  # Importing function to initialize Tavily search
from src.modules.tools.langfuse import end_trace  # Importing function to end tracing
from src.modules.prompt import base_prompt, query_formatting_prompt, generate_prompt, followup_query_prompt, key_points_prompt, summary_prompt  # Importing additional prompt templates

async def process_query():
    # Retrieve the latest query from session state
    query = st.session_state.messages[-1]["content"]
    # If there are more than 3 messages, generate a standalone query
    if len(st.session_state.messages) > 3:
        history = st.session_state.messages[:-1]  # Get the message history
        query = await llm_generate(standalone_query_prompt(query, history), "Standalone Query")  # Generate standalone query
        st.write(f"❓ Standalone query: {query}")  # Display the standalone query
    st.write("🔄 Processing your query...")  # Indicate processing
    intent = await llm_generate(intent_prompt(query), "Intent")  # Generate intent from the query
    intent = intent.strip().lower()  # Clean up the intent string
    st.write(f"🔍 Intent validated...")  # Indicate intent validation
    return query, intent  # Return the processed query and intent

async def search_vectorstore(query):
    trace = st.session_state.trace  # Get the trace from session state
    st.write("📚 Searching the document...")  # Indicate document search
    if trace:
        retrieval = trace.span(name="Retrieval", metadata={"search": "document"}, input=query)  # Start tracing retrieval
    search_results = search_collection(st.session_state.collection_name, query, st.session_state.top_k)  # Search the vector store
    st.session_state.search_results = search_results  # Store search results in session state
    if trace:
        retrieval.end(output=search_results)  # End tracing retrieval
    if search_results:  # If there are search results
        return search_rag_prompt(search_results, st.session_state.messages)  # Return the search results formatted for RAG

async def search_tavily(query):
    tavily = initialise_tavily()  # Initialize Tavily search
    trace = st.session_state.trace  # Get the trace from session state
    st.write("🌐 Searching the web...")  # Indicate web search
    if trace:
        retrieval = trace.span(name="Retrieval", metadata={"search": "tavily"}, input=query)  # Start tracing retrieval
    search_results = tavily.search(query, search_depth="advanced", include_images=True)  # Perform web search
    st.session_state.search_results = search_results  # Store search results in session state
    if trace:
        retrieval.end(output=search_results)  # End tracing retrieval                
    if search_results["results"]:  # If there are results
        search_context = [{"url": obj["url"], "content": obj["content"]} for obj in search_results["results"]]  # Prepare search context
        image_urls = []  # Initialize image URLs list
        if "VISION_MODELS" in st.secrets:  # Check for vision models in secrets
            if st.session_state.model_name in st.secrets['VISION_MODELS']:  # If the model is a vision model
                image_urls = search_results["images"]  # Get image URLs from search results
        return search_rag_prompt(search_context, st.session_state.messages, image_urls)  # Return formatted search results
    else:  # If no results found
        if trace:
            end_trace("No search results found", "WARNING")  # End trace with warning
        abort_chat("I'm sorry, There was an error in search. Please try again.")  # Abort chat with error message

async def generate_answer_prompt():
    with st.status("🚀 AI at work...", expanded=True) as status:  # Show status while processing
        query, intent = await process_query()  # Process the query and get intent
        followup_query_asyncio = asyncio.create_task(llm_generate(followup_query_prompt(st.session_state.messages), "Follow-up Query"))  # Generate follow-up query asynchronously
                    
        if len(st.session_state.image_data):  # If there is image data
            prompt = generate_prompt(query, st.session_state.messages, st.session_state.image_data)  # Generate prompt with images
        elif "search" in intent:  # If intent is to search
            query = await llm_generate(query_formatting_prompt(query), "Query Formatting")  # Format the query
            st.write(f"📝 Search query: {query}")  # Display the formatted search query
            if st.session_state.vectorstore:  # If using vector store
                prompt = await search_vectorstore(query)  # Search in vector store
            else:
                prompt = await search_tavily(query)  # Search using Tavily
        elif "generate" in intent:  # If intent is to generate
            st.write("🔮 Generating response...")  # Indicate response generation
            prompt = generate_prompt(query, st.session_state.messages)  # Generate response prompt
        else:  # For any other intent
            prompt = base_prompt(intent, query)  # Generate base prompt
        status.update(label="Done and dusted!", state="complete", expanded=False)  # Update status to complete
    return prompt, followup_query_asyncio  # Return the generated prompt and follow-up task

async def generate_summary_prompt():
    with st.status("📝 Reading through the document...", expanded=False) as status:  # Show status while reading document
        st.toast("Process may take a while, please wait...", "⏳")  # Notify user to wait
        query = st.session_state.messages[-1]["content"]  # Get the latest query
        all_texts = all_points(st.session_state.collection_name)  # Retrieve all points from the collection
        tasks = [llm_generate(key_points_prompt(text), "Key Points") for text in all_texts]  # Create tasks for key points generation
        key_points = await asyncio.gather(*tasks)  # Gather all key points
        status.update(label="Done and dusted!", state="complete", expanded=False)  # Update status to complete
    key_points = "\n".join([f"{point}" for point in key_points])  # Join key points into a single string
    return summary_prompt(query, key_points)  # Return the summary prompt
