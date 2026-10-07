from app.vectorstore.base import BaseVectorStore
from app.models.schemas import Chunk

class Retriever:
    def __init__(self, vector_store:BaseVectorStore):
        self.vector_store = vector_store

    def retrieve(self,query:str,top_k:int= 4)->list[Chunk]:
        return self.vector_store.search(query,top_k=top_k)