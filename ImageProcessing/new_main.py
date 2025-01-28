import streamlit as st
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from threading import Thread
from flask_cors import CORS
from process_file.process import process_file

models={
    "model1":"Tesseract",
     "model2":"EasyOCR",
     "model3":"Docling",
        "default":"default"
}

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask route to extract text
@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join("uploads", filename)

        # Save the file
        file.save(filepath)

        try:
            # Call the existing method to process the image or pdf
            extracted_text = process_file(filepath,"default")
            return jsonify({"text": extracted_text}), 200

        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400

# Streamlit app for frontend
def streamlit_app():
    st.title("Text Extraction from Images or PDFs")
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    model_selector = st.selectbox("Select a model", ["default","model1", "model2", "model3"])
    # language_selector = st.selectbox("Select a language", ["eng","ara"])
    
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
                extracted_text = process_file(filepath,models[model_selector])
                st.success("Text extracted successfully!")
                st.text_area("Extracted Text", extracted_text,height=500)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        else:
            st.error("Invalid file format")
    else:
        st.info("Please upload a file")



# Start Flask app in a separate thread
def start_flask():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(debug=True, host="0.0.0.0", port=11200, use_reloader=False)

if __name__ == "__main__":
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Start Flask app in background
    flask_thread = Thread(target=start_flask)
    flask_thread.start()

    # Run Streamlit app
    streamlit_app()
