# app/retrieve.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.retrievers import BaseRetriever
from config import EMBEDDING_MODEL, VECTORSTORE_PATH, DEVICE

def get_retriever(k: int = 6) -> BaseRetriever:
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

    return vectorstore.as_retriever(search_kwargs={"k": k})