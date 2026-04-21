from fastapi import APIRouter, UploadFile, File
import os

from app.services.document_loader import load_pdf
from app.services.chunking import chunk_text
from app.services.embedding import embed_texts
from app.services.llm_service import generate_answer
from app.services.vector_store import create_index
from app.services.embedding import embed_query
from app.services.vector_store import search
from app.models.schemas import QueryRequest, QueryResponse
router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Step 1: Extract
    text = load_pdf(file_path)

    # Step 2: Chunk
    chunks = chunk_text(text)

    # Step 3: Embed
    embeddings = embed_texts(chunks)

    # Step 4: Store
    create_index(embeddings, chunks)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "message": "Embeddings created and stored"
    }


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):

    # Step 1: Embed query
    query_embedding = embed_query(request.query)

    # Step 2: Retrieve chunks
    retrieved_chunks = search(query_embedding)

    # Step 3: Generate answer using LLM
    answer = generate_answer(request.query, retrieved_chunks)

    return QueryResponse(answer=answer) 