from fastapi import APIRouter

from app.services.vector_store import build_faiss_index, search_faiss
from app.services.code_chunker import chunk_code
from app.services.repo_ingestion import clone_repo, read_code_files
from app.services.bm25_store import build_bm25_index, search_bm25
from app.services.llm_service import generate_answer
from app.services.memory import add_message, get_memory

from app.models.schemas import RepoQueryRequest, RepoIngestRequest

router = APIRouter()


@router.post("/ingest-repo")
def ingest_repo(request: RepoIngestRequest):

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


@router.post("/query-repo")
def query_repo(request: RepoQueryRequest):

    # 1. Get memory
    history = get_memory(request.session_id)

    # 2. Retrieval
    faiss_results = search_faiss(request.question)
    bm25_results = search_bm25(request.question)

    # merge results
    retrieved_chunks = faiss_results + bm25_results

    # 3. Generate answer
    answer = generate_answer(
        question=request.question,
        contexts=retrieved_chunks,
        history=history
    )

    # 4. Store memory
    add_message(request.session_id, "user", request.question)
    add_message(request.session_id, "assistant", answer)

    return {
        "answer": answer
    }