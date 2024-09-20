import faiss
import numpy as np

class VectorDB:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []

    def add_documents(self, embeddings: np.ndarray, documents: list):
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        distances, indices = self.index.search(query_embedding, top_k)
        return [(self.documents[i], distances[0][j]) for j, i in enumerate(indices[0])]