import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    APP_NAME = "Serendib Routes AI"
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "qwen3:4b-instruct-2507-q4_K_M"
    )
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )
    QDRANT_URL = os.getenv(
        "QDRANT_URL",
        "https://fac90d0b-877c-4ad6-a4bb-9be2db9c23c3.eu-west-2-0.aws.cloud.qdrant.io"
    )
    QDRANT_API_KEY = os.getenv(
        "QDRANT_API_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YmVlMTA5YjItMzVlNC00YmEwLThkMGEtYWU5MjhlYzYwYjNlIn0.VqW7L3caZxLqbIsByvKW5tgviFhdIzA93llQLw4uksY"
    )
    QDRANT_COLLECTION = os.getenv(
        "QDRANT_COLLECTION",
        "serendib_routes"
    )
    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )
settings = Settings()