from docling.document_converter import DocumentConverter
import pytesseract
from PIL import Image
import fitz
import pdf2image
import cv2
import numpy as np
import os
import easyocr
import pdf2image
import os
import numpy as np

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

def extract_text_from_file_for_pytesseract(file_path):
    # Check if the file is an image or a PDF
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        # Handle image file
        img = Image.open(file_path)

        # Preprocess the image
        preprocessed_image = preprocess_image(img)

        # Use Tesseract to extract text with optimal config for Arabic
        custom_config = r'--oem 1 --psm 6'  # Use OEM 1 for LSTM-based OCR, PSM 6 for standard block text
        text = pytesseract.image_to_string(preprocessed_image, lang='ara', config=custom_config)

    elif file_extension == '.pdf':
        # Handle PDF file
        text = ""
        # Convert PDF to images
        images = pdf2image.convert_from_path(file_path)

        for img in images:
            # Preprocess each image in the PDF
            preprocessed_image = preprocess_image(img)

            # Extract text from the preprocessed image
            custom_config = r'--oem 1 --psm 6'  # Use OEM 1 for LSTM-based OCR, PSM 6 for standard block text
            text += pytesseract.image_to_string(preprocessed_image, lang='ara', config=custom_config)

    else:
        raise ValueError("Unsupported file type. Only image and PDF files are supported.")

    return text

def extract_text_from_file_using_easyocr(file_path):
    # Initialize the EasyOCR reader with the specified language
    reader = easyocr.Reader(['ar'])  # Language support (default Arabic)

    # Check if the file is an image or a PDF
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        # Handle image file
        result = reader.readtext(file_path)
        predicted_result = ''
        for (bbox, text, conf) in result:
            predicted_result += text + " "
        return predicted_result.strip()

    elif file_extension == '.pdf':
        # Handle PDF file by converting each page to an image
        text = ""
        images = pdf2image.convert_from_path(file_path)

        for img in images:
            # Convert the PIL Image to a NumPy array
            img_np = np.array(img)

            # Convert the image to text using EasyOCR
            result = reader.readtext(img_np) # Pass the NumPy array
            for (bbox, text_in_page, conf) in result:
                text += text_in_page + " "

        return text.strip()
    else:
        raise ValueError("Unsupported file type. Only image and PDF files are supported.")

def extract_text_from_image_using_docling(image_path):
  converter = DocumentConverter()
  result=converter.convert(image_path)
  return result.document.export_to_text()


def process_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    text=''
    if file_extension=='.pdf':
      images=pdf2image.convert_from_path(file_path)

      for img in images:
        img_np=np.array(img)
        text+=extract_text(img_np)
    elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
       img = Image.open(file_path)
       text+=extract_text(img)
    
    return text
      

def extract_text(img):
    text=''
    try:
        print("extracting text using tesseract")
        text=extract_text_from_file_for_pytesseract(img)
    except Exception as e:
        print(f"Error processing  image (error: {str(e)} trying with easyocr")
        try:
            text=extract_text_from_file_using_easyocr(img)
        except Exception as e:
            print(f"Error processing  image (error: {str(e)} trying with docling")
            text=extract_text_from_image_using_docling(img)
    return text

def process_images_and_get_extracted_text(file_path):
  try:
    print("extracting text using tesseract")
    text=extract_text_from_file_for_pytesseract(file_path)
  except Exception as e:
    print(f"Error processing  (image: {file_path}): {str(e)} trying with easyocr")
    try:
      text=extract_text_from_file_using_easyocr(file_path)
    except Exception as e:
      print(f"Error processing  (image: {file_path}): {str(e)} trying with docling")
      text=extract_text_from_image_using_docling(file_path)
  return text