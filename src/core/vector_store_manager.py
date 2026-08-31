from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

class VectorStoreManager:
    def __init__(self, embeddings, qdrant_path, collection_name = "serendib_routes"):
        self.embeddings = embeddings
        self.qdrant_path = qdrant_path
        self.collection_name = collection_name
        self.vector_store = None

    def create_vector_store(self, documents):
        print("Creating LangChain Qdrant vector store...")
        self.vector_store = QdrantVectorStore.from_documents(
            documents= documents,
            embedding= self.embeddings,
            path=str(self.qdrant_path),
            collection_name = self.collection_name,
            force_recreate=True
        )
        print(
            "Vector store created successfully."
        )
        return self.vector_store

    def load_vector_store(self):
        print("Loading existing vector store from disk...")
        self.vector_store = QdrantVectorStore.from_existing_collection(
            path=str(self.qdrant_path),
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
        print(
            "Vector store loaded successfully."
                )
        return self.vector_store

    def close(self):
        if self.vector_store is not None:
            try:
                self.vector_store.client.close()
            except Exception:
                pass

    
        