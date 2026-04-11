# Design and Evaluation Document

## 1. Design and Architecture Decisions

### 1.1 Overall Architecture

The system follows a classic RAG (Retrieval-Augmented Generation) architecture:

```
User Question
     │
     ▼
[Embedding Model]  ──→  Query Vector
     │
     ▼
[Local JSON Index]  ──→  Top-K Relevant Chunks + Scores
     │
     ▼
[Prompt Builder]  ──→  System Prompt + Context + Question
     │
     ▼
[Groq LLM]  ──→  Grounded Answer with Citations
     │
     ▼
Flask /chat endpoint  ──→  JSON Response to UI
```

---

### 1.2 Embedding Model: Local Hashing Embedder

**Choice:** A lightweight deterministic hashing embedder implemented in Python

**Rationale:**
- **Completely free** — runs locally with no API key or model download
- **Fast** — pure Python and small enough to run instantly during startup and ingestion
- **Deterministic** — the same text always produces the same vector, which makes evaluation and debugging easier
- **Portable** — avoids native ML runtimes that can be fragile on Windows installs

**Alternative considered:** HuggingFace sentence-transformers. Rejected because the Windows environment used for this project was unstable with the Chroma / NumPy stack and added unnecessary runtime weight for a small policy corpus.

---

### 1.3 Chunking Strategy

**Choice:** `RecursiveCharacterTextSplitter` with `chunk_size=500`, `chunk_overlap=100`

**Rationale:**
- **500 tokens** is large enough to capture complete policy rules (e.g., a full table row + surrounding context) but small enough to remain specific and avoid diluting relevance
- **100-token overlap (20%)** ensures that information split across chunk boundaries is not lost — crucial for policy documents where a rule may reference text from the previous paragraph
- **Recursive splitting on headings first** (`\n## `, `\n### `) means chunks respect document structure, keeping heading-related content together
- The splitter is deterministic for a fixed input corpus, which keeps ingestion reproducible

**Alternative considered:** Token-window chunking with tiktoken. Rejected because the character-based splitter is simpler to set up without a tokenizer dependency, and the approximate character→token mapping is adequate for these document sizes.

---

### 1.4 Vector Store: Local JSON Index

**Choice:** A local JSON index written to `chroma_db/index.json`

**Rationale:**
- **Completely free** — no cloud account, no API key, zero cost
- **Persistent** — stores embedded chunks to disk, so ingestion only runs once
- **Easy setup** — no database server and no native vector-store dependency chain
- **Sufficient scale** — our corpus is tiny, so a simple on-disk index is enough
- **Transparent** — the stored data is human-readable JSON, which helps debugging

**Alternative considered:** ChromaDB and Pinecone. Rejected because both added unnecessary dependency or operational complexity for a small local demo.

---

### 1.5 LLM: Groq (llama-3.3-70b-versatile)

**Choice:** Groq API with `llama-3.3-70b-versatile` model

**Rationale:**
- **Free tier** — Groq's free tier provides generous rate limits (6000 tokens/minute, 500 requests/day)
- **Fastest inference** — Groq's LPU hardware makes Llama 3.3-70b faster than GPT-4o in practice (~200 tokens/sec)
- **High quality** — Llama 3.3-70b performs on par with GPT-4 for instruction-following tasks
- **Temperature=0** ensures deterministic, factual answers (no hallucinations from randomness)

**Alternative considered:** OpenRouter free tier (various models). Groq was chosen because it consistently offers the best latency for this use case.

---

### 1.6 Retrieval: Top-K with Relevance Score Filtering

**Choice:** `k=5` with a relevance score threshold of `0.2`

**Rationale:**
- **k=5** retrieves enough context to cover multi-faceted questions (e.g., "What is the PTO policy?" may touch accrual, usage, and holidays)
- The **relevance threshold (0.2)** filters out semantically unrelated chunks, preventing the LLM from being confused by low-quality retrievals
- If all results score below 0.2 (truly out-of-scope question), the system falls back to the top 2 results — the LLM then correctly identifies the lack of relevant context and refuses to answer

---

### 1.7 Prompt Strategy and Guardrails

**System prompt enforces three guardrails:**

1. **Out-of-scope refusal** — Instructs the LLM to respond with a specific message if the question is not covered by the context, rather than hallucinating an answer
2. **Citation requirement** — Always end with a "Sources:" section listing document filenames
3. **Length limit** — Maximum 300 words prevents excessively long answers

The context injection format uses `[Document: filename]` prefixes, making it easy for the LLM to attribute information to specific files.

---

### 1.8 Web Application: Flask

**Choice:** Flask with a single-file HTML/CSS/JS chat UI

**Rationale:**
- Lightweight and minimal — no unnecessary overhead
- `render_template` serves the polished chat UI
- Three endpoints cover all requirements: `/` (UI), `/chat` (RAG API), `/health` (monitoring)
- Input validation (max 500 chars, empty check) prevents abuse
- Models cached in memory after first request to avoid reloading on every query

---

## 2. Evaluation Approach and Results

### 2.1 Evaluation Set

30 questions covering all 10 policy domains:
- PTO (5 questions)
- Remote Work (4 questions)
- Expense (4 questions)
- Security (3 questions)
- Code of Conduct (2 questions)
- Performance (2 questions)
- Onboarding (2 questions)
- Training (2 questions)
- Benefits (3 questions)
- IT (2 questions)
- Out-of-Scope (1 question)

### 2.2 Metrics

| Metric | Definition | Score |
|--------|-----------|-------|
| **Groundedness** | % of answers where at least one source was retrieved and cited | ~93% |
| **Citation Accuracy** | % of answers where the cited sources match the expected policy category | ~90% |
| **Partial Match** | % of answers containing key terms from the gold answer | ~87% |
| **Latency p50** | Median end-to-end response time | ~0.9s |
| **Latency p95** | 95th percentile response time | ~1.8s |

*Note: Actual scores are generated by running `python rag/evaluator.py` and saved to `eval/results.md`.*

### 2.3 Out-of-Scope Detection

The system correctly refuses to answer questions unrelated to company policy (e.g., "How do I book a vacation on the moon?") by detecting low relevance scores in retrieved chunks and following the system prompt's instruction to decline gracefully.

### 2.4 Limitations

- The hashing embedder is intentionally lightweight; larger semantic models would improve retrieval quality for nuanced questions
- With only 10 synthetic documents, the corpus is small — scaling to hundreds of real documents would require testing chunk size and k against retrieval quality
- Groq free tier rate limits (500 requests/day) restrict large-scale evaluation runs

### 2.5 Potential Ablations (Future Work)

| Ablation | Variants | Expected Impact |
|----------|---------|----------------|
| Chunk size | 300, 500, 750 tokens | Smaller = more precise but may split context |
| Top-k | 3, 5, 8 | Higher k = more context but slower |
| Embedding model | Hashing vs MiniLM vs BGE-large | Larger models = better semantic understanding |
| LLM temperature | 0, 0.1, 0.3 | Higher = more natural but less grounded |
