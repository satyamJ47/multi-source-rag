import pandas as pd
from app.connectors.base import BaseConnector
from app.models.schemas import Chunk


class ExcelConnector(BaseConnector):
    def load(self) -> list[Chunk]:
        sheets = pd.read_excel(self.source_path, sheet_name=None)  # dict: sheet name -> DataFrame
        chunks = []

        for sheet_name, df in sheets.items():
            for i, row in df.iterrows():
                fields = ", ".join(f"{str(col).strip()}: {row[col]}" for col in df.columns)
                chunks.append(
                    Chunk(
                        text=f"sheet: {sheet_name}, {fields}",
                        source_type="excel",
                        source_name=self.source_path,
                        metadata={"sheet": str(sheet_name), "row": int(i)},
                    )
                )

        return chunks