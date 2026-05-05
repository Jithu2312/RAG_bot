import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

faiss_index = None
metadata_store = []


def build_faiss_index(chunks):
    global faiss_index, metadata_store

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings)

    metadata_store = chunks

    return len(chunks)


def search_faiss(query, top_k=5):
    global faiss_index, metadata_store

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = faiss_index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata_store):
            results.append(metadata_store[idx])

    return results
