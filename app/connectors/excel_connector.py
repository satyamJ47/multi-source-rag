import pandas as pd
from app.connectors.base import BaseConnector
from app.models.schemas import Chunk


class ExcelConnector(BaseConnector):
    def load(self) -> list[Chunk]:
        df = pd.read_excel(self.source_path)
        chunks = []

        print(df)
        for i, row in df.iterrows():
            sentence = ", ".join(f"{col.strip()}: {row[col]}" for col in df.columns)
            chunks.append(
                Chunk(
                    text=sentence,
                    source_type="excel",
                    source_name=self.source_path,
                    metadata={"row": int(i)},
                )
            )

        return chunks