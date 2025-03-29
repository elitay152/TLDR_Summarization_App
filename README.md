# 📝 TL;DR Summarization App
This project is a RESTful API built with FastAPI that uses the BART (Bidirectional and Auto-Regressive Transformers) model to generate concise summaries of journal articles. The goal is to streamline academic reading by providing high-quality, auto-generated summaries from long-form scholarly content.

## 🚀 Project Overview
#### 🔧 Technologies Used
- FastAPI – Lightweight Python framework for building APIs
- Hugging Face Transformers – BART model for abstractive summarization
- PyMuPDF (fitz) – PDF text extraction
- Uvicorn – ASGI server for running FastAPI

#### 🚀 How It Works
1. User uploads a PDF file via a simple web form or API call.
2. The app extracts the full text from the PDF.
3. The BART model generates a concise summary of the content.
4. The result is returned to the user.

## 📌 API Endpoints
##### GET /
Returns an HTML form to upload a PDF file.

- Purpose: Basic front-end for manual testing.
- Response: HTML page with upload input and loading animation.

##### POST /uploadfile/
Uploads and processes a PDF to generate a summary.

##### GET /summarize_pdf/
Alternative endpoint to summarize an existing PDF on the server by file path.

👩‍🔬 Use Cases
- Literature reviews for students and researchers
- Time-saving tool for clinicians reviewing research
