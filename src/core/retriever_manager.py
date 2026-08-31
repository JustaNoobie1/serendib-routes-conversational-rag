class RetrieverManager:
    def __init__(self, vector_store, top_k=5):
        self.vector_store = vector_store
        self.top_k = top_k
        self.retriever = None

        self.initialize_retriever()

    def initialize_retriever(self):
        if self.vector_store is None:
            raise ValueError(
                "Vector store is not initiated"
            )
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                'k': self.top_k
            }
        )
        print(
            f"Retriever initialized successfully "
            f"with top_k={self.top_k}"
        )

    def retrieve(self, query):
        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
        )

        return self.retriever.invoke(query)

    def retrieve_with_scores(self, query, top_k=None):
        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
        )
        k = self.top_k or top_k
        results = self.vector_store.similarity_search_with_score(
            query = query,
            k = k
        )
        return results
