import cv2
import numpy as np
from PIL import Image
import pytesseract
import easyocr
from docling import DocumentConverter
import pdf2image
import os

def preprocess_image(image):
    # Convert the image to grayscale if it is in RGB format
    if image.mode != 'L':
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    else:
        gray_image = np.array(image)

    # Apply binary thresholding using Otsu's method
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply Gaussian blur to reduce noise
    denoised_image = cv2.GaussianBlur(binary_image, (5, 5), 0)

    return denoised_image

def extract_text_from_file_for_pytesseract(image):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Use Tesseract to extract text with optimal config for Arabic
    custom_config = r'--oem 1 --psm 6'  # Use OEM 1 for LSTM-based OCR, PSM 6 for standard block text
    text = pytesseract.image_to_string(preprocessed_image, lang='ara', config=custom_config)

    return text

def extract_text_from_file_using_easyocr(image):
    # Initialize the EasyOCR reader with the specified language
    reader = easyocr.Reader(['ar'])  # Language support (default Arabic)

    # Convert the PIL Image to a NumPy array if it's a PIL image
    if isinstance(image, Image.Image):
        image = np.array(image)

    # Convert the image to text using EasyOCR
    result = reader.readtext(image)  # Pass the NumPy array
    text = ""
    for (bbox, text_in_page, conf) in result:
        text += text_in_page + " "

    return text.strip()

def extract_text_from_image_using_docling(image):
    # Convert the image to a temporary file if needed for Docling
    # If the image is a PIL Image, save it to a temporary file and convert
    if isinstance(image, Image.Image):
        image_path = "/tmp/temp_image.png"
        image.save(image_path)
    else:
        image_path = image  # Assume it's already a file path if it's not a PIL image

    # Use DocumentConverter from Docling
    converter = DocumentConverter()
    result = converter.convert(image_path)
    extracted_text = result.document.export_to_text()

    # Remove the temporary file after extraction
    if isinstance(image, Image.Image):  # Only remove the file if it was created
        if os.path.exists(image_path):
            os.remove(image_path)

    return extracted_text

def process_file(file_path):
    # Extract file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    text = ''
    
    if file_extension == '.pdf':
        # Convert PDF to images
        images = pdf2image.convert_from_path(file_path)

        for img in images:
            img_np = np.array(img)
            text += extract_text(img_np)
    
    elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        # Handle image files directly
        img = Image.open(file_path)
        text += extract_text(img)

    else:
        raise ValueError("Unsupported file type. Only image and PDF files are supported.")
    
    return text

def extract_text(image):
    text = ''
    try:
        print("Extracting text using Tesseract...")
        text = extract_text_from_file_for_pytesseract(image)
    except Exception as e:
        print(f"Error processing image with Tesseract (error: {str(e)}). Trying with EasyOCR...")
        try:
            text = extract_text_from_file_using_easyocr(image)
        except Exception as e:
            print(f"Error processing image with EasyOCR (error: {str(e)}). Trying with Docling...")
            text = extract_text_from_image_using_docling(image)
    
    return text
