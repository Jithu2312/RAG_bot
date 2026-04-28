from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    query: str
    session_id: str   # 👈 REQUIRED for memory


class QueryResponse(BaseModel):
    answer: str


# Optional (for repo-specific queries — cleaner separation)
class RepoQueryRequest(BaseModel):
    question: str
    session_id: str


# Optional (for repo ingestion)
class RepoIngestRequest(BaseModel):
    repo_url: str