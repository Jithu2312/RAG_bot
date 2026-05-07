# RepoLens

RepoLens is an AI-powered repository understanding and conversational code exploration system built using Retrieval-Augmented Generation (RAG).

The project allows users to:

- Ingest GitHub repositories
- Parse and chunk source code intelligently
- Store embeddings using FAISS
- Perform hybrid retrieval using:
  - Semantic Search (FAISS)
  - Keyword Search (BM25)
- Ask natural language questions about codebases
- Maintain short-term conversational memory
- Generate contextual AI answers using Gemini

---

# Project Goal

Modern repositories are large and difficult to navigate.

Developers often spend significant time:

- Searching for where features are implemented
- Understanding unfamiliar codebases
- Finding API usages
- Tracing business logic
- Understanding architecture
- Onboarding into projects

RepoLens aims to solve this problem by acting as:

> “ChatGPT for GitHub repositories.”

Instead of manually searching files, users can ask questions like:

- "Where is JWT authentication implemented?"
- "How is user login handled?"
- "Which file contains database connection logic?"
- "Where is payment validation performed?"
- "Explain the architecture of this project"
- "Which endpoint handles order creation?"

RepoLens retrieves the most relevant code chunks and generates contextual answers.

---

# Current Architecture

The current implementation is a:

## Hybrid Conversational Code RAG

It combines:

| Component | Purpose |
|---|---|
| FAISS | Semantic similarity search |
| BM25 | Exact keyword matching |
| Sentence Transformers | Code embeddings |
| Gemini | Answer generation |
| Memory Store | Multi-turn conversations |
| FastAPI | Backend API |

---

# High-Level Workflow

```text
GitHub Repo URL
        ↓
Clone Repository
        ↓
Read Source Files
        ↓
Code Chunking
        ↓
Embedding Generation
        ↓
FAISS + BM25 Indexing
        ↓
User Question
        ↓
Hybrid Retrieval
        ↓
Conversation Memory
        ↓
Gemini Prompt Construction
        ↓
AI Generated Answer
```

---

# Features

## Implemented Features

### Repository Ingestion
- Clone public GitHub repositories
- Read source files recursively
- Ignore unsupported file types

### Intelligent Code Chunking
- Splits large codebases into smaller searchable chunks
- Maintains file-level metadata
- Supports function-level understanding

### Semantic Search
- Uses embeddings to understand meaning
- Finds relevant code even if keywords differ

### Keyword Search
- BM25-based retrieval
- Handles exact term matching
- Improves precision for technical queries

### Hybrid Retrieval
- Combines semantic + keyword search
- Better retrieval quality than using only FAISS

### Conversational Memory
- Maintains short-term session context
- Enables follow-up questions
- Multi-turn interactions supported

### AI Answer Generation
- Uses Gemini for contextual responses
- Generates explanations using retrieved code context

### CI Pipeline
- GitHub Actions based CI
- Black formatting checks
- isort import checks
- Flake8 lint validation

---

# Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI |
| Vector Search | FAISS |
| Keyword Retrieval | BM25 |
| Embeddings | sentence-transformers |
| LLM | Gemini |
| CI/CD | GitHub Actions |
| Formatting | Black |
| Linting | Flake8 |
| Import Sorting | isort |

---

# Retrieval Architecture

## 1. Semantic Retrieval (FAISS)

Semantic retrieval helps the system understand meaning.

Example:

Question:

```text
Where is login handled?
```

Even if the code contains:

```python
authenticate_user()
```

FAISS retrieval can still identify the relevant code because embeddings capture semantic meaning.

---

## 2. Keyword Retrieval (BM25)

BM25 is useful when exact terms matter.

Example:

```text
JWT middleware
```

BM25 performs exact keyword matching.

This improves retrieval precision for:

- Function names
- API names
- Technical keywords
- Variables
- File names

---

## 3. Hybrid Search

RepoLens combines:

- FAISS semantic retrieval
- BM25 keyword retrieval

This provides better results than either technique alone.

---

# Conversational Memory

RepoLens currently supports short-term memory.

Example:

```text
User: Where is authentication implemented?
Assistant: Authentication logic exists in auth.py

User: What middleware does it use?
```

The second question works because conversation history is preserved.

Memory currently uses an in-memory session store.

---

# Current Project Structure

```text
repolens/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── main.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── routes/
│   │   └── rag_routes.py
│   │
│   └── services/
│       ├── bm25_store.py
│       ├── code_chunker.py
│       ├── embedding.py
│       ├── llm_service.py
│       ├── memory.py
│       ├── repo_ingestion.py
│       └── vector_store.py
│
├── repos/
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

# File-by-File Explanation

## app/main.py

Application entry point.

Responsibilities:
- Creates FastAPI app
- Registers routes
- Starts backend server

---

## app/routes/rag_routes.py

Contains all API endpoints.

Endpoints:

### POST /ingest-repo
- Accepts GitHub repository URL
- Clones repository
- Chunks code
- Builds FAISS + BM25 indexes

### POST /query-repo
- Accepts user question
- Retrieves conversation memory
- Performs hybrid retrieval
- Generates AI answer
- Stores conversation history

---

## app/services/repo_ingestion.py

Handles repository operations.

Responsibilities:
- Clone GitHub repositories
- Read supported source files
- Return repository contents

---

## app/services/code_chunker.py

Splits source code into searchable chunks.

Current implementation:
- Chunk-based splitting
- Metadata preservation
- Function-level chunk storage

Each chunk contains:

```python
{
    "text": code_chunk,
    "file_path": file_path
}
```

---

## app/services/embedding.py

Generates vector embeddings.

Uses:

```python
sentence-transformers/all-MiniLM-L6-v2
```

Purpose:
- Convert code/text into dense vectors
- Enable semantic similarity search

---

## app/services/vector_store.py

Handles FAISS operations.

Responsibilities:
- Create vector index
- Store embeddings
- Perform semantic search

Current FAISS Index:

```python
faiss.IndexFlatL2
```

---

## app/services/bm25_store.py

Handles keyword retrieval.

Responsibilities:
- Tokenize chunks
- Build BM25 index
- Perform keyword matching

Useful for:
- Exact technical terms
- API names
- Function names

---

## app/services/memory.py

Implements conversational memory.

Responsibilities:
- Store chat history
- Retrieve previous messages
- Maintain session context

Current implementation:
- In-memory dictionary storage

---

## app/services/llm_service.py

Handles answer generation.

Responsibilities:
- Construct prompts
- Inject retrieved context
- Inject conversation history
- Generate Gemini responses

---

## app/models/schemas.py

Contains Pydantic request/response models.

Used for:
- API validation
- Request parsing
- Response formatting

---

# Installation

## 1. Clone Repository

```bash
git clone <your_repo_url>
cd repolens
```

---

## 2. Create Virtual Environment

Using uv:

```bash
uv venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## 4. Configure Gemini API Key

Create:

```text
config.py
```

Example:

```python
GEMINI_API_KEY = "your_api_key"
```

---

## 5. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# API Usage

# 1. Ingest Repository

## Endpoint

```http
POST /rag/ingest-repo
```

## Request

```json
{
  "repo_url": "https://github.com/user/repo"
}
```

---

# 2. Query Repository

## Endpoint

```http
POST /rag/query-repo
```

## Request

```json
{
  "question": "Where is authentication implemented?",
  "session_id": "user_1"
}
```

---

# Current Limitations

## Current Memory
- In-memory only
- Lost after restart

## Current Chunking
- Basic chunking
- Not full AST-aware chunking yet

## Current Retrieval
- No reranking yet
- No metadata filtering yet

## Current Scope
- Optimized mainly for Python repositories

---

# Planned Enhancements

## AST-Based Chunking
Smarter function/class extraction.

## Cross-File Relationship Mapping
Understand imports and dependencies.

## Persistent Memory
Store chat sessions in Redis/DB.

## Reranking
Improve retrieval accuracy.

## Multi-Language Support
Support:
- Rust
- Go
- Java
- TypeScript
- C++

## Repository Graph Understanding
Architecture-aware retrieval.

## Streaming Responses
Real-time token streaming.

## Frontend UI
Interactive conversational interface.

---

# CI Pipeline

RepoLens includes a lightweight GitHub Actions CI pipeline.

Current checks:

- Black
- isort
- Flake8

Purpose:
- Maintain consistent code quality
- Prevent formatting issues
- Catch lint problems before merge

---

# Why Hybrid Retrieval Matters

Using only FAISS is insufficient for code repositories.

Reason:
- Code search often requires exact matching
- Technical identifiers matter

Using only BM25 is also insufficient.

Reason:
- Semantic meaning gets lost
- Synonyms cannot be understood

Hybrid retrieval combines both strengths.

---

# Example Query Flow

Example:

```text
Question:
Where is JWT token validation implemented?
```

## Step 1
BM25 retrieves chunks containing:
- JWT
- token
- validation

## Step 2
FAISS retrieves semantically related chunks.

## Step 3
Retrieved chunks are merged.

## Step 4
Conversation history is appended.

## Step 5
Gemini generates contextual answer.

---

# Learning Outcomes From This Project

This project demonstrates:

- RAG architecture
- Hybrid retrieval systems
- Vector databases
- Semantic search
- BM25 keyword search
- Conversational memory
- FastAPI backend development
- CI pipeline setup
- AI-powered code understanding

---

# Future Vision

RepoLens can evolve into:

- AI repository onboarding assistant
- Engineering knowledge system
- AI code navigator
- Team-level code intelligence platform
- Enterprise repository search engine

---

# License

MIT License

