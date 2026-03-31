# app/ingest.py
import os
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_core.documents import Document
from tqdm import tqdm

def ingest_documents(raw_dir: str = "data/raw") -> list[Document]:
    """
    Load all PDFs and TXT files from data/raw.
    Returns a list of LangChain Document objects.
    """
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        os.makedirs(raw_path, exist_ok=True)
        print(f"✅ Created empty folder: {raw_path}")
        return []

    documents = []
    # Get all PDF and TXT files
    pdf_files = list(raw_path.glob("*.pdf"))
    txt_files = list(raw_path.glob("*.txt"))

    all_files = pdf_files + txt_files

    if not all_files:
        print("⚠️  No PDF or TXT files found in data/raw/")
        return []

    print(f"📄 Found {len(all_files)} document(s). Loading...")

    for file_path in tqdm(all_files, desc="Loading documents"):
        try:
            if file_path.suffix.lower() == ".pdf":
                loader = PyMuPDFLoader(str(file_path))
            else:  # .txt
                loader = TextLoader(str(file_path), encoding="utf-8")

            docs = loader.load()
            documents.extend(docs)

        except Exception as e:
            print(f"❌ Failed to load {file_path.name}: {e}")

    print(f"✅ Successfully loaded {len(documents)} document chunks from {len(all_files)} files.")
    return documents


# For quick testing (run this file directly)
if __name__ == "__main__":
    docs = ingest_documents()
    if docs:
        print(f"\nExample from first document:\n{docs[0].page_content[:300]}...")