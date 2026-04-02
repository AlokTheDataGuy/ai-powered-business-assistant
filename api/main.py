# api/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from pydantic import BaseModel

# Import our modules
from app.ingest import ingest_documents
from app.preprocess import preprocess_documents
from app.embed import embed_and_store
from app.generate import get_rag_chain
from app.insights import generate_insights
from config import RAW_DIR

app = FastAPI(title="Business RAG Assistant")

RAW_DIR.mkdir(parents=True, exist_ok=True)

# Pydantic model for /query
class QueryRequest(BaseModel):
    question: str

@app.post("/upload-docs")
async def upload_docs(files: list[UploadFile] = File(...)):
    # Clear old files (single-document mode)
    for old_file in RAW_DIR.glob("*.*"):
        if old_file.is_file():
            old_file.unlink()

    saved_files = []
    for file in files:
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(400, "Only PDF and TXT files allowed")
        
        with open(RAW_DIR / file.filename, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(file.filename)

    try:
        raw_docs = ingest_documents()
        chunks = preprocess_documents(raw_docs)
        embed_and_store(chunks)
        return {"status": "success", "message": f"✅ Processed {len(saved_files)} new file(s)"}
    except Exception as e:
        raise HTTPException(500, f"Something went wrong: {str(e)}")


@app.post("/query")
async def query_document(request: QueryRequest):
    if not request.question or len(request.question.strip()) < 5:
        raise HTTPException(400, "Please ask a proper question (minimum 5 characters)")
    
    try:
        chain = get_rag_chain()
        answer = chain.invoke(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(500, f"Error generating answer: {str(e)}")


@app.get("/insights")
async def get_insights():
    try:
        insights = generate_insights()
        return {"status": "success", "insights": insights}
    except Exception as e:
        raise HTTPException(500, f"Error generating insights: {str(e)}")


@app.get("/")
async def root():
    return {"message": "✅ Business Assistant API is running"}