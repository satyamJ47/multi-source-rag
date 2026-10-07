from app.retrieval.retriever import Retriever
from app.vectorstore.chroma_store import ChromaVectorStore

store = ChromaVectorStore()
retriever = Retriever(store)

results = retriever.retrieve("how fast does f1 car goes",top_k=3)
for r in results:
    print("\n-----")
    print(r.text)
    print(r.metadata)

