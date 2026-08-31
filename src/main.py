from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.schemas import ChatRequest, ChatResponse
from src.services.rag_service import RAGService

rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_service

    #Startup
    rag_service = RAGService()

    yield

    #Shutdown
    if rag_service is not None:
        rag_service.close()

app = FastAPI(
    title="Serendib Routes AI",
    description=
        "Conversational RAG travel assistant for Sri Lanka tourism.",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Serendib Routes AI"
    }

@app.post("/chat", response_model= ChatResponse)
def chat(request: ChatRequest):
    answer = rag_service.chat(
        question=request.message,
        thread_id=request.thread_id
    ) 
    print(
    "FASTAPI ANSWER:",
    repr(answer)
)

    print(
    "ANSWER TYPE:",
    type(answer)
)
    return ChatResponse(
        answer=answer,
        thread_id=request.thread_id
    )