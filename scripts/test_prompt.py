from app.vectorstore.chroma_store import ChromaVectorStore
from app.retrieval.retriever import Retriever
from app.generation.prompt_builder import build_prompt

store = ChromaVectorStore()
retriever = Retriever(store)

question = "what is downforce"
chunks = retriever.retrieve(question, top_k=3)

prompt = build_prompt(question, chunks)
print(prompt)