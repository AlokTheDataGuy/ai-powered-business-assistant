# app/generate.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.retrieve import get_retriever
from config import LLM_MODEL, DEVICE

def get_rag_chain():
    retriever = get_retriever(k=6)
    llm = ChatOllama(model=LLM_MODEL, temperature=0.3, device=DEVICE if DEVICE == "cuda" else None)

    # Validation + Answer prompt
    template = """You are a business analyst.
First, check if the question is relevant to company/enterprise documents.
If the question is vague, unrelated, or not about business (revenue, risks, strategy, etc.), reply ONLY with: "Please ask a relevant business question about the company document."
Otherwise, answer using ONLY the context.

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