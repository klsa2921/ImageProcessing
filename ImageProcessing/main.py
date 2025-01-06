from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from process import process_file
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            # Call your existing method to process the image or pdf
            # extracted_text = process_images_and_get_extracted_text(filepath)
            extracted_text=process_file(filepath)
            print(extracted_text)
            return jsonify({"text": extracted_text}), 200

        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400


if __name__ == "__main__":
    # Ensure uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(debug=True,host="0.0.0.0", port=11200)


#curl -X POST -F "file=@/home/ds1/ImageProcessing/arabic1.png" http://192.168.1.46:11201/extract_text
