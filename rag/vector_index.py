"""ChromaDB vector index for the policy RAG app."""

from __future__ import annotations
import os
import shutil
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

COLLECTION_NAME = "policy_docs"


def save_index(chunks, embeddings, persist_directory: str, reset: bool = False) -> int:
    if reset and os.path.isdir(persist_directory):
        shutil.rmtree(persist_directory)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=COLLECTION_NAME,
    )
    return vectorstore._collection.count()


def load_index(persist_directory: str, embeddings):
    if not os.path.isdir(persist_directory):
        raise RuntimeError(
            f"Vector store not found at '{persist_directory}'. "
            "Please run: python rag/ingest.py"
        )
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )


def search_index(question: str, embeddings, persist_directory: str, k: int = 5):
    vectorstore = load_index(persist_directory, embeddings)
    results = vectorstore.similarity_search_with_relevance_scores(question, k=k)
    return results