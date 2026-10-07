from app.models.schemas import Chunk

SYSTEM_INSTRUCTIONS = (
    "You are a helpful assistant. Answer the user's question using ONLY the "
    "context provided below. If the answer isn't in the context, say you "
    "don't have enough information - do not make things up."
)


def build_prompt(question: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"[Source: {c.source_type}:{c.source_name}]\n{c.text}" for c in chunks
    )
    return (
        f"{SYSTEM_INSTRUCTIONS}\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )