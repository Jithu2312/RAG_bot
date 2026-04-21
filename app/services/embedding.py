from sentence_transformers import SentenceTransformer

# Load once (important)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Convert list of text chunks → embeddings
    """
    return model.encode(texts)


def embed_query(query: str):
    """
    Convert query → embedding
    """
    return model.encode([query])