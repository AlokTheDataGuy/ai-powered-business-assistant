# ui/app.py
import streamlit as st
import requests
import os
from pathlib import Path

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Business Assistant", page_icon="🏢", layout="wide")
st.title("🏢 Business Document Assistant")
st.markdown("Upload a document → Ask questions → Get insights")

# Sidebar
with st.sidebar:
    st.header("📁 Document Upload")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    
    if st.button("Process Documents", type="primary"):
        if uploaded_files:
            with st.spinner("Processing documents... This may take a while for large files"):
                files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                
                try:
                    response = requests.post(f"{API_URL}/upload-docs", files=files)
                    if response.status_code == 200:
                        result = response.json()
                        st.success(result["message"])
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please upload at least one file")

# Main area - Tabs
tab1, tab2 = st.tabs(["💬 Ask Questions", "📊 Insights"])

with tab1:
    st.subheader("Ask questions about your documents")
    question = st.text_input("Enter your question:", 
                            placeholder="What are the key financial highlights?")
    
    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{API_URL}/query", json={"question": question})
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown("### Answer")
                        st.write(result["answer"])
                    else:
                        st.error("Failed to get answer")
                except Exception as e:
                    st.error(f"Could not connect to backend: {e}")
        else:
            st.warning("Please enter a question")

with tab2:
    st.subheader("Business Insights & Summary")
    if st.button("Generate Insights"):
        with st.spinner("Generating insights..."):
            try:
                response = requests.get(f"{API_URL}/insights")
                if response.status_code == 200:
                    result = response.json()
                    st.markdown(result["insights"])
                else:
                    st.error("Failed to generate insights")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

# Footer
st.caption("Powered by local RAG • 100% free & private")

# Run with: streamlit run ui/app.py