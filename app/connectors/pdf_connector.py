from pypdf import PdfReader
from app.connectors.base import BaseConnector
from app.models.schemas import Chunk

class PDFConnector(BaseConnector):
    def load(self)-> list[Chunk]:
        reader = PdfReader(self.source_path)
        chunks = []
        # print(reader)
        # print(reader.pages)
        # print(reader.pages[0])
        for page_num, page in enumerate(reader.pages,start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue

            chunks.append(
                Chunk(
                    text=text,
                    source_type="pdf",
                    source_name=self.source_path,
                    metadata={"page":page_num},
                )
            )

        return chunks 