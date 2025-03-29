# 📝 TL;DR Summarization App
This project is a RESTful API built with FastAPI that uses the BART (Bidirectional and Auto-Regressive Transformers) model to generate concise summaries of journal articles. The goal is to streamline academic reading by providing high-quality, auto-generated summaries from long-form scholarly content.

### 🚀 Project Overview
##### 🤖 Model Used: BART (Hugging Face Transformers)
##### 🧠 Architecture: BART combines BERT’s bidirectional encoder with GPT’s autoregressive decoder.
##### 🌐 API Framework: FastAPI for rapid, scalable backend development.
##### 🧰 Tech Stack
- FastAPI	For building the REST API
- Transformers	Hugging Face Transformers library (BART)
- uvicorn	ASGI server for running FastAPI

📦 API Endpoints:
- POST /summarize: Takes in a long text input (journal article) and returns a summarized version.

👩‍🔬 Use Cases
- Literature reviews for students and researchers
- Time-saving tool for clinicians reviewing research
