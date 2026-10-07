from app.connectors.connector_factory import ConnectorFactory
from app.processing.chunker import chunk_documents
from app.vectorstore.chroma_store import ChromaVectorStore

# connector = ConnectorFactory.create("pdf", "data/Formula_One.pdf")
# raw_chunks = connector.load()
# chunks = chunk_documents(raw_chunks)

store = ChromaVectorStore()
# store.add(chunks)
# print(f"Added {len(chunks)} chunks to the vector store.")

results = store.search("what are different typoes of chanpionships in f1", top_k=3)
for r in results:
    print("\n---")
    print(r.text)
    print(r.metadata)