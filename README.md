# PolicyBot — RAG-Powered Policy Q&A

A Retrieval-Augmented Generation (RAG) application that answers employee questions about Acme Corporation's company policies, with source citations and snippets.

---

## Tech Stack

| Component | Choice | Reason |
|---|---|---|
| LLM | Groq (llama-3.3-70b-versatile) | Free tier, extremely fast |
| Embeddings | Lightweight local hashing embedder | Free, runs locally, no API key needed |
| Vector Store | Local JSON index | Free, zero setup, persistent |
| Framework | LangChain | Best RAG ecosystem |
| Web App | Flask | Lightweight, simple |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/imajawad/policy-rag.git
cd policy-rag
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# macOS/Linux:
cp .env.example .env
# Windows PowerShell:
Copy-Item .env.example .env
# Edit .env and add your GROQ_API_KEY
# Get a free key at: https://console.groq.com
```

### 5. Ingest policy documents (first time only)
```bash
python rag/ingest.py
```
This loads all 10 policy documents from `policies/`, chunks them, embeds them with a lightweight local model, and stores them in `chroma_db/index.json`. The first run is quick and does not download any model weights.

### 6. Run the application
```bash
python app.py
```
Open your browser at: **http://localhost:5000**

---

## Project Structure

```
policy-rag/
├── app.py                    # Flask web app (/, /chat, /health)
├── rag/
│   ├── ingest.py             # Document ingestion pipeline
│   ├── retriever.py          # RAG retrieval + generation
│   └── evaluator.py          # Evaluation script
├── policies/                 # 10 synthetic policy markdown files
├── chroma_db/                # Auto-created local vector index
├── templates/
│   └── index.html            # Chat UI
├── eval/
│   ├── questions.json        # 30 evaluation questions
│   └── results.md            # Evaluation results (auto-generated)
├── tests/
│   └── test_app.py           # Pytest smoke tests
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI pipeline
├── requirements.txt
├── .env.example
├── README.md
├── design-and-evaluation.md
└── ai-tooling.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Chat web interface |
| POST | `/chat` | Query the RAG system |
| GET | `/health` | Health check |

### POST /chat

**Request:**
```json
{ "question": "How many vacation days do I get per year?" }
```

**Response:**
```json
{
  "answer": "Full-time employees in their first year receive 15 days of PTO... Sources: pto-policy.md",
  "sources": ["pto-policy.md"],
  "snippets": [{ "source": "pto-policy.md", "text": "...", "score": 0.87 }],
  "latency": 0.82,
  "status": "ok"
}
```

---

## Running Evaluation

```bash
# Make sure the app and vector store are set up first
python rag/evaluator.py
# Results saved to eval/results.md
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Deployment (Render)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build command:** `pip install -r requirements.txt && python rag/ingest.py`
   - **Start command:** `gunicorn app:app`
5. Add environment variable: `GROQ_API_KEY=your_key`
6. Deploy!

---

## Policies Covered

- PTO & Leave Policy
- Remote Work Policy
- Expense Reimbursement Policy
- Information Security Policy
- Code of Conduct & Ethics
- Performance Management Policy
- IT Acceptable Use Policy
- Employee Onboarding Policy
- Training & Development Policy
- Health & Benefits Policy
