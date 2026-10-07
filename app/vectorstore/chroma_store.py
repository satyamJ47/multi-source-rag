import hashlib
import chromadb
from app.vectorstore.base import BaseVectorStore
from app.models.schemas import Chunk
from app.processing.embedder import embed_texts, embed_text

def _stable_id(chunk: Chunk) -> str:
    meta_str = ",".join(f"{k}={v}" for k, v in sorted(chunk.metadata.items()))
    raw = f"{chunk.source_type}:{chunk.source_name}:{meta_str}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

class ChromaVectorStore(BaseVectorStore):
    def __init__(self, collection_name:str = "rag_chunks", persist_dir:str = "./data/chroma"):
        client = chromadb.PersistentClient(path=persist_dir)
        self.collection = client.get_or_create_collection(collection_name)

    def delete_by_source(self, source_name):
        deleted = self.collection.delete(where={"source_name":source_name})
        print(f"deleted records: {deleted}")

    def add(self,chunks:list[Chunk]) -> None:
        if chunks is None:
            return

        self.delete_by_source(chunks[0].source_name) # clear old chunks for this file first
        texts = [c.text for c in chunks]
        vectors = embed_texts(texts)
        ids = [_stable_id(c) for c in chunks]
        metadatas = [{"source_type":c.source_type,"source_name":c.source_name, **c.metadata} for c in chunks]

        self.collection.upsert(ids=ids,embeddings=vectors,metadatas=metadatas,documents=texts)

    def search(self, query:str, top_k:int = 4) -> list[Chunk]:
        query_vector = embed_text(query)
        # Query by vector similarity
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        # print(results)
        # print(type(results))

        chunks = []
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for text,meta in zip(documents,metadatas):
            meta = dict(meta)
            source_type = meta.pop("source_type","unknown")
            source_name = meta.pop("source_name","unknown")
            chunks.append(Chunk(text=text,source_type=source_type,source_name=source_name,metadata=meta))

        return chunks
    

