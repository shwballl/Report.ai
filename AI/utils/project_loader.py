import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

VALID_EXTENSIONS = {".py", ".md", ".txt", ".json", ".cpp", ".log", ".ipynb", ".yaml", ".yml", ".toml"}
IGNORED_FILES = {"__init__.py", ".gitignore", "pyproject.toml", ".git", "__pycache__/"}

def load_and_split_project_files(folder: str) -> list[Document]:
    documents = []

    for root, _, files in os.walk(folder):
        for file in files:
            if file in IGNORED_FILES:
                continue

            path = Path(root) / file
            if path.suffix.lower() in VALID_EXTENSIONS:
                try:
                    loader = TextLoader(str(path), encoding="utf-8")
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source"] = str(path.relative_to(folder))
                        documents.append(doc)
                except Exception as e:
                    print(f"Error loading {path}: {e}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    split_docs = splitter.split_documents(documents)

    return split_docs
