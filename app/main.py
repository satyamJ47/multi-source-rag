from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="GenAI RAG system",version="0.1.0")
app.include_router(router)

@app.get("/")
def health_check():
    return {"status":"running"}
