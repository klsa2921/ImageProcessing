import streamlit as st
import os
from werkzeug.utils import secure_filename
from process2 import process_file
import requests

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text():
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if uploaded_file is not None:
        if uploaded_file.name == '':
            st.error("No selected file")
            return

        if allowed_file(uploaded_file.name):
            filename = secure_filename(uploaded_file.name)
            filepath = os.path.join("uploads", filename)

            # Save the file
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                # Call your existing method to process the image or pdf
                extracted_text = process_file(filepath)
                st.success("Text extracted successfully!")
                st.text_area("Extracted Text", extracted_text)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        else:
            st.error("Invalid file format")
    else:
        st.info("Please upload a file")

if __name__ == "__main__":
    st.title("Text Extraction from Images or PDFs")
    extract_text()