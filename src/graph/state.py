from langgraph.graph import MessagesState
from langchain_core.documents import Document

class SerendibState(MessagesState):
    route: str
    question: str
    documents = list[Document]
    context: str
    answer: str
    retrieval_query: str