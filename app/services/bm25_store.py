from rank_bm25 import BM25Okapi

bm25 = None
documents = []


def tokenize(text):
    return text.lower().split()


def build_bm25_index(chunks):
    global bm25, documents

    documents = chunks

    texts = [chunk["text"] for chunk in chunks]
    tokenized_docs = [tokenize(t) for t in texts]

    bm25 = BM25Okapi(tokenized_docs)

    print(f"BM25 index built with {len(chunks)} documents.")


def search_bm25(query, top_k=5):
    if bm25 is None:
        return []

    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    return [documents[i] for i in top_indices]
