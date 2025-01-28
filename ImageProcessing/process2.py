import cv2
import numpy as np
from PIL import Image
import pytesseract
import easyocr
from docling.document_converter import DocumentConverter
import pdf2image
import os
import json
import fitz  # PyMuPDF

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mmallikanti\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

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

def process_file(file_path, model):
    # Extract file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    result = {}

    if file_extension == '.pdf':
        # Convert PDF to images using PyMuPDF
        pdf_document = fitz.open(file_path)
        result['pages'] = []

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # img_np = np.array(img) ## 
            if model == 'default':
                output, model_used = extract_text(img)
            else:
                output, model_used = extract_text2(img, model)
            result['pages'].append({
                'page_number': page_number + 1,
                'model_used': model_used,
                'extracted_text': output
            })

    elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        # Handle image files directly
        img = Image.open(file_path)
        if model == 'default':
            output, model_used = extract_text(img)
        else:
            output, model_used = extract_text2(img, model)
        result['image_path'] = file_path
        result['model_used'] = model_used
        result['extracted_text'] = output

    else:
        raise ValueError("Unsupported file type. Only image and PDF files are supported.")

    return json.dumps(result, indent=4, ensure_ascii=False)

def extract_text(image):
    text = ''
    model_used = ''
    try:
        print("Extracting text using Tesseract...")
        text = extract_text_from_file_for_pytesseract(image)
        model_used = 'model1'
    except Exception as e:
        print(f"Error processing image with Tesseract (error: {str(e)}). Trying with EasyOCR...")
        try:
            
            text = extract_text_from_file_using_easyocr(image)
            model_used = 'model2'
        except Exception as e:
            
            print(f"Error processing image with EasyOCR (error: {str(e)}). Trying with Docling...")
            text = extract_text_from_image_using_docling(image)
            model_used = 'model3'
    
    return text, model_used


def extract_text2(image, model):
    text = ''
    model_used = ''
    try:
        if model == 'Tesseract':
            print("Extracting text using Tesseract...")
            text = extract_text_from_file_for_pytesseract(image)
            model_used = 'model1'
        elif model == 'EasyOCR':
            print("Extracting text using EasyOCR...")
            text = extract_text_from_file_using_easyocr(image)
            model_used = 'model2'
        elif model == 'Docling':
            print("Extracting text using Docling...")
            text = extract_text_from_image_using_docling(image)
            model_used = 'model3'
        else:
            raise ValueError("Unsupported model specified.")
    except Exception as e:
        print(f"Error processing image with {model} (error: {str(e)}).")
    
    return text, model_used
