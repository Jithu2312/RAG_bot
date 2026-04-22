from rank_bm25 import BM25Okapi

bm25 = None
documents = []


def tokenize(text):
    return text.lower().split()


def build_bm25_index(chunks):
    global bm25, documents

    documents = chunks

    tokenized_docs = [tokenize(chunk["text"]) for chunk in chunks]

    bm25 = BM25Okapi(tokenized_docs)


def search_bm25(query, top_k=5):
    global bm25, documents

    tokenized_query = tokenize(query)

    scores = bm25.get_scores(tokenized_query)

    top_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    return [documents[i] for i in top_indices]