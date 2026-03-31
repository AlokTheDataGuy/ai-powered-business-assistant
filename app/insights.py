# app/insights.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.retrieve import get_retriever

LLM_MODEL = "llama3.1:8b"

def generate_insights():
    """
    Generates a short summary + key business insights from all documents.
    Perfect for your single-file future use.
    """
    retriever = get_retriever(k=8)   # more context for insights
    
    llm = ChatOllama(model=LLM_MODEL, temperature=0.2)

    prompt = ChatPromptTemplate.from_template("""You are a senior business analyst.
Provide a clear, short response with bullet points.

1. One-paragraph overall summary of the document(s).
2. Key insights in these categories:
   - Top revenue segments / financial highlights
   - Major risks or challenges mentioned
   - Key opportunities or strategic points

Context:
{context}

Answer in simple business language:""")

    # Get context
    context_docs = retriever.invoke("Summarize the entire document")
    context = "\n\n".join(doc.page_content for doc in context_docs)

    chain = prompt | llm
    response = chain.invoke({"context": context})

    print("📊 INSIGHTS GENERATED")
    print(response.content)
    return response.content


# Quick test
if __name__ == "__main__":
    generate_insights()