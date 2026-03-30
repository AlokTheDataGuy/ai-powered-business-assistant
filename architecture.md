# 📌 Objective

Build an AI system that:

- Answers questions from business documents
- Generates summaries and insights

---

## 🏗️ Architecture
```
[Documents (PDF/TXT)]
        ↓
[Text Extraction]
        ↓
[Chunking]
        ↓
[Embeddings Model]
        ↓
[Vector Database]
        ↓
[Retriever + LLM (RAG)]
        ↓
[FastAPI Backend]
        ↓
[Streamlit UI]
```

---

## 🔧 Component Breakdown

### 1. Data Ingestion
- **Input:** PDFs, TXT files
- **Tools:** PyMuPDF / pdfplumber
- **Output:** Raw extracted text

### 2. Preprocessing
- Clean text (remove noise, headers)
- Split into chunks (200–500 tokens)
- Store chunks locally

### 3. Embeddings + Storage
- Convert text → vectors
- **Tools:** OpenAI Embeddings OR SentenceTransformers
- **Store in:** FAISS (simple, local)

### 4. Retrieval Layer
- **Input:** User query
- **Process:**
  - Convert query → embedding
  - Retrieve top-k relevant chunks

### 5. Generation (LLM)
- **Input:** Retrieved chunks + query
- **Output:** Final answer
- **Tools:** OpenAI / Gemini

### 6. Insights Layer ⚠️ *(important)*
- **Extra processing:**
  - Summarization
  - Key points extraction
- **Examples:**
  - "Top revenue segments"
  - "Major risks identified"

### 7. Backend API (FastAPI)

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload-docs` | Upload + process documents |
| `POST` | `/query` | Ask questions |
| `GET` | `/insights` | Generate summary insights |

### 8. UI (Streamlit)
- Upload documents
- Ask questions
- View:
  - Answers
  - Insights

---

## 📁 Folder Structure
```
rag-system/
│
├── data/
│   ├── raw/              # uploaded docs
│   └── processed/        # cleaned + chunked text
│
├── embeddings/
│   └── vector_store/     # FAISS index
│
├── app/
│   ├── ingest.py         # document loading + extraction
│   ├── preprocess.py     # cleaning + chunking
│   ├── embed.py          # embeddings + storage
│   ├── retrieve.py       # similarity search
│   ├── generate.py       # LLM response
│   └── insights.py       # summaries
│
├── api/
│   └── main.py           # FastAPI app
│
├── ui/
│   └── app.py            # Streamlit interface
│
└── requirements.txt
```

---

## 🧠 MVP Strategy

**Start with:**
- 1–2 PDFs
- Basic Q&A

**Then add:**
- Insights layer
- Better prompts

---

## 🔄 Future Extensions

- Multi-document comparison
- Chat history (memory)
- Role-based responses
- Hybrid search