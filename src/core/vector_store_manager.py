from langchain_qdrant import QdrantVectorStore
import os 

class VectorStoreManager:
    def __init__(self, embeddings, qdrant_path, collection_name = "serendib_routes"):
        self.embeddings = embeddings
        self.qdrant_path = qdrant_path
        self.collection_name = os.getenv('QDRANT_COLLECTION', collection_name)
        self.mode = os.getenv('QDRANT_MODE', 'local')
        self.vector_store = None
        print(f"Qdrant mode: {self.mode}")

    def create_vector_store(self, documents):
        if self.mode == 'cloud':
            print("Creating LangChain Qdrant Cloud vector store...")
            self.vector_store = QdrantVectorStore.from_documents(
                documents= documents,
                embedding= self.embeddings,
                url=os.environ['QDRANT_URL'],
                api_key= os.environ['QDRANT_API_KEY'],
                collection_name = self.collection_name,
                force_recreate=True
            )
            print("Cloud Vector store created successfully.")

        else:
                    print("Creating LangChain Qdrant Local vector store...")
                    self.vector_store = QdrantVectorStore.from_documents(
                        documents= documents,
                        embedding= self.embeddings,
                        path=str(self.qdrant_path),
                        collection_name = self.collection_name,
                        force_recreate=True
                    )
                    print("Local Vector store created successfully.")

        return self.vector_store

    def load_vector_store(self):
        if self.mode == 'cloud':
            print("Loading existing vector store from cloud...")
            self.vector_store = QdrantVectorStore.from_existing_collection(
                url=os.environ['QDRANT_URL'],
                api_key= os.environ['QDRANT_API_KEY'],
                collection_name=self.collection_name,
                embedding=self.embeddings
            )
            print("Cloud Vector store loaded successfully.")

        else:
            print("Loading existing vector store from disk...")
            self.vector_store = QdrantVectorStore.from_existing_collection(
                path=str(self.qdrant_path),
                collection_name=self.collection_name,
                embedding=self.embeddings
                    )
            print("Vector store loaded successfully.")
        return self.vector_store

    def close(self):
        if self.vector_store is not None:
            try:
                self.vector_store.client.close()
            except Exception:
                pass

    
        