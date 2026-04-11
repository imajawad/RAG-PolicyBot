"""Small persisted vector index used by the policy RAG app."""

from __future__ import annotations

import json
import math
import os
import shutil
from pathlib import Path

from langchain_core.documents import Document


INDEX_FILENAME = "index.json"


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def save_index(chunks, embeddings, persist_directory: str, reset: bool = False) -> int:
    if reset and os.path.isdir(persist_directory):
        shutil.rmtree(persist_directory)

    os.makedirs(persist_directory, exist_ok=True)

    vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
    records = []

    for chunk, vector in zip(chunks, vectors):
        records.append(
            {
                "page_content": chunk.page_content,
                "metadata": _json_safe(dict(chunk.metadata)),
                "embedding": vector,
            }
        )

    index_path = Path(persist_directory) / INDEX_FILENAME
    with index_path.open("w", encoding="utf-8") as file:
        json.dump({"version": 1, "documents": records}, file, ensure_ascii=False)

    return len(records)


def load_index(persist_directory: str) -> list[tuple[Document, list[float]]]:
    index_path = Path(persist_directory) / INDEX_FILENAME
    if not index_path.is_file():
        raise RuntimeError(
            f"Vector store not found at '{persist_directory}'. "
            "Please run: python rag/ingest.py"
        )

    with index_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    documents: list[tuple[Document, list[float]]] = []
    for record in payload.get("documents", []):
        documents.append(
            (
                Document(
                    page_content=record.get("page_content", ""),
                    metadata=record.get("metadata", {}),
                ),
                record.get("embedding", []),
            )
        )

    return documents


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0

    dot_product = sum(l_value * r_value for l_value, r_value in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot_product / (left_norm * right_norm)


def search_index(question: str, embeddings, persist_directory: str, k: int = 5):
    query_vector = embeddings.embed_query(question)
    indexed_documents = load_index(persist_directory)

    scored_documents = [
        (document, _cosine_similarity(query_vector, vector))
        for document, vector in indexed_documents
    ]
    scored_documents.sort(key=lambda item: item[1], reverse=True)
    return scored_documents[:k]