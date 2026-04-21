from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """
    Reads a PDF file and extracts all text.
    """

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:  # handle None cases
            text += extracted + "\n"

    return text