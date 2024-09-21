import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, Range
import numpy as np

# Initialize Qdrant client
client = QdrantClient(host="localhost", port=6333)

# Function to create a collection
def create_collection(collection_name, vector_size):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        st.success(f"Collection '{collection_name}' created successfully.")
    else:
        st.warning(f"Collection '{collection_name}' already exists.")

# Function to upsert points
def upsert_points(collection_name, vectors):
    points = [
        PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload={"color": "red", "rand_number": idx % 10}
        )
        for idx, vector in enumerate(vectors)
    ]
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    st.success(f"Points upserted successfully into '{collection_name}'.")

# Function to search points
def search_points(collection_name, query_vector, filter_condition=None):
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=filter_condition,
        limit=5  # Return 5 closest points
    )
    return hits

# Streamlit interface
st.title("Qdrant Management Interface")

# Create Collection Section
st.header("Create Collection")
collection_name = st.text_input("Collection Name", "my_collection")
vector_size = st.number_input("Vector Size", min_value=1, value=100)
if st.button("Create Collection"):
    create_collection(collection_name, vector_size)

# Upsert Points Section
st.header("Upsert Points")
num_points = st.number_input("Number of Points", min_value=1, value=10)
if st.button("Upsert Points"):
    vectors = np.random.random((num_points, vector_size)).tolist()
    upsert_points(collection_name, vectors)

# Search Points Section
st.header("Search Points")
query_vector = np.random.random(vector_size).tolist()
filter_condition = Filter(
    must=[
        FieldCondition(
            key='rand_number',
            range=Range(
                gte=3
            )
        )
    ]
)
if st.button("Search Points"):
    hits = search_points(collection_name, query_vector, filter_condition)
    st.write("Search Results:")
    for hit in hits:
        st.write(hit)

