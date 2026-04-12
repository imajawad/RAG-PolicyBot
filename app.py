"""
app.py - Flask web application for the Policy RAG chatbot

Endpoints:
  GET  /        - Chat UI
  POST /chat    - RAG query endpoint
  GET  /health  - Health check
"""

import os
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def _vector_store_ready() -> bool:
    chroma_path = Path(os.getenv("CHROMA_PATH", "chroma_db"))
    # ChromaDB 0.6.x uses chroma.sqlite3 (not index.json)
    return chroma_path.is_dir() and (
        (chroma_path / "chroma.sqlite3").is_file()
        or any(chroma_path.iterdir())  # fallback: dir exists and is non-empty
    )

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Pre-warm the embedding model so the first user query doesn't timeout.
# This runs once per gunicorn worker at startup.
try:
    from rag.retriever import _get_embeddings
    _get_embeddings()
    logger.info("Embedding model pre-warmed successfully.")
except Exception as _e:
    logger.warning(f"Could not pre-warm embedding model: {_e}")


@app.route("/")
def index():
    """Serve the chat UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    POST /chat
    Body:    { "question": "What is the PTO policy?" }
    Returns: { "answer": "...", "sources": [...], "snippets": [...], "latency": 0.5 }
    """
    data = request.get_json(silent=True)
    if not data or not data.get("question", "").strip():
        return jsonify({"error": "Missing or empty 'question' field"}), 400

    question = data["question"].strip()

    if len(question) > 500:
        return jsonify({"error": "Question too long (max 500 characters)"}), 400

    logger.info(f"Question: {question[:80]}")

    try:
        # Import inside the route so startup never crashes
        from rag.retriever import get_rag_response
        result = get_rag_response(question)
        logger.info(f"Answered in {result['latency']}s | sources: {result['sources']}")
        return jsonify(result)

    except Exception as e:
        logger.exception("Error in /chat endpoint")
        return jsonify({
            "answer":   f"Server error: {str(e)}",
            "sources":  [],
            "snippets": [],
            "latency":  0,
            "status":   "error",
        }), 500


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status":       "ok",
        "service":      "Policy RAG",
        "version":      "1.0.0",
        "vector_store": _vector_store_ready(),
    })


if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    logger.info(f"Starting PolicyBot on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
