from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingManager:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embeddings = None
        self.load_model()

    def load_model(self):
         print(f"Loading embedding model: {self.model_name}")
         self.embeddings = HuggingFaceEmbeddings(
             model_name = self.model_name,
             encode_kwargs = {
                 'normalize_embeddings': True
             }
         )
         print('Embedding model loaded successfully')

    def get_embeddings(self):
        return self.embeddings
        