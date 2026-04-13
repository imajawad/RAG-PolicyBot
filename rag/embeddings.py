"""Embedding helpers for the policy RAG stack.

SWITCHED from PyTorch sentence-transformers → chromadb's built-in ONNX
DefaultEmbeddingFunction.

WHY: PyTorch alone consumes 300-400 MB RAM at runtime, which causes OOM
on Render's 512 MB free tier. The ONNX approach uses ~100-150 MB — a 3x
reduction. The model is identical: all-MiniLM-L6-v2 in ONNX format.
onnxruntime is already installed as a required dep of chromadb 0.6.x.
"""

from __future__ import annotations


class PolicyEmbeddings:
    """ONNX-based embeddings for retrieval — no PyTorch dependency."""

    def __init__(self):
        self._ef = None   # lazy-loaded

    def _get_ef(self):
        """Lazy-load chromadb's DefaultEmbeddingFunction (ONNX, no PyTorch)."""
        if self._ef is None:
            try:
                from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
            except ImportError as exc:
                raise RuntimeError(
                    "chromadb DefaultEmbeddingFunction not available. "
                    "Ensure chromadb is installed: pip install -r requirements.txt"
                ) from exc
            self._ef = DefaultEmbeddingFunction()
        return self._ef

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        result = self._get_ef()(list(texts))
        return [list(v) for v in result]

    def embed_query(self, text: str) -> list[float]:
        result = self._get_ef()([text])
        return list(result[0])