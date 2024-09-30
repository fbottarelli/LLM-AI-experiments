import os
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import BedrockEmbeddings
from dotenv import load_dotenv
import streamlit as st
import matplotlib.pyplot as plt
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse
from libs.RAG.qdrant_operations import qdrant_delete_by_filter

load_dotenv()


# providers
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse

# generic
import os
import logging


logger = logging.getLogger(__name__)

def get_embedding_model():
    from openai import OpenAI
    client = OpenAI()

    response = client.embeddings.create(
        input="Your text string goes here",
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def vectorstore_definition(db: str, embedding_provider: str, collection_name: str, hybrid: bool):
    dense_embeddings = get_embedding_model()
    if hybrid:    
        sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
    else:
        sparse_embeddings = None

    if db == "QDRANT":
        url = os.getenv("QDRANT_URL")
        client = QdrantClient(
            url=url,
        )
        # always create the collections, or the lambda won't work if missing
        # create_collection(client, collection_name)'
        if hybrid:
            vectorstore = QdrantVectorStore(
                client=client,
                collection_name=collection_name,
                embedding=dense_embeddings,
                vector_name="dense",
                sparse_embedding=sparse_embeddings,
                sparse_vector_name="sparse",
                # retrieval_mode="RetrievalMode.HYBRID",
                retrieval_mode="hybrid",
            )
        else:
            vectorstore = QdrantVectorStore(
                client=client,
                collection_name=collection_name,
                embedding=dense_embeddings,
            )
    return vectorstore

def format_docs(docs):
    formatted_docs = []
    chunks_list = []
    for doc in docs:
        if doc.metadata.get("chunk_type") == "image_chunk":
            chunk = {
                "extracted_image_description": doc.page_content
            }
        elif doc.metadata.get("chunk_type") == "document_chunk":
            chunk = {
                "chunk_type": doc.metadata.get("chunk_type"),
                "chunk_content": doc.page_content 
            }
        else:
            print("Chunk type not recognized")
            continue
        chunks_list.append(chunk)
    
    chunk_intro = "Retrieved chunks:"
    chunks_string = f"{chunk_intro} {chunks_list}"
    formatted_docs.append(chunks_string)
    return "\n\n".join(formatted_docs)

def get_available_collections():
    url = os.getenv("QDRANT_URL")
    client = QdrantClient(url=url)
    collections = client.get_collections()
    return [collection.name for collection in collections.collections]

def get_chunk_type_counts(client, collection_name):
    chunk_types = ["table_chunk", "qa", "text_chunk", "series_chunk"]
    counts = {}
    for chunk_type in chunk_types:
        count = client.count(
            collection_name=collection_name,
            count_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.chunk_type",
                        match=models.MatchValue(value=chunk_type)
                    ),
                ]
            ),
            exact=True,
        )
        counts[chunk_type] = count.count
    return counts

def streamlit_interface():
    initialize_session_state()
    sidebar_config()
    
    st.title("Retrieval Test Interface")

    qdrant_url, collection_name = get_qdrant_config()

    # Query input
    query = st.text_input("Enter your query")

    # Embedding provider and database selection (can be expanded if needed)
    embedding_provider = "Bedrock-embeddings"
    db = "QDRANT"

    if st.button("Retrieve"):
        vectorstore = vectorstore_definition(db, embedding_provider, collection_name, hybrid=True)
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 6, "score_threshold": 0.2}
        )

        docs = retriever.get_relevant_documents(query)
        formatted_results = format_docs_specialspring(docs)

        st.subheader("Retrieved Chunks:")
        st.json(eval(formatted_results.split("Retrieved chunks: ")[1]))

    # Add a section to display chunk type counts
    st.subheader("Chunk Type Counts")
    if st.button("Get Counts"):
        url = "http://internal-chatbo-llmba-zjovyxhbq8e8-1705934167.eu-central-1.elb.amazonaws.com:6333"
        client = QdrantClient(url=url)
        counts = get_chunk_type_counts(client, collection_name)
        for chunk_type, count in counts.items():
            st.write(f"{chunk_type}: {count}")

    # Delete Points section
    st.subheader("Delete Points by Type")
    delete_type = st.selectbox("Select chunk type to delete", ["table_chunk", "qa", "text_chunk", "series_chunk"])
    if st.button("Delete Points"):
        url = "http://internal-chatbo-llmba-zjovyxhbq8e8-1705934167.eu-central-1.elb.amazonaws.com:6333"
        client = QdrantClient(url=url)
        qdrant_delete_by_filter("chunk_type", delete_type, collection_name, client)
        if delete_type == "qa":
            qdrant_delete_by_filter("source_type", delete_type, collection_name, client)
        st.success(f"Points with chunk_type '{delete_type}' have been deleted from collection '{collection_name}'.")

    # New section for searching, counting, and printing points
    st.subheader("Search and Filter Points")
    filter_key = st.text_input("Enter filter key (e.g., metadata.city)")
    filter_value = st.text_input("Enter filter value (e.g., London or 42)")
    
    if st.button("Search and Count"):
        url = "http://internal-chatbo-llmba-zjovyxhbq8e8-1705934167.eu-central-1.elb.amazonaws.com:6333"
        client = QdrantClient(url=url)
        
        # Try to convert the filter_value to an integer if possible
        try:
            filter_value = int(filter_value)
        except ValueError:
            # If conversion fails, keep it as a string
            pass

        # Create the filter
        search_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key=f"metadata.{filter_key}",
                    match=models.MatchValue(value=filter_value),
                )
            ]
        )
        print(search_filter)
        
        # Count points
        count_result = client.count(
            collection_name=collection_name,
            count_filter=search_filter,
            exact=True
        )
        st.write(f"Number of points matching the filter: {count_result.count}")
        
        # Scroll through points
        scroll_results = client.scroll(
            collection_name=collection_name,
            scroll_filter=search_filter,
            limit=30  # Limit to 30 results for display
        )
        
        st.write("Sample matching points:")
        for point in scroll_results[0]:
            st.json(point.payload)

    # Add a section to display chunk type counts and statistics
    st.subheader("Collection Statistics")
    if st.button("Get Statistics"):
        url = "http://internal-chatbo-llmba-zjovyxhbq8e8-1705934167.eu-central-1.elb.amazonaws.com:6333"
        client = QdrantClient(url=url)
        counts = get_chunk_type_counts(client, collection_name)
        
        # Display total count
        total_count = sum(counts.values())
        st.write(f"Total points in collection: {total_count}")
        
        # Display counts for each chunk type
        st.write("Counts by chunk type:")
        for chunk_type, count in counts.items():
            st.write(f"- {chunk_type}: {count}")
        
        # Create a bar plot
        fig, ax = plt.subplots()
        ax.bar(counts.keys(), counts.values())
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Chunk Types')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    # New Section: Create Collection
    st.subheader("Create New Collection")
    new_collection_name = st.text_input("Enter new collection name")
    vector_size = st.number_input("Enter vector size", min_value=1, value=768)
    distance_metric = st.selectbox("Select distance metric", ["COSINE", "DOT", "EUCLID"])

    if st.button("Create Collection"):
        if new_collection_name:
            try:
                client = QdrantClient(url=qdrant_url)
                client.recreate_collection(
                    collection_name=new_collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance[distance_metric]
                    )
                )
                st.success(f"Collection '{new_collection_name}' created successfully.")
            except Exception as e:
                st.error(f"Error creating collection: {e}")
        else:
            st.error("Please enter a collection name.")

streamlit_interface()