# app/insights.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.retrieve import get_retriever
from config import LLM_MODEL, DEVICE

def generate_insights():
    retriever = get_retriever(k=8)

    try:
        llm = ChatOllama(
            model=LLM_MODEL,
            temperature=0.2,
            device=DEVICE if DEVICE == "cuda" else None
        )
    except Exception as e:
        raise RuntimeError(f"❌ Ollama is not running or model '{LLM_MODEL}' is not loaded.\n"
                           f"   Please run 'ollama serve' in a new terminal and 'ollama pull {LLM_MODEL}'")

    prompt = ChatPromptTemplate.from_template("""You are a senior business analyst.
If the context is not a company document, reply: "Please upload a company/enterprise document (annual report, financial statement, etc.)."

Otherwise provide:
1. One-paragraph overall summary
2. Bullet points: Top revenue/financial highlights, Major risks, Key opportunities

Context:
{context}""")

    context_docs = retriever.invoke("Summarize the entire document")
    context = "\n\n".join(doc.page_content for doc in context_docs)

    response = (prompt | llm).invoke({"context": context})
    return response.content