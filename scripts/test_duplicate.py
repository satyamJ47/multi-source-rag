from app.connectors.connector_factory import ConnectorFactory
from app.processing.chunker import chunk_documents
from app.vectorstore.chroma_store import ChromaVectorStore

connector = ConnectorFactory.create("pdf", "data/Formula_One.pdf")
chunks = chunk_documents(connector.load())

store = ChromaVectorStore()
store.add(chunks)
print("after 1st ingest:", store.collection.count())

store.add(chunks)  # ingest the SAME file again
print("after 2nd ingest:", store.collection.count())