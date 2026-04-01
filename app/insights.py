# app/insights.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.retrieve import get_retriever
from config import LLM_MODEL, DEVICE

def generate_insights():
    retriever = get_retriever(k=8)
    llm = ChatOllama(model=LLM_MODEL, temperature=0.2, device=DEVICE if DEVICE == "cuda" else None)

    prompt = ChatPromptTemplate.from_template("""Check if the context is a company/enterprise business document.
If not, reply ONLY: "Please upload a company or enterprise-related document (annual report, financial statement, business plan, etc.)."
Otherwise, give:
1. One-paragraph summary
2. Bullet points: Top revenue/financial highlights, Major risks, Key opportunities

Context:
{context}""")

    context_docs = retriever.invoke("Summarize the entire document")
    context = "\n\n".join(doc.page_content for doc in context_docs)

    response = (prompt | llm).invoke({"context": context})
    return response.content