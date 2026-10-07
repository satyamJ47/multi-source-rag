from app.connectors.base import BaseConnector
from app.models.schemas import Chunk

class TextConnector(BaseConnector):
    def load(self) -> list[Chunk]:
        # with helps to close file automatically even when it faces error while reading
        with open(self.source_path,"r",encoding="utf-8") as f:
            text = f.read()

        if not text.strip():
            return []

        return [
            Chunk(
                text=text,
                source_type="text",
                source_name=self.source_path,
                metadata={},
            )
        ]
