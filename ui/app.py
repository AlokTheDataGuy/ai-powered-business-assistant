# ui/app.py
import streamlit as st
import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))  # adds project root to path

from config import MAX_PAGES_WARNING

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Business Assistant", page_icon="🏢", layout="wide")

# BIG TITLE
st.markdown("# 🏢 Business Document Assistant")
st.markdown("**Upload your company document → Ask questions → Get instant insights**")

# Instructions (side panel)
with st.sidebar:
    st.header("📋 How to use")
    st.markdown(f"""
    1. Upload **one company/enterprise document** (PDF or TXT)
    2. Click **Process Document**
    3. Ask questions or click **Generate Insights**
    
    **Accepted documents:**
    - Annual reports
    - Financial statements
    - Business plans
    - Quarterly updates
    - Strategy documents
    
    **Note:** Files with more than **{MAX_PAGES_WARNING} pages** may take longer.
    Only business/company documents work best.
    """)

# Main page file uploader
st.subheader("📤 Upload your document")
uploaded_files = st.file_uploader(
    "Choose PDF or TXT file (company reports work best)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

process_button = st.button("🚀 Process Document", type="primary", disabled=not uploaded_files)

if process_button and uploaded_files:
    with st.spinner("Processing your document... (GPU is being used if available)"):
        files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
        try:
            response = requests.post(f"{API_URL}/upload-docs", files=files)
            if response.status_code == 200:
                st.success("✅ Document processed successfully! You can now ask questions or get insights.")
            else:
                st.error(f"❌ {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Could not connect to the system. Make sure the backend is running.")

# Tabs (chat disabled until processed)
tab1, tab2 = st.tabs(["💬 Ask Questions", "📊 Get Insights"])

with tab1:
    st.subheader("Ask any business question")
    question = st.text_input("Type your question here:", 
                             placeholder="What are the key revenue highlights?")
    
    if st.button("Get Answer", disabled=not uploaded_files):
        if question:
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(f"{API_URL}/query", json={"question": question})
                    if resp.status_code == 200:
                        st.markdown("### Answer")
                        st.write(resp.json()["answer"])
                    else:
                        st.error(f"❌ {resp.json().get('detail', 'Something went wrong')}")
                except:
                    st.error("❌ Backend not running. Start it with: `uvicorn api.main:app --reload`")
        else:
            st.warning("Please type a question")

with tab2:
    st.subheader("Business Summary & Insights")
    if st.button("Generate Insights", disabled=not uploaded_files):
        with st.spinner("Creating insights..."):
            try:
                resp = requests.get(f"{API_URL}/insights")
                if resp.status_code == 200:
                    st.markdown(resp.json()["insights"])
                else:
                    st.error(f"❌ {resp.json().get('detail', 'Something went wrong')}")
            except:
                st.error("❌ Backend not running.")

st.caption("💡 Powered by local AI • 100% free • Runs on your GPU if available")