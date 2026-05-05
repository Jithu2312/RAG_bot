import os
import shutil
import subprocess

BASE_DIR = "repos"


def clone_repo(repo_url: str) -> str:
    """
    Clone GitHub repo locally
    """
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(BASE_DIR, repo_name)

    # Remove if already exists (fresh clone)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    os.makedirs(BASE_DIR, exist_ok=True)

    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    return repo_path


def read_code_files(repo_path: str):
    """
    Read all code files from repo
    """

    code_extensions = [".py", ".js", ".ts", ".java", ".rs"]

    files_data = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):

                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    files_data.append({"file_path": full_path, "content": content})

                except Exception:
                    continue

    return files_data
