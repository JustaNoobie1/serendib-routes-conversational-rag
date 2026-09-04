from pathlib import Path
import os
from src.core.document_manager import DocumentManager
from src.core.embedding_manager import EmbeddingManager
from src.core.vector_store_manager import VectorStoreManager
from dotenv import load_dotenv

PROJECT_ROOT = (
    Path(__file__).resolve().parents[1]
)
ENV_PATH = PROJECT_ROOT / ".env"
print("PROJECT ROOT:", PROJECT_ROOT)
print("ENV PATH:", ENV_PATH)
print("ENV EXISTS:", ENV_PATH.exists())
load_dotenv(dotenv_path=ENV_PATH, override=True)

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

    QDRANT_PATH = (
    PROJECT_ROOT
    / "storage"
    / "qdrant_langchain"
)


def main():

    print(
        "ENV FILE:",
        ENV_PATH
    )

    print(
        "QDRANT MODE:",
        os.getenv("QDRANT_MODE")
    )

    print(
        "QDRANT URL SET:",
        bool(
            os.getenv("QDRANT_URL")
        )
    )

    print(
        "QDRANT API KEY SET:",
        bool(
            os.getenv(
                "QDRANT_API_KEY"
            )
        )
    )

    print(
        "QDRANT COLLECTION:",
        os.getenv(
            "QDRANT_COLLECTION"
        )
    )

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