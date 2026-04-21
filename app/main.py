from fastapi import FastAPI
from app.routes.rag_routes import router as rag_router

app = FastAPI(title="RAG App")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(rag_router, prefix="/rag")