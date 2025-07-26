import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from openai import OpenAI
from newspaper import Article

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def summarize_text(text, mode="bullet", language="English", length=5):
    prompt = (
        f"Summarize the following text in {language} as {length} {mode} points:\n\n{text}"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

def extract_keywords(text):
    prompt = f"Extract the top 10 keywords from the following text:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()


