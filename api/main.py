# api/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from app.ingest import ingest_documents
from app.preprocess import preprocess_documents
from app.embed import embed_and_store
from app.generate import get_rag_chain
from app.insights import generate_insights
from config import RAW_DIR

app = FastAPI(title="Business RAG Assistant")

RAW_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-docs")
async def upload_docs(files: list[UploadFile] = File(...)):
    for file in files:
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(400, "Only PDF and TXT files are allowed")
        with open(RAW_DIR / file.filename, "wb") as f:
            shutil.copyfileobj(file.file, f)

    try:
        docs = ingest_documents()
        chunks = preprocess_documents(docs)
        embed_and_store(chunks)
        return {"status": "success", "message": f"Processed {len(files)} file(s)"}
    except Exception as e:
        raise HTTPException(500, f"Something went wrong: {str(e)}")


@app.post("/query")
async def query_document(question: str):
    if not question or len(question.strip()) < 5:
        raise HTTPException(400, "Please ask a proper question (minimum 5 characters)")
    try:
        chain = get_rag_chain()
        answer = chain.invoke(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.get("/insights")
async def get_insights():
    try:
        insights = generate_insights()
        return {"status": "success", "insights": insights}
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Business Assistant API is ready"}