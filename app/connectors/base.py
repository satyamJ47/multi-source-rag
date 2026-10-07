from abc import ABC, abstractmethod
from app.models.schemas import Chunk

class BaseConnector(ABC):
    def __init__(self, source_path: str):
        self.source_path = source_path

    @abstractmethod
    def load(self) -> list[Chunk]:
        ...

        