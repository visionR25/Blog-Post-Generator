# This script is used to extract text from PDF files and URLs.
# It uses PyPDF2 for PDF extraction and Newspaper3k for URL extraction.
# Import necessary libraries

from pypdf import PdfReader
from newspaper import Article

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text[:4000]  # Limit input for token safety

def extract_text_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text[:4000]
