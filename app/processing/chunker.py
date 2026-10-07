from app.models.schemas import Chunk

def split_text(text: str, chunk_size: int = 50, overlap: int = 10) -> list[str]:
    words = text.split()
    if not words:
        return []

    pieces = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        piece = " ".join(words[start:end])
        pieces.append(piece)
        start += chunk_size - overlap

    return pieces


def chunk_documents(raw_chunks: list[Chunk]) -> list[Chunk]:
    result: list[Chunk] = []

    for raw in raw_chunks:
        pieces = split_text(raw.text)
        for i, piece in enumerate(pieces):
            result.append(
                Chunk(
                    text=piece,
                    source_type=raw.source_type,
                    source_name=raw.source_name,
                    metadata={**raw.metadata, "chunk_index": i}
                )
            )

    return result