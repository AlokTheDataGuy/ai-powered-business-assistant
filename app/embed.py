# app/embed.py
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List

# Configuration
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"   # Best free model for business RAG
VECTORSTORE_PATH = "vectorstore"
COLLECTION_NAME = "business_docs"

def embed_and_store(chunks: List[Document]):
    """
    Create embeddings and store in ChromaDB (persistent).
    """
    if not chunks:
        print("⚠️  No chunks to embed.")
        return None

    print(f"🔢 Creating embeddings using {EMBEDDING_MODEL}...")
    print(f"   (This may take 10-60 seconds depending on your docs & CPU)")

    # Load embedding model (downloads automatically first time)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Create or load Chroma vectorstore
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTORSTORE_PATH
    )

    # Add documents (Chroma handles duplicates intelligently)
    vectorstore.add_documents(chunks)
    
    print(f"✅ Vectorstore created/updated with {len(chunks)} chunks")
    print(f"   Stored in: {VECTORSTORE_PATH}/")
    return vectorstore


# For quick testing (run this file directly)
if __name__ == "__main__":
    from app.ingest import ingest_documents
    from app.preprocess import preprocess_documents
    
    # Chain everything
    raw_docs = ingest_documents()
    if raw_docs:
        chunks = preprocess_documents(raw_docs)
        if chunks:
            vectorstore = embed_and_store(chunks)
            print("\n✅ Test complete! You can now use the vectorstore for retrieval.")