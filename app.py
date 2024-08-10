import os
import openai
import streamlit as st
import fitz  # PyMuPDF
import re
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text.append(page.get_text("text"))
        doc.close()
        return "\n".join(text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Function to preprocess text
def preprocess_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
    return cleaned_text.strip()

# Function to query the OpenAI API
def query_resume_model(prompt, cleaned_resume_text):
    full_prompt = f"Based on the following resume: {cleaned_resume_text}\n\n{prompt}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit App
st.title("Chat With Your Resume")

# File uploader for PDF files
uploaded_file = st.file_uploader("Upload your resume PDF", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file to a local directory
    save_dir = "C:/Users/virat/Desktop/chatwithprem/uploads"
    os.makedirs(save_dir, exist_ok=True)
    pdf_path = os.path.join(save_dir, uploaded_file.name)
    
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract and clean text from the PDF
    resume_text = extract_text_from_pdf(pdf_path)
    cleaned_resume_text = preprocess_text(resume_text)
    
    st.subheader("Extracted Resume Text")
    # st.write(resume_text)

    # Input box for user questions
    query = st.text_input("Enter your question about the resume")
    
    if query:
        response = query_resume_model(query, cleaned_resume_text)
        st.subheader("Response")
        st.write(response)
else:
    st.info("Please upload a PDF file to start.")
