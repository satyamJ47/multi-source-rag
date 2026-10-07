from app.connectors.base import BaseConnector
from app.connectors.pdf_connector import PDFConnector
from app.connectors.text_connector import TextConnector
from app.connectors.excel_connector import ExcelConnector

class ConnectorFactory:
    _registry : dict[str,type[BaseConnector]] = {
        "pdf" : PDFConnector,
        "text" : TextConnector,
        "excel": ExcelConnector,
    }

    @classmethod
    def create(cls,source_type:str,source_path:str) -> BaseConnector:
        connector_class = cls._registry.get(source_type)
        if connector_class is None:
            raise ValueError(
                f"No connector registered for source_type='{source_type}'. "
                f"Available: {list(cls._registry.keys())}"
            )
        connector = connector_class(source_path)
        return connector
