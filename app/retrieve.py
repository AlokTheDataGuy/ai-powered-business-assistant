# app/retrieve.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.retrievers import BaseRetriever

# Same config as embed.py
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
VECTORSTORE_PATH = "vectorstore"
COLLECTION_NAME = "business_docs"

def get_retriever(k: int = 6) -> BaseRetriever:
    """
    Load the vectorstore and return a retriever.
    Works with multiple documents or single document.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTORSTORE_PATH
    )

    # Retriever (you can later filter by metadata["source"] for single-file use)
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    print(f"✅ Retriever ready (top-{k} results)")
    return retriever


# For quick testing (run this file directly)
if __name__ == "__main__":
    retriever = get_retriever()
    
    # Quick test query
    test_query = "What is the main topic of the document?"
    print(f"\n🔍 Testing query: '{test_query}'")
    results = retriever.invoke(test_query)
    
    if results:
        print(f"✅ Retrieved {len(results)} relevant chunks")
        print(f"First chunk preview:\n{results[0].page_content[:200]}...")
        print(f"Source: {results[0].metadata.get('source', 'unknown')}")
    else:
        print("No results found.")