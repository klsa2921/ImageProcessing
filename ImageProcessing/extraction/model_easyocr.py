import numpy as np
from PIL import Image
import easyocr

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