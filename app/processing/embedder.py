from sentence_transformers import SentenceTransformer

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model

def embed_text(text:str) -> list[float]:
    return _get_model().encode(text).tolist()

def embed_texts(texts:list[str]) -> list[list[float]]:
    return _get_model().encode(texts).tolist()

