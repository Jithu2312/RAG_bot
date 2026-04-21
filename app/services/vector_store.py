import faiss
import numpy as np

index = None
stored_chunks = []


def create_index(embeddings, chunks):
    """
    Store embeddings in FAISS
    """
    global index, stored_chunks

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    stored_chunks = chunks


def search(query_embedding, k=3):
    """
    Retrieve top-k similar chunks
    """
    global index, stored_chunks

    distances, indices = index.search(query_embedding, k)

    results = [stored_chunks[i] for i in indices[0]]

    return results