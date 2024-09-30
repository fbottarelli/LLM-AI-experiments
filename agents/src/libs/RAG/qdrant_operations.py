from qdrant_client import QdrantClient, models
import uuid
import os
import json


def bedrock_embedding(text, model_id):
    runtime = boto3.client('bedrock-runtime')
    response = runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": text}).encode()
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get("embedding")
    return embedding

def qdrant_create_collection(qdrant_client, collection_name, vector_size=1024):
    """
    Creates a new collection in the Qdrant database with a specified name.

    This function initializes a Qdrant client using the QDRANT_URL environment variable and creates a new collection
    with the given name. The collection is configured to use COSINE distance for vector comparisons and expects vectors
    of size 1536.

    Parameters:
    - collection_name (str): The name of the collection to create.
    """
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config={"dense": models.VectorParams(size=1024, distance=models.Distance.COSINE)},
        sparse_vectors_config={"sparse": models.SparseVectorParams()}
    )

def ensure_collection_exists(qdrant_client, collection_name):
    try:
        collection_status = qdrant_client.get_collection(collection_name=collection_name)
        print("Collection exists, status:", collection_status.status)
    except Exception as e:
        print(f"Error retrieving collection {collection_name}: {str(e)}, proceeding to create a new collection.")
        qdrant_create_collection(qdrant_client, collection_name, 1024)
    return None

# Funzione per caricare i punti nel database vettoriale Qdrant
def qdrant_upload(docs, qdrant_client, collection_name, hybrid=False):
    """
    Uploads documents to a specified collection in the Qdrant database.

    Each document is assigned a unique ID and its embeddings are uploaded along with any metadata.
    The metadata and the page content are stored in the payload for filtering purposes.

    Parameters:
    - docs (list of dict): A list of dictionaries, each representing a document with embeddings and metadata.
    - collection_name (str): The name of the collection to upload the documents to.
    """
    # upload of data
    if hybrid:
        print("\n\n")
        print("sparse_embeddings")
        print(docs[0]["sparse_embeddings"])

        print("\n\n")
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector={
                        "dense": doc["dense_embeddings"],
                        "sparse": {
                            "indices": doc["sparse_embeddings"].indices,
                            "values": doc["sparse_embeddings"].values
                            }
                    },
                    ### qui bisogna fare unpack delle cose dentro metadata ed inserirle come valori singoli
                    ### in modo da poter fare filtering
                    # payload={ **doc["metadata"], "page_content": doc["page_content"] }
                    payload={
                        "metadata": doc["metadata"],
                        "page_content": doc["page_content"],
                    },
                )
                for doc in docs
            ],
        )
    else:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector={"dense": doc["dense_embeddings"]},
                    payload={
                        "metadata": doc["metadata"],
                        "page_content": doc["page_content"],
                        },
                )
                for doc in docs
            ],
        )
    print("vectors uploaded in Qdrant database")

# Funzione per eliminare i punti dal database vettoriale Qdrant sulla base di un filtro
def qdrant_delete_by_filter(key, value, collection_name, qdrant_client):
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
    qdrant_client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key=f"metadata.{key}",
                        match=models.MatchValue(value=value),
                    ),
                ],
            )
        ),
    )
    print(f"Points with field: {key} == {value} removed")
    return None


def qdrant_check_by_filter(key, value, collection_name, qdrant_client):
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
    points_count = qdrant_client.count(
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

def find_unique_doc(collection_name: str):
    url = os.getenv("QDRANT_URL")
    client = QdrantClient(
        url=url,
    )
    points = client.scroll(
        collection_name=f"{collection_name}",
        limit=50,
        with_payload=True,
        with_vectors=False,
    )

    i = 0
    unique_docs = []
    seen_titles = set()
    for point in points[0]:
        title = point.payload["metadata"]["file_name"]
        if title not in seen_titles:
            seen_titles.add(title)
            unique_docs.append(
                {
                    "file_name": title,
                    "file_summary": point.payload["metadata"]["file_summary"],
                }
            )
    return unique_docs