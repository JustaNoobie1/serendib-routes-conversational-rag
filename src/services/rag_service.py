from pathlib import Path

from src.core.embedding_manager import EmbeddingManager
from src.core.vector_store_manager import VectorStoreManager
from src.core.retriever_manager import RetrieverManager
from src.core.llm_manager import LLMManager
from src.core.rag_pipeline import RAGPipeline
from src.graph.serendib_graph import LangGraphRAG

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "knowledge_base"
    / "rag_chunks.jsonl"
)


QDRANT_PATH = (
    PROJECT_ROOT
    / "storage"
    / "qdrant_langchain"
)

class RAGService:
    def __init__(self):

        # Load embedding model
        embedding_manager = EmbeddingManager()

        embeddings = (
            embedding_manager
            .get_embeddings()
        )


        # Create vector database
        self.vector_manager = VectorStoreManager(
            embeddings=embeddings,
            qdrant_path=QDRANT_PATH
        )

        vector_store = self.vector_manager.load_vector_store()

        retriever_manager = RetrieverManager(vector_store)
        
        llm_manager = LLMManager()

        rag_pipeline = RAGPipeline(
            retrieve_manager=retriever_manager,
            llm_manager=llm_manager)

        self.graph_rag = LangGraphRAG(
        retrieve_manager=retriever_manager,
        llm_manager=llm_manager,
        rag_pipeline=rag_pipeline
        )

        
        print(
            "✅ Serendib Routes AI initialized"
            )

    def chat(self, question, thread_id):
        if question.lower() in {
            "exit",
            "quit"
            }:
            print("quitting the system")
               
        answer = self.graph_rag.ask(question=question, 
            thread_id= thread_id)

        return str(answer)    

    def close(self):
        if self.vector_manager is not None:
            self.vector_manager.close()

