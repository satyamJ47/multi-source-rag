from app.connectors.connector_factory import ConnectorFactory
from app.processing.chunker import chunk_documents

connector = ConnectorFactory.create("pdf","data/Formula_one.pdf")
raw_chunks = connector.load()
print("raw_chunks: ",len(raw_chunks),type(connector).__name__)
split_chunks = chunk_documents(raw_chunks)
print("split_chunks: ", len(split_chunks))
print(split_chunks)