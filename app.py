import openai
import streamlit as st
from utils import (
    extract_text_from_pdf,
    extract_text_from_url,
    summarize_text,
    extract_keywords
)
import base64

from dotenv import load_dotenv
import os
st.set_page_config(
    page_title="🧠 AI Text Summarizer",
    layout="centered",
    initial_sidebar_state="auto"
)


st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📄 AI-Powered Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload a PDF, enter text, or paste a URL to get a clean, bullet-point or paragraph summary powered by GPT-4.</p>", unsafe_allow_html=True)
st.markdown("---")

# Input choice
option = st.radio("Choose Input Type", ["Upload PDF", "Paste Text", "Enter URL"])

text = ""

if option == "Upload PDF":
    pdf_file = st.file_uploader("📄 Upload a PDF file", type=["pdf"])
    if pdf_file is not None:
        text = extract_text_from_pdf(pdf_file)
        st.success("✅ Text extracted from PDF successfully!")

elif option == "Paste Text":
    text = st.text_area("📝 Paste your text here", height=250)

elif option == "Enter URL":
    url = st.text_input("🔗 Enter article/blog URL")
    if url:
        try:
            text = extract_text_from_url(url)
            st.success("✅ Text extracted from the URL successfully!")
        except Exception as e:
            st.error(f"❌ Failed to extract text: {e}")

# Sidebar options
st.sidebar.header("⚙️ Settings")
mode = st.sidebar.selectbox("Summary Style", ["bullet", "paragraph"])
language = st.sidebar.selectbox("Summary Language", ["English", "Hindi", "French", "Spanish", "German"])
length = st.sidebar.slider("Number of summary points", min_value=3, max_value=10, value=5)


if st.button("✨ Generate Summary"):
    if text:
        with st.spinner("⏳ Generating summary..."):
            summary = summarize_text(text, mode=mode, language=language, length=length)
        st.subheader("📌 Summary")
        st.markdown(summary)

        
        def download_link(text, filename="summary.txt"):
            b64 = base64.b64encode(text.encode()).decode()
            return f'<a href="data:text/plain;base64,{b64}" download="{filename}">📥 Download Summary</a>'
        
        st.markdown(download_link(summary), unsafe_allow_html=True)

        if st.checkbox("🔑 Show Keywords"):
            with st.spinner("Extracting keywords..."):
                keywords = extract_keywords(text)
            st.markdown(f"**Keywords:** {keywords}")
    else:
        st.warning("Please provide input text first.")

