from app.processing.embedder import embed_text
from app.processing.embedder import embed_texts

vector = embed_text("Formula One is a motorsport.")
print("Vector length:", len(vector))
print("First 5 values:", vector[:5])

vectors = embed_texts(["Formula One is a motorsport.","Hello from the other side","I wonder if you know, how they live in Tokyo if u have seen it then u mean it...."])
print("No of vectors", len(vectors))
print("1st vector len", len(vectors[0]))
print("First 5 values of V1:", vectors[0][:5])
print("First 5 values of v2:", vectors[1][:5])
print("First 5 values of v3:", vectors[2][:5])

