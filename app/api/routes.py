from fastapi import APIRouter, HTTPException

from app.vectorstore.chroma_store import ChromaVectorStore
from app.retrieval.retriever import Retriever
from app.connectors.connector_factory import ConnectorFactory
from app.processing.chunker import chunk_documents
from app.generation.prompt_builder import build_prompt
from app.generation.llm_client import get_llm_client

from app.models.schemas import IngestRequest, QueryRequest, QueryResponse

router = APIRouter()

vector_store = ChromaVectorStore()
retriever = Retriever(vector_store)

@router.post("/ingest")
def ingest(request: IngestRequest):
    try:
        connector = ConnectorFactory.create(request.source_type,request.source_path)
        raw_chunks = connector.load()
        chunks = chunk_documents(raw_chunks)
        vector_store.add(chunks)
        return {"status": "ok", "chunks_ingested": len(chunks)}
    except ValueError as e :
        raise HTTPException(status_code=400,detail=str(e))

@router.post("/query")
def query(request: QueryRequest):
    chunks = retriever.retrieve(request.question,request.top_k)
    if not chunks:
        return QueryResponse(answer="No relevant data found for that question", sources=[])

    prompt = build_prompt(request.question,chunks)
    llm = get_llm_client()
    answer = llm.generate(prompt)
    return QueryResponse(answer=answer,sources=chunks)