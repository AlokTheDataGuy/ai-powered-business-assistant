# ui/app.py
import streamlit as st
import requests
from config import MAX_PAGES_WARNING

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Business Assistant", page_icon="🏢", layout="wide")

st.markdown("# 🏢 Business Document Assistant")
st.markdown("**Upload → Ask questions → Get insights**")

# Sidebar instructions
with st.sidebar:
    st.header("📋 How to use")
    st.markdown(f"""
    1. Upload **one company document** (PDF/TXT)
    2. Click **Process Document**
    3. Ask questions or get insights

    **Accepted:**
    - Annual reports, financial statements, business plans
    - Max recommended: {MAX_PAGES_WARNING} pages

    Make sure **both terminals** are running!
    """)

# File uploader in main area
st.subheader("📤 Upload your document")
uploaded_files = st.file_uploader("Choose PDF or TXT (company report best)", 
                                  type=["pdf", "txt"], accept_multiple_files=True)

if st.button("🚀 Process Document", type="primary", disabled=not uploaded_files):
    with st.spinner("Processing on GPU..."):
        files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
        try:
            resp = requests.post(f"{API_URL}/upload-docs", files=files)
            if resp.status_code == 200:
                st.success(resp.json()["message"])
            else:
                st.error(f"❌ {resp.json().get('detail', 'Upload failed')}")
        except:
            st.error("❌ Cannot connect to backend. Start it with: `uvicorn api.main:app --reload`")

# Tabs
tab1, tab2 = st.tabs(["💬 Ask Questions", "📊 Insights"])

with tab1:
    st.subheader("Ask any business question")
    question = st.text_input("Type your question here:", 
                             placeholder="What are the top revenue segments?")
    
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
                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend not running! Start it in another terminal.")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
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
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running! Start it in another terminal.")
            except Exception as e:
                st.error(f"❌ {str(e)}")

st.caption("💡 100% local • Runs on your GPU • Private")