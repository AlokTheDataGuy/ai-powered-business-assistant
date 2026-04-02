# app/generate.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.retrieve import get_retriever
from config import LLM_MODEL, DEVICE

def get_rag_chain():
    retriever = get_retriever(k=6)

    try:
        llm = ChatOllama(
            model=LLM_MODEL,
            temperature=0.3,
            device=DEVICE if DEVICE == "cuda" else None
        )
    except Exception as e:
        raise RuntimeError(f"❌ Ollama is not running or model '{LLM_MODEL}' is not loaded.\n"
                           f"   Please run 'ollama serve' in a new terminal and 'ollama pull {LLM_MODEL}'")

    template = """You are a helpful business analyst.
Answer using ONLY the context below.
If the question is not relevant to business documents, reply: "Please ask a relevant business question about the company document."

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain