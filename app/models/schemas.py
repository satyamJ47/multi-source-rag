from pydantic import BaseModel

class Chunk(BaseModel):
    text: str
    source_type: str          # e.g. "pdf", "sql", "mongo", "excel"
    source_name: str          # e.g. filename or table name
    metadata: dict = {}       # anything extra worth keeping (page number, row id, etc.)


class IngestRequest(BaseModel):
    source_type: str
    source_path: str

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list[Chunk]