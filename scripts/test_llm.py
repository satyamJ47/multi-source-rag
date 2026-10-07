from dotenv import load_dotenv
load_dotenv()

from app.vectorstore.chroma_store import ChromaVectorStore
from app.retrieval.retriever import Retriever
from app.generation.prompt_builder import build_prompt
from app.generation.llm_client import get_llm_client

store = ChromaVectorStore()
retriever = Retriever(store)

question = "What is F1"
chunks = retriever.retrieve(question, top_k=3)
prompt = build_prompt(question, chunks)

llm = get_llm_client()
answer = llm.generate(prompt)
print(answer)