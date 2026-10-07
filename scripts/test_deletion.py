from app.connectors.connector_factory import ConnectorFactory
from app.processing.chunker import chunk_documents
from app.vectorstore.chroma_store import ChromaVectorStore

connector = ConnectorFactory.create("text", "data/air.txt")
chunks = chunk_documents(connector.load())


store = ChromaVectorStore()
print("count before ingest:", store.collection.count())
store.add(chunks)
print("count after ingest:", store.collection.count())

store.add(chunks)  # same file again
print("count after re-ingest (same content):", store.collection.count())