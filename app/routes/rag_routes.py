from fastapi import APIRouter

from app.services.vector_store import build_faiss_index, search_faiss
from app.services.code_chunker import chunk_code
from app.services.repo_ingestion import clone_repo, read_code_files
from app.services.bm25_store import build_bm25_index, search_bm25
from pydantic import BaseModel
from app.services.llm_service import generate_answer

class RepoRequest(BaseModel):
    repo_url: str
 
router = APIRouter()
@router.post("/ingest-repo")
def ingest_repo(request: RepoRequest):

    repo_path = clone_repo(request.repo_url)
    files = read_code_files(repo_path)
    chunks = chunk_code(files)

    # Build FAISS
    num_indexed = build_faiss_index(chunks)

    # Build BM25
    build_bm25_index(chunks)

    return {
        "message": "Repo indexed successfully",
        "num_files": len(files),
        "num_chunks": len(chunks),
        "indexed": num_indexed
    }

class RepoQueryRequest(BaseModel):
    question: str

@router.post("/query-repo")
def query_repo(request: RepoQueryRequest):

    # Hybrid retrieval
    faiss_results = search_faiss(request.question, top_k=5)
    bm25_results = search_bm25(request.question, top_k=5)

    combined = faiss_results + bm25_results

    # Deduplicate
    seen = set()
    unique_results = []

    for item in combined:
        key = item["text"]
        if key not in seen:
            seen.add(key)
            unique_results.append(item)

    top_chunks = unique_results[:5]

    #  LLM generation
    answer = generate_answer(request.question, top_chunks)

    return {
        "question": request.question,
        "answer": answer,
        "sources": top_chunks
    }