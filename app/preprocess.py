# app/preprocess.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

def preprocess_documents(documents: List[Document], 
                         chunk_size: int = 500, 
                         chunk_overlap: int = 100) -> List[Document]:
    """
    Clean and split documents into smaller chunks.
    """
    if not documents:
        print("⚠️  No documents to preprocess.")
        return []

    print(f"🔪 Splitting {len(documents)} documents into chunks...")

    # Simple cleaning: remove excessive whitespace
    cleaned_docs = []
    for doc in documents:
        cleaned_text = " ".join(doc.page_content.split())  # removes extra spaces/newlines
        cleaned_doc = Document(
            page_content=cleaned_text,
            metadata=doc.metadata
        )
        cleaned_docs.append(cleaned_doc)

    # Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_documents(cleaned_docs)

    print(f"✅ Created {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    return chunks


# For quick testing (run this file directly after ingest)
if __name__ == "__main__":
    from app.ingest import ingest_documents
    
    raw_docs = ingest_documents()
    if raw_docs:
        chunks = preprocess_documents(raw_docs)
        if chunks:
            print(f"\nExample chunk:\n{chunks[0].page_content[:300]}...")
            print(f"Metadata: {chunks[0].metadata}")