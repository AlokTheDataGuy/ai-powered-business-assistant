# 🏢 Business Document Assistant

> A **local-first RAG system** for querying enterprise documents — annual reports, 10-Ks, strategy decks — without sending a single byte to the cloud.

Built for **analysts, founders, and finance teams** who need to extract insights from dense corporate PDFs but can't (or won't) upload them to ChatGPT.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green)](https://langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📸 Demo

| Q&A Interface | Auto-Generated Insights |
|---------------|--------------------------|
| ![Q&A](./screenshots/question.png) | ![Insights](./screenshots/insights.png) |

---

## 🎯 Why This Project?

Most "chat with your PDF" tools fail on real business documents because:
1. They send sensitive financials to third-party APIs (compliance nightmare)
2. They struggle with multi-page financial tables and footnotes
3. They give generic answers instead of structured business insights

This project addresses all three: **runs 100% locally, optimized for financial documents, and produces analyst-grade structured insights** (revenue trends, risks, opportunities) on demand.

---

## ✨ Key Features

- 🔒 **Fully local & private** — Ollama + ChromaDB, zero external API calls
- 📊 **Structured insights mode** — auto-generates revenue/risk/opportunity summaries
- ⚡ **GPU acceleration** — 5–10× faster embeddings on CUDA-enabled GPUs
- 📄 **Multi-document support** — query across multiple reports simultaneously
- 🧠 **Smart chunking** — preserves table structure and section context
- 🚀 **FastAPI + Streamlit** — clean separation of inference backend and UI

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Streamlit UI   │ ───▶ │  FastAPI Backend │ ───▶ │   Ollama LLM    │
│  (port 8501)    │      │   (port 8000)    │      │  (llama3.1:8b)  │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Retrieval Layer │
                         │  ┌────────────┐  │
                         │  │  ChromaDB  │  │ ◀── BGE-base embeddings
                         │  │  (vectors) │  │
                         │  └────────────┘  │
                         └──────────────────┘
                                  ▲
                                  │
                         ┌──────────────────┐
                         │  Ingestion Layer │
                         │  PyMuPDF + chunk │
                         └──────────────────┘
```

**Pipeline:** PDF → PyMuPDF text extraction → recursive chunking (512 tokens, 50 overlap) → BGE embeddings → ChromaDB → top-k retrieval → Ollama generation

---

## 🛠️ Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| **LLM** | Ollama (`llama3.1:8b` / `phi4:3.8b`) | Local inference, no API costs, privacy-preserving |
| **Embeddings** | `BAAI/bge-base-en-v1.5` | Top-tier retrieval quality on MTEB, runs locally |
| **Vector DB** | ChromaDB | Lightweight, persistent, no server setup |
| **Orchestration** | LangChain 0.3 | Mature RAG primitives, easy to extend |
| **PDF Parsing** | PyMuPDF | Fastest Python PDF library, handles tables better than pdfplumber for our use case |
| **Backend** | FastAPI | Async, type-safe, easy to containerize later |
| **Frontend** | Streamlit | Rapid prototyping for ML demos |
| **Acceleration** | PyTorch CUDA | Auto-detected; falls back to CPU gracefully |

---

## 📊 Performance

Tested on Infosys Annual Report 2024-25 (~280 pages, RTX 3060 6GB):

| Stage | CPU (i5-11th gen) | GPU (RTX 3060) |
|-------|-------------------|----------------|
| Document ingestion | ~95s | ~18s |
| First embedding | ~120s | ~22s |
| Avg query latency | ~8s | ~3s |
| Insights generation | ~25s | ~9s |

> Numbers will vary by hardware and document size. CPU mode is fully supported but noticeably slower.

---

## 🚀 Quick Start

### 1. Install Ollama

Download from [ollama.com](https://ollama.com), then:

```bash
ollama pull llama3.1:8b      # ~4.7 GB — recommended
# or for lower-RAM machines:
ollama pull phi4:3.8b        # ~2.2 GB
```

### 2. Setup

```bash
git clone https://github.com/<your-username>/business-doc-assistant.git
cd business-doc-assistant

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
python check_gpu.py               # optional GPU sanity check
```

### 3. Run

```bash
# Terminal 1 — backend
uvicorn api.main:app --reload

# Terminal 2 — UI
streamlit run ui/app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## 📋 Usage

1. Drop your PDF into `data/raw/` (or upload via UI)
2. Click **🚀 Process Document**
3. Choose your mode:
   - **Ask Questions** — free-form Q&A
   - **Get Insights** — one-click structured summary (revenue, risks, opportunities)

**Sample documents to test:**
- [Infosys Annual Report 2024-25](https://www.infosys.com/investors/reports-filings/annual-report/annual/documents/infosys-ar-24.pdf)
- [Tesla Q3 2023 Update](https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q3-2023-Update.pdf)

---

## 📁 Project Structure

```
business-doc-assistant/
├── app/                    # Core RAG pipeline
│   ├── ingest.py           # PDF/TXT loading
│   ├── preprocess.py       # Chunking & cleaning
│   ├── embed.py            # BGE embedding wrapper
│   ├── retrieve.py         # ChromaDB query interface
│   ├── generate.py         # Ollama generation
│   └── insights.py         # Structured insights prompt chain
├── api/main.py             # FastAPI endpoints
├── ui/app.py               # Streamlit interface
├── config.py               # Centralized config + GPU detection
├── check_gpu.py            # CUDA availability test
├── data/raw/               # Input documents
├── vectorstore/            # ChromaDB persistence (gitignored)
├── screenshots/            # Demo images
├── requirements.txt
└── README.md
```

---

## 🔍 Engineering Decisions

A few design choices worth calling out:

**Why local embeddings (BGE) over OpenAI?**
Privacy was the core requirement, but BGE-base also matches `text-embedding-3-small` on most retrieval benchmarks at zero cost.

**Why Ollama over llama.cpp directly?**
Ollama abstracts model management and exposes a clean HTTP API, which made backend integration trivial. Trade-off: slightly less control over inference parameters.

**Why ChromaDB over FAISS or Pinecone?**
ChromaDB persists to disk out of the box, has metadata filtering, and requires zero infrastructure. FAISS would be faster at scale but adds complexity for a single-user tool. Pinecone breaks the local-first promise.

**Chunking strategy:**
RecursiveCharacterTextSplitter at 512 tokens with 50-token overlap. Tested 256/1024 — 512 was the sweet spot for retrieving complete financial table rows without diluting embedding signal.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `CUDA not available` | Run `python check_gpu.py`. CPU fallback works fine, just slower. |
| Backend connection refused | Confirm FastAPI terminal is running on port 8000. |
| First query is slow | Embedding model downloads on first run (~440 MB). Cached afterward. |
| Ollama timeout | Increase timeout in `config.py` or pull a smaller model (`phi4:3.8b`). |
| Out-of-memory on GPU | Switch to `phi4:3.8b` or set `DEVICE=cpu` in `config.py`. |

---

## 🛣️ Roadmap

- [ ] **Citation highlighting** — show source page numbers in answers
- [ ] **Multi-doc comparison** — "compare risks in 2023 vs 2024 reports"
- [ ] **Financial table extraction** — dedicated table-aware retriever
- [ ] **Conversation memory** — multi-turn dialogue with context
- [ ] **Eval suite** — benchmark retrieval quality on a labeled QA set
- [ ] **Docker compose** — one-command deployment

---

## 📄 License

MIT — use it, modify it, ship it.

---

## 👤 Author

Built by Alok — exploring the intersection of NLP, RAG, and practical business tooling.

[LinkedIn](https://linkedin.com/in/alokthedataguy) · [Portfolio](https://alok-deep.vercel.app/) · [Email](alokdeep9925@gmail.com)

---

⭐ **Star this repo** if you find it useful. Issues and PRs welcome.
