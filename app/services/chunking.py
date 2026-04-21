from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str):
    """
    Splits text into overlapping chunks.
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks