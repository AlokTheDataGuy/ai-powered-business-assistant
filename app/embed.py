# app/embed.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
from config import EMBEDDING_MODEL, VECTORSTORE_PATH, DEVICE

def embed_and_store(chunks: List[Document]):
    if not chunks:
        return None

    print(f"🔢 Creating embeddings on {DEVICE.upper()}...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': DEVICE},
        encode_kwargs={'normalize_embeddings': True}
    )

    vectorstore = Chroma(
        collection_name="business_docs",
        embedding_function=embeddings,
        persist_directory=str(VECTORSTORE_PATH)
    )

    vectorstore.add_documents(chunks)
    print(f"✅ Vectorstore updated with {len(chunks)} chunks on {DEVICE.upper()}")
    return vectorstore