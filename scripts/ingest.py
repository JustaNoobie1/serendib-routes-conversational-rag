from pathlib import Path
from core.document_manager import DocumentManager
from core.embedding_manager import EmbeddingManager
from core.vector_store_manager import VectorStoreManager


PROJECT_ROOT = (
    Path(__file__).resolve().parents[1]
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


def main():

    # Load documents
    document_manager = DocumentManager(DATA_FILE)

    documents = (
        document_manager
        .load_documents()
    )


    # Load embedding model
    embedding_manager = EmbeddingManager()

    embeddings = (
        embedding_manager
        .get_embeddings()
    )


    # Create vector database
    vector_manager = VectorStoreManager(
        embeddings=embeddings,
        qdrant_path=QDRANT_PATH
    )

    try:
        vector_manager.create_vector_store(
            documents
        )


        print(
            "\n✅ Serendib Routes "
            "LangChain ingestion complete!"
        )
    finally:
        vector_manager.close()

if __name__=="__main__":
    main()