import cv2
import numpy as np
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mmallikanti\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

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