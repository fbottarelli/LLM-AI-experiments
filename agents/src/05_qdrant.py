import streamlit as st
from qdrant_client import QdrantClient
from RAG.qdrant import create_collection, upsert_points, search_points
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, Range
import numpy as np

# Initialize Qdrant client
client = QdrantClient(host="localhost", port=6333)



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

