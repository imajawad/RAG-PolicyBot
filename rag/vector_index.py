"""ChromaDB vector index for the policy RAG app."""

from __future__ import annotations
import os
import shutil
from pathlib import Path
import chromadb
from langchain_core.documents import Document

COLLECTION_NAME = "policy_docs"


def _get_client(persist_directory: str):
    return chromadb.PersistentClient(path=persist_directory)


def save_index(chunks, embeddings, persist_directory: str, reset: bool = False) -> int:
    if reset and os.path.isdir(persist_directory):
        shutil.rmtree(persist_directory)

    client = _get_client(persist_directory)

    # Delete existing collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Embed in batches of 50 to avoid memory issues
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        texts = [c.page_content for c in batch]
        vectors = embeddings.embed_documents(texts)
        ids = [f"chunk_{i + j}" for j in range(len(batch))]
        metadatas = [dict(c.metadata) for c in batch]

        collection.add(
            ids=ids,
            embeddings=vectors,
            documents=texts,
            metadatas=metadatas,
        )

    return collection.count()


def search_index(question: str, embeddings, persist_directory: str, k: int = 5):
    client = _get_client(persist_directory)
    collection = client.get_collection(
        name=COLLECTION_NAME,
    )

    query_vector = embeddings.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    docs_and_scores = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for text, meta, distance in zip(documents, metadatas, distances):
        # ChromaDB cosine distance → similarity score (1 - distance)
        score = 1.0 - distance
        doc = Document(page_content=text, metadata=meta)
        docs_and_scores.append((doc, score))

    return docs_and_scores