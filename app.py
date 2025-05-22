import streamlit as st
from pdfminer.high_level import extract_text
import tempfile
import re
import spacy
import os

# Title
st.title("PDF Resume Parser")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Define skill set
skills_list = ['python', 'java', 'sql', 'c++', 'machine learning', 'html', 'css', 'javascript', 'react']

# NLP helper functions
def extract_name(text, nlp):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_email(text):
    email = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-zA-Z]+", text)
    return email[0] if email else None

def extract_phone(text):
    phone = re.findall(r'(\(?\d{3}\)?\s?-?\d{3}-\d{4})', text)
    return phone[0] if phone else None

def extract_skills(text):
    text = text.lower()
    return [skill for skill in skills_list if skill in text]

def extract_education(text):
    edu = re.findall(r'(B\.S\.|M\.S\.|Bachelor|Masters|Ph\.D\.).*', text, re.IGNORECASE)
    return edu

def extract_experience(text):
    lines = text.split('\n')
    exp = [line for line in lines if 'experience' in line.lower() or 'engineer' in line.lower()]
    return exp

# Handle file upload
if uploaded_file is not None:
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Extract text from PDF
        text = extract_text(tmp_path)

        if text.strip():
            st.success("✅ PDF processed successfully!")
            st.subheader("Extracted Text (First 2000 characters):")
            st.text(text[:2000])  # Display partial text

            # Load SpaCy model
            nlp = spacy.load("en_core_web_sm")

            # Extract and display details
            st.subheader("Extracted Information:")
            st.write("**Name:**", extract_name(text, nlp))
            st.write("**Email:**", extract_email(text))
            st.write("**Phone:**", extract_phone(text))
            st.write("**Skills:**", ", ".join(extract_skills(text)))
            st.write("**Education:**", extract_education(text))
            st.write("**Experience Snippets:**", extract_experience(text))

        else:
            st.warning("The PDF file appears to be empty or text could not be extracted.")

    except Exception as e:
        st.error(f"⚠️ Error extracting text from PDF: {e}")
else:
    st.info("Please upload a PDF file to proceed.")

