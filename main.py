from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from transformers import BartForConditionalGeneration, BartTokenizer
import fitz  # PyMuPDF for extracting text from PDFs
import textwrap
import os
from typing import Annotated

# Create a FastAPI application instance
app = FastAPI()

def extract_text_from_pdf(pdf_bytes):
    # Open the PDF file from bytes
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def text_summarizer_from_pdf(pdf_text):
    """
    Generates a summary from the text of a PDF file.

    Parameters:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Summarized text.
    """

    # Load the pre-trained BART model and tokenizer
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)

    # Tokenize the text and prepare it for the model
    inputs = tokenizer.encode("summarize: " + pdf_text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate a summary of the text
    summary_ids = model.generate(
        inputs,
        max_length=450,  # Maximum length of the summary
        min_length=200,  # Minimum length of the summary
        length_penalty=2.0,  # Penalize short sequences
        num_beams=4,  # Use beam search for better results
        early_stopping=True  # Stop when an optimal point is reached
    )

    # Decode the generated tokens to get the summary in text format
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Format the summary to make it more readable
    formatted_summary = "\n".join(textwrap.wrap(summary, width=80))
    return formatted_summary

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    pdf_bytes = await file.read()
    extracted_text = extract_text_from_pdf(pdf_bytes)
    extracted_text = extracted_text.replace('\n', ' ')  # Remove line breaks
    summary = text_summarizer_from_pdf(extracted_text).replace('\n', ' ')
    return {
        "filename": file.filename,
        "extracted_text_snippet": extracted_text[:200] + "...",  # Show first 200 characters
        "summary": summary  
    }

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
    <html>
        <head>
            <title>Upload PDF</title>
            <style>
                #loading {
                    display: none;
                    width: 100px;
                    height: 100px;
                    border: 10px solid #f3f3f3;
                    border-top: 10px solid #3498db;
                    border-radius: 50%;
                    animation: spin 2s linear infinite;
                    margin: auto;
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    left: 0;
                    right: 0;
                }

                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }

                #message {
                    display: none;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h2>Upload a PDF to Summarize</h2>
            <form id="upload-form" action="/uploadfile/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
            <div id="loading"></div>
            <p id="message">Please wait while the BART model processes your file. You will be redirected to <a href="/uploadfile" target="_blank">/uploadfile</a> when your summary is ready.</p>
            <script>
                const form = document.getElementById('upload-form');
                form.addEventListener('submit', function() {
                    document.getElementById('loading').style.display = 'block';
                    document.getElementById('message').style.display = 'block';
                });
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=content)


#path for interacting with mobile app
@app.get("/summarize_pdf/")
async def summarize_pdf_path(pdf_path: str):
    try:
        # Summarize the PDF using the provided path
        summary = text_summarizer_from_pdf(pdf_path)
        return {"summary": summary}
    except Exception as e:
        # Handle errors (e.g., file not found, invalid PDF)
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

# This part runs the FastAPI app with Uvicorn if the script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
