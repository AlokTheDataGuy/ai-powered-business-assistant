# app/generate.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.retrieve import get_retriever

# LLM Setup (free & local)
LLM_MODEL = "llama3.1:8b"   # Change to "phi4:3.8b" if your laptop is slower

def get_rag_chain():
    """
    Creates a simple RAG chain: query → retrieve chunks → LLM answer
    """
    retriever = get_retriever(k=6)

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0.3,        # low temperature = more factual
        num_predict=1024
    )

    # Business-friendly prompt
    template = """You are a helpful business analyst.
Answer the question using ONLY the provided context.
If you don't know, say "I don't have enough information."

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


# Quick test
if __name__ == "__main__":
    chain = get_rag_chain()
    
    test_query = "What is the main topic or summary of the document?"
    print(f"\n🔍 Asking: {test_query}")
    print("-" * 60)
    
    answer = chain.invoke(test_query)
    print(answer)