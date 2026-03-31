# api/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from typing import List

# Import our app modules
from app.ingest import ingest_documents
from app.preprocess import preprocess_documents
from app.embed import embed_and_store
from app.generate import get_rag_chain
from app.insights import generate_insights

app = FastAPI(title="Business RAG Assistant")

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-docs")
async def upload_docs(files: List[UploadFile] = File(...)):
    """Upload one or more PDFs/TXT files"""
    saved_files = []
    
    for file in files:
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(status_code=400, detail="Only PDF and TXT files allowed")
        
        file_path = UPLOAD_DIR / file.filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_files.append(file.filename)
    
    # Process the uploaded files
    try:
        raw_docs = ingest_documents()
        chunks = preprocess_documents(raw_docs)
        vectorstore = embed_and_store(chunks)
        
        return JSONResponse({
            "status": "success",
            "message": f"Successfully processed {len(saved_files)} file(s)",
            "files": saved_files,
            "chunks": len(chunks)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_document(question: str):
    """Ask a question about the documents"""
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    
    try:
        chain = get_rag_chain()
        answer = chain.invoke(question)
        
        return {
            "question": question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/insights")
async def get_insights():
    """Generate summary and business insights"""
    try:
        insights = generate_insights()
        return {
            "status": "success",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Business RAG API is running 🚀"}


# Run with: uvicorn api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)