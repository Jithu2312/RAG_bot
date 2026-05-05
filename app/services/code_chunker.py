import re
from typing import Dict, List


def detect_language(file_path: str) -> str:
    if file_path.endswith(".py"):
        return "python"
    elif file_path.endswith(".js") or file_path.endswith(".ts"):
        return "javascript"
    elif file_path.endswith(".java"):
        return "java"
    elif file_path.endswith(".rs"):
        return "rust"
    else:
        return "unknown"


# ----------- FUNCTION SPLITTER -----------


def split_python_functions(content: str):
    pattern = r"(def\s+\w+\(.*?\):[\s\S]*?)(?=\ndef\s|\Z)"
    return re.findall(pattern, content)


def split_js_functions(content: str):
    pattern = r"(function\s+\w+\(.*?\)\s*\{[\s\S]*?\})"
    return re.findall(pattern, content)


def split_rust_functions(content: str):
    pattern = r"(fn\s+\w+\(.*?\)\s*\{[\s\S]*?\})"
    return re.findall(pattern, content)


def split_java_methods(content: str):
    pattern = r"(public|private|protected).*?\(.*?\)\s*\{[\s\S]*?\}"
    return re.findall(pattern, content)


# ----------- MAIN CHUNKER -----------


def chunk_code(files_data: List[Dict]):

    chunks = []

    for file in files_data:
        file_path = file["file_path"]
        content = file["content"]

        language = detect_language(file_path)

        functions = []

        if language == "python":
            functions = split_python_functions(content)

        elif language == "javascript":
            functions = split_js_functions(content)

        elif language == "rust":
            functions = split_rust_functions(content)

        elif language == "java":
            functions = split_java_methods(content)

        # fallback if no functions found
        if not functions:
            functions = [content]

        for func in functions:
            chunks.append({"text": func, "file_path": file_path, "language": language})

    return chunks
