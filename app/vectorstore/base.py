from abc import ABC, abstractmethod
from app.models.schemas import Chunk

class BaseVectorStore (ABC):
    @abstractmethod
    def add(self, chunks:list[Chunk])->None:
        pass

    @abstractmethod
    def search(self, query:str, top_k:int = 4)->list[Chunk]:
        pass

    @abstractmethod
    def delete_by_source(self, source_name: str) -> None:
        raise NotImplementedError