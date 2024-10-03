from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, Distance
import uuid

# Function to create a collection
def create_collection(client, collection_name, vector_size, hybrid=False):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"dense": models.VectorParams(size=vector_size, distance=models.Distance.COSINE)},
            sparse_vectors_config={"sparse": models.SparseVectorParams()}
        )
        print(f"Collection '{collection_name}' created successfully.")
    else:
        print(f"Collection '{collection_name}' already exists.")

# list of collections
def list_collections(client):
    return client.get_collections()


# Function to upsert points
def upsert_points(docs, client, collection_name, hybrid=False):
    # upload of data
    points = []
    for doc in docs:
        if hybrid:
            vectors = {
                "dense": doc["dense_embeddings"],
                "sparse": {
                    "indices": doc["sparse_embeddings"].indices,
                    "values": doc["sparse_embeddings"].values
                }
            }
        else:
            vectors = {"dense": doc["dense_embeddings"]}

        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors,
                payload={
                    "metadata": doc["metadata"],
                    "page_content": doc["page_content"],
                },
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points,
    )
    print(f"Points upserted successfully into '{collection_name}'.")




def scroll_points(client, collection_name, filter_condition=None, limit=1, with_payload=True, with_vectors=False):
    client.scroll(
        collection_name=collection_name,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(key=filter_condition.key, match=models.MatchValue(value=filter_condition.value)),
            ]
        ),
        limit=limit,
        with_payload=with_payload,
        with_vectors=with_vectors,
    )


def count_points(key, value, collection_name, client):
    """
    Checks the existence of documents in a specified collection in the Qdrant database based on a filter.

    The function counts the number of documents that match the given key-value pair filter.

    Parameters:
    - key (str): The field key to filter by.
    - value (str): The value to match for the specified key.
    - collection_name (str): The name of the collection to check documents in.

    Returns:
    - int: The count of documents that match the filter.
    """
    # perform points existance check
    points_count = client.count(
        collection_name=collection_name,
        count_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key=f"metadata.{key}",
                    match=models.MatchValue(value=value),
                ),
            ]
        ),
    )
    return points_count


# qdrant delete by filter
def delete_points(condition_filter, collection_name, client):
    """
    Deletes documents from a specified collection in the Qdrant database based on a filter.

    The filter is defined by a key-value pair. All documents in the collection that match this filter
    will be deleted.

    Parameters:
    - key (str): The field key to filter by.
    - value (str): The value to match for the specified key.
    - collection_name (str): The name of the collection to delete documents from.
    """
    # perform points deletion
    client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key=f"metadata.{condition_filter.key}",
                        match=models.MatchValue(value=condition_filter.value),
                    ),
                ],
            )
        ),
    )
    print(f"Points with field: {condition_filter.key} == {condition_filter.svalue} removed")
    return None


# SEARCH
# Function to search points
def search_points(client, collection_name, query_vector, filter_condition=None, hybrid=False):
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=filter_condition,
        limit=5  # Return 5 closest points
    )
    return hits