from qdrant_client import QdrantClient

from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)
if not client.collection_exists("my_collection"):
   client.create_collection(
      collection_name="my_collection",
      vectors_config=VectorParams(size=100, distance=Distance.COSINE),
   )


from qdrant_client.models import PointStruct

client.upsert(
   collection_name="my_collection",
   points=[
      PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload={"color": "red", "rand_number": idx % 10}
      )
      for idx, vector in enumerate(vectors)
   ]
)